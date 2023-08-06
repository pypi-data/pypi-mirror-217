from argparse import Namespace
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_, select, delete, true, event, DDL
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from time import sleep
from threading import Thread
import queue
import logging as log
from logging.config import dictConfig
import os
from subprocess import run, Popen, PIPE
import signal
import json as json_module
from sqlalchemy.dialects import sqlite
from .util import PropagatingThread, package_path, package_version, check_dir, to_dict, tryupdate
from .default_settings import SQLALCHEMY_POOL_SIZE, SQLALCHEMY_DATABASE_URI
from .ansible.scitq.sqlite_inventory import scitq_inventory
from .constants import SIGNAL_CLEAN, SIGNAL_RESTART


MAIN_THREAD_SLEEP = 5
WORKER_OFFLINE_DELAY = 15
SCITQ_SERVER = os.environ.get('SCITQ_SERVER',None)

WORKER_CREATE = f'cd {package_path("ansible","playbooks")} && ansible-playbook deploy_one_vm.yaml --extra-vars \
"nodename={{hostname}} concurrency={{concurrency}} status=running flavor={{flavor}} \
region={{region}} provider={{provider}}"'

if SCITQ_SERVER is not None:
    WORKER_CREATE = WORKER_CREATE[:-1] + f' target={SCITQ_SERVER}"'
WORKER_DELETE = os.environ.get('WORKER_DELETE',
    f'cd {package_path("ansible","playbooks")} && ansible-playbook destroy_vm.yaml --extra-vars "nodename={{hostname}}"')
SERVER_CRASH_WORKER_RECOVERY = os.environ.get('SERVER_CRASH_WORKER_RECOVERY',
    f'cd {package_path("ansible","playbooks")} && ansible-playbook check_after_reboot.yaml')
WORKER_IDLE_CALLBACK = os.environ.get('WORKER_IDLE_CALLBACK',WORKER_DELETE)
WORKER_CREATE_CONCURRENCY = 10
WORKER_CREATE_RETRY=2
WORKER_CREATE_RETRY_SLEEP=30
UI_OUTPUT_TRUNC=100
UI_MAX_DISPLAYED_ROW = 500
WORKER_DESTROY_RETRY=2

if os.environ.get('QUEUE_PROCESS') and os.environ.get('QUEUE_LOG_FILE'):
    check_dir(os.environ.get('QUEUE_LOG_FILE'))
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }, "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": os.environ.get('QUEUE_LOG_FILE'),
            "maxBytes": int(os.environ.get('QUEUE_LOG_FILE_MAX_SIZE',
                os.environ.get('LOG_FILE_MAX_SIZE',"10000000"))),
            "backupCount": int(os.environ.get('QUEUE_LOG_FILE_KEEP',
                os.environ.get('LOG_FILE_KEEP',"3")))
        }},
        'root': {
            'level': os.environ.get('LOG_LEVEL',"INFO"),
            'handlers': ['wsgi' if 'DEBUG' in os.environ else 'file']
        }
    })
else:
    check_dir(os.environ.get('LOG_FILE',"/tmp/scitq.log"))
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }, "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": os.environ.get('LOG_FILE',"/tmp/scitq.log"),
            "maxBytes": int(os.environ.get('LOG_FILE_MAX_SIZE',"10000000")),
            "backupCount": int(os.environ.get('LOG_FILE_KEEP',"3"))
        }},
        'root': {
            'level': os.environ.get('LOG_LEVEL',"INFO"),
            'handlers': ['wsgi' if 'DEBUG' in os.environ else 'file']
        }
    })

IS_SQLITE = 'sqlite' in SQLALCHEMY_DATABASE_URI


log.info('Starting')
log.warning(f'WORKER_CREATE is {WORKER_CREATE}')

#worker_create_queue = queue.Queue()


# via https://github.com/pallets/flask-sqlalchemy/blob/main/examples/hello/hello.py
app = Flask(__name__, instance_relative_config=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/"
app.config.from_object('scitq.default_settings')
#app.config.from_pyfile("scitq.cfg", silent=True)
#app.config.from_prefixed_env()
if SQLALCHEMY_POOL_SIZE is not None:
    db = SQLAlchemy(app, engine_options={'pool_size': int(SQLALCHEMY_POOL_SIZE)})
else:
    db = SQLAlchemy(app)

# with uwsgi, the master worker is forking to create the workers which receive a 
# non-working connection (because it comes from another process), it must be discarded
# so that workers re-open the connection properly
# idea from https://stackoverflow.com/questions/39562838/how-to-configure-pyramid-uwsgi-sqlalchemy
try:
    # import uwsgi is only working in uwsgi context. It is normal that is fails
    # to import in VisualStudioCode or manually
    import uwsgi # pyright: ignore[reportMissingImports]

    def postfork():
        db.engine.dispose()
    uwsgi.post_fork_hook = postfork
except ImportError:
    pass

 #######  ######   ######  
 #     #  #     #  #     # 
 #     #  #     #  #     # 
 #     #  ######   ######  
 #     #  #   #    #     # 
 #     #  #    #   #     # 
 #######  #     #  ######  




class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    command = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    modification_date = db.Column(db.DateTime)
    batch = db.Column(db.String, nullable=True)
    input = db.Column(db.String, nullable=True)
    output = db.Column(db.String, nullable=True)
    container = db.Column(db.String, nullable=True)
    container_options = db.Column(db.String, nullable=True)
    resource = db.Column(db.String, nullable=True)

    def __init__(self, command, name=None, status='pending', batch=None, 
                    input=None, output=None, container=None, 
                    container_options=None, resource=None):
        self.name = name
        self.command = command
        self.status = status
        self.creation_date = datetime.utcnow()
        self.modification_date = self.creation_date
        self.batch = batch
        self.input = input
        self.output = output
        self.container = container
        self.container_options = container_options
        self.resource = resource


class Worker(db.Model):
    __tablename__ = "worker"
    worker_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String, nullable=False)
    hostname = db.Column(db.String)
    status = db.Column(db.String, nullable=False)
    concurrency = db.Column(db.Integer)
    prefetch = db.Column(db.Integer)
    load = db.Column(db.String)
    memory=db.Column(db.String)
    stats=db.Column(db.String)
    creation_date = db.Column(db.DateTime)
    modification_date = db.Column(db.DateTime)
    last_contact_date = db.Column(db.DateTime)
    batch = db.Column(db.String,nullable=True)
    idle_callback = db.Column(db.String, nullable=True)

    def __init__(self, name, concurrency, prefetch=0, hostname=None, 
                status='paused', batch=None, idle_callback=None):
        self.name = name
        self.concurrency = concurrency
        self.prefetch = prefetch
        self.status = status
        self.creation_date = datetime.utcnow()
        self.modification_date = self.creation_date
        self.hostname = hostname
        self.batch = batch
        self.idle_callback = idle_callback
    

class Execution(db.Model):
    __tablename__ = "execution"
    execution_id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.worker_id"), nullable=True)
    worker = db.relationship(
        Worker,
        backref=db.backref('executions',
                         uselist=True,
                         cascade='save-update',
                         order_by='Execution.modification_date.desc()'))
    task_id = db.Column(db.Integer, db.ForeignKey("task.task_id"), nullable=False)
    task = db.relationship(
        Task,
        backref=db.backref('tasks',
                         uselist=True,
                         cascade='delete,all'),
                         order_by='Execution.creation_date')
    status = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    modification_date = db.Column(db.DateTime)
    output = db.Column(db.Text)
    error = db.Column(db.Text)
    return_code = db.Column(db.Integer)
    pid = db.Column(db.String)
    output_files = db.Column(db.String, nullable=True)
    command = db.Column(db.String, nullable=True)
    latest = db.Column(db.Boolean, default=True)
    

    def __init__(self, worker_id, task_id, status='pending', pid=None, 
                    return_code=None, command=None):
        self.worker_id = worker_id
        self.task_id = task_id
        self.status = status
        self.pid = pid
        self.return_code = return_code
        self.creation_date = datetime.utcnow()
        self.modification_date = self.creation_date
        self.command = command

trigger_latest_sqlite = DDL("""
        CREATE TRIGGER is_latest BEFORE INSERT ON execution FOR EACH ROW 
        BEGIN
            UPDATE execution SET latest=false WHERE latest AND task_id=NEW.task_id;
        END
        """)

func_latest_postgres = DDL("""
        CREATE OR REPLACE FUNCTION render_obsolete() 
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        BEGIN
            UPDATE execution 
            SET latest=false
            WHERE task_id=NEW.task_id
            AND latest;
            RETURN NEW;
        END;
        $$
        """)

trigger_latest_postgres = DDL("""
CREATE TRIGGER is_latest BEFORE INSERT ON execution FOR EACH ROW EXECUTE PROCEDURE render_obsolete()
""")

event.listen(
    Execution.__table__, 'after_create',
    trigger_latest_sqlite.execute_if(dialect="sqlite")    
)
event.listen(
    Execution.__table__, 'after_create',
    func_latest_postgres.execute_if(dialect="postgresql")    
)
event.listen(
    Execution.__table__, 'after_create',
    trigger_latest_postgres.execute_if(dialect="postgresql")    
)

class Signal(db.Model):
    __tablename__ = "signal"
    #execution_id = db.Column(db.Integer, db.ForeignKey("execution.execution_id"), primary_key=True, nullable=True)
    signal_id = db.Column(db.Integer, primary_key=True)
    execution_id = db.Column(db.Integer, db.ForeignKey("execution.execution_id"), nullable=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.worker_id"))
    signal = db.Column(db.Integer, nullable=False)    

    def __init__(self, execution_id, worker_id, signal):
        self.execution_id = execution_id
        self.worker_id = worker_id
        self.signal = signal


class Job(db.Model):
    __tablename__ = "job"
    job_id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String)
    action = db.Column(db.String)
    args = db.Column(db.JSON, default={})
    retry =  db.Column(db.Integer, default = 0)
    status = db.Column(db.String, default = 'pending')
    log = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, server_default=func.now())
    modification_date = db.Column(db.DateTime, onupdate=func.now())
    

    def __init__(self, target, action, args={}, retry=0):
        self.target = target
        self.action = action
        self.args = args
        self.retry = retry


def create_worker_destroy_job(worker, session, commit=True):
    job = Job(target = worker.name,
        action='worker_destroy',
        args=to_dict(worker),
        retry=WORKER_DESTROY_RETRY)
    session.add(job)
    if commit:
        session.commit()


with app.app_context():
    db.create_all()


 ######      #     ####### 
 #     #    # #    #     # 
 #     #   #   #   #     # 
 #     #  #     #  #     # 
 #     #  #######  #     # 
 #     #  #     #  #     # 
 ######   #     #  ####### 
                           


def process_filtering_args(ObjectType, args):
    """In list functions it seems natural to filter the results with some attributes
    conditions (such as 'batch="foo"' or 'status="succeeded"') and it makes more 
    efficient queries than listing the lot and filtering the results out or sending
    several individual queries (one per item id).
    However sqlalchemy filtering syntax is not friendly when using typical python
    optional args dictionary, this function does this transformation:
    
    When args maybe something as 'batch="foo"' or 'batch=["foo","bar"]'
    - the function will return 'ObjectType.batch=="foo"'
    - or 'ObjectType.batch.in_(["foo","bar"])' if value is a list

    which can then be passed to sqlalchemy .filter() function
    """
    # 
    # filter expects something as 'ObjectType.batch=="foo"'
    # or 'ObjectType.batch.in_(["foo","bar"])' if value is a list
    new_args = [ getattr(ObjectType,attribute).in_(value) if type(value)==list else \
                 getattr(ObjectType,attribute)==value 
                    for attribute,value in args.items() ]
    return and_(*new_args) if len(new_args)>1 else new_args[0]


# via https://flask-restx.readthedocs.io/en/latest/example.html
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TaskMVC API',
    description='A simple TaskMVC API'
)


class BaseDAO(object):
    ObjectType = None
    authorized_status = []

    def get(self, id):
        object = self.ObjectType.query.get(id)
        if object is None:
            api.abort(404, "{} {} doesn't exist".format(
                    self.ObjectType.__name__,id))
        return object
        
    def create(self, data):
        object = self.ObjectType(**data)
        if 'status' in data and data['status'] not in self.authorized_status:
            api.abort(500,
                f"Status {data['status']} is not possible (only {' '.join(self.authorized_status)})")
        db.session.add(object)
        db.session.commit()
        return object

    def update(self, id, data):
        object = self.get(id)
        modified = False
        for attr, value in data.items():
            if hasattr(object,attr): 
                if getattr(object,attr)!=value:
                    if attr=='status' and value not in self.authorized_status:
                        api.abort(500,
                           f"Status {value} is not possible (only {' '.join(self.authorized_status)})")
                    setattr(object, attr, value)
                    modified = True
            else:
                api.abort(500,f'Error: {object.__name__} has no attribute {attr}')
        if modified:
            if hasattr(object,'modification_date'):
                object.modification_date = datetime.utcnow()
            db.session.commit()
        return object

    def delete(self, id):
        object = self.get(id)
        db.session.delete(object)
        db.session.commit()
        return object
    
    def list(self, sorting_column=None, **args):
        if args:
            final_filter = process_filtering_args(self.ObjectType, args)
            return list(self.ObjectType.query.filter(final_filter).order_by(sorting_column))
        else:
            return list(self.ObjectType.query.order_by(sorting_column).all())
        
        



ns = api.namespace('tasks', description='TASK operations')

class TaskDAO(BaseDAO):
    ObjectType = Task
    authorized_status = ['paused','pending','assigned','accepted','running','failed','succeeded']

    def list(self, **args):
        return super().list(sorting_column='task_id',**args)

    def update(self, id, data):
        task = self.get(id)
        modified = False
        for attr, value in data.items():
            if hasattr(task,attr): 
                if getattr(task,attr)!=value:
                    if attr=='status':
                        if value not in self.authorized_status:
                            api.abort(500,
                                f"Status {value} is not possible (only {' '.join(self.authorized_status)})")
                        if task.status=='running':
                            for execution in db.session.query(Execution).filter(
                                    Execution.task_id==id, Execution.status=='running'):
                                db.session.add(Signal(execution.execution_id, execution.worker_id, 9))
                                execution.status='failed'
                                execution.modification_date = datetime.utcnow()
                    setattr(task, attr, value)
                    modified = True
            else:
                raise Exception('Error: {} has no attribute {}'.format(
                    task.__name__, attr))
        if modified:
            task.modification_date = datetime.utcnow()
            db.session.commit()
        return task


task_dao = TaskDAO()

task = api.model('Task', {
    'task_id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=False, description='The task (optional) name'),
    'status': fields.String(required=False, 
        description=f'The task status: {", ".join(TaskDAO.authorized_status)}'), 
    'command': fields.String(required=True, description='The task command'), 
    'creation_date': fields.DateTime(readonly=True, 
        description='timestamp of task creation in server'),
    'modification_date': fields.DateTime(readonly=True,
        description='timestamp of task last modification'),
    'batch': fields.String(required=False, 
        description="only workers with the same batch (null or not) will accept the task."),
    'input': fields.String(required=False,
        decription="Input data required for task (space separated files URL in s3://...)"),
    'output': fields.String(required=False,
        decription="Output data basepath where /output content will be copied (if null, the result transmission is up to the command)"),
    'container': fields.String(required=False,
        decription="Container (as for now this is a docker) in which task is launched"),
    'container_options': fields.String(required=False,
        decription="Container (extra) option if needed"),
    'resource': fields.String(required=False,
        decription="Resource data required for task (much like input except it is shared between tasks) (space separated files URL in s3://...)"),
})

task_filter = api.model('TaskFilter', {
    'task_id': fields.List(fields.Integer(),required=False,decription='A list of ids to restrict listing'),
    'batch': fields.String(required=False, description="Filter with this batch"),
    'status': fields.String(required=False, description="Filter with this status"),
    'name': fields.String(required=False, description="Filter with this name"),
})


@ns.route('/')
class TaskList(Resource):
    '''Shows a list of all tasks, and lets you POST to add new tasks'''
    @ns.doc('list_tasks')
    @ns.expect(task_filter)
    @ns.marshal_list_with(task)
    def get(self):
        '''List all tasks'''
        return task_dao.list(**api.payload) if api.payload else task_dao.list()

    @ns.doc('create_task')
    @ns.expect(task)
    @ns.marshal_with(task, code=201)
    def post(self):
        '''Create a new task'''
        return task_dao.create(api.payload), 201


@ns.route("/<id>")
@ns.param("id", "The task identifier")
@ns.response(404, "Task not found")
class WorkerObject(Resource):
    @ns.doc("get_task")
    @ns.marshal_with(task)
    def get(self, id):
        """Fetch a task given its identifier"""
        return task_dao.get(id)

    @ns.doc("update_task")
    @ns.expect(task)
    @ns.marshal_with(task, code=201)
    def put(self, id):
        """Update a task"""
        return task_dao.update(id, api.payload)

    @ns.doc("delete_task")
    @ns.marshal_with(task)
    def delete(self, id):
        """Delete a task"""
        return task_dao.delete(id)

ns = api.namespace('workers', description='WORKER operations')



class WorkerDAO(BaseDAO):
    ObjectType = Worker
    authorized_status = ['paused','running','offline','failed']

    def update_contact(self, id, load,memory,stats):
        db.engine.execute(
            db.update(Worker
                    ).values({'last_contact_date':datetime.utcnow(),
                        'load':load,'memory':memory,'stats':stats}
                    ).where(Worker.worker_id==id)
        )
        db.session.commit()

    def delete(self,id,is_destroyed=False, session=db.session):
        """Delete a worker
        """
        worker=self.get(id)
        log.warning(f'Deleting worker {id} ({worker.idle_callback})')
        if worker.idle_callback is not None and not is_destroyed:
            create_worker_destroy_job(worker, session)
            return worker
        else:
            object = self.get(id)
            session.delete(object)
            session.commit()
            return object

    def list(self):
        return super().list(sorting_column='worker_id')

worker_dao = WorkerDAO()

worker = api.model('Worker', {
    'worker_id': fields.Integer(readonly=True, description='The worker unique identifier'),
    'name': fields.String(required=True, description='The worker name'),
    'concurrency': fields.Integer(required=True, 
        description='The worker concurrency (nb of parallel processes)'), 
    'prefetch': fields.Integer(required=False, 
        description='How many jobs should be prefetch so that they can be launched as soon as possible'),     
    'hostname': fields.String(required=False, description='The worker hostname'),
    'status': fields.String(required=False,
         description=f'The worker status: {", ".join(WorkerDAO.authorized_status)}'), 
    'load': fields.String(readonly=True, description='The worker load (in %)'),
    'memory':fields.Float(readonly=True, description='Memory used (in %)'),
    'stats':fields.String(readonly=True,description='Other worker stats'),
    'creation_date': fields.DateTime(readonly=True, 
        description='timestamp of worker creation'),
    'modification_date': fields.DateTime(readonly=True, 
        description='timestamp of last worker modification'),
    'last_contact_date': fields.DateTime(readonly=True, 
        description='timestamp of last worker ping (automatically sent by worker'),
    'batch': fields.String(required=False, 
        description="worker accept only tasks with same batch (null or not)."),
    'idle_callback': fields.String(readonly=True,
        description="A command to be called on scitq server when the worker load *returns* to zero. Typically used to end cloud instances.")
})

@ns.route('/')
class WorkerList(Resource):
    '''Shows a list of all workers, and lets you POST to add new workers'''
    @ns.doc('list_workers')
    @ns.marshal_list_with(worker)
    def get(self):
        '''List all workers'''
        return worker_dao.list()

    @ns.doc('create_worker')
    @ns.expect(worker)
    @ns.marshal_with(worker, code=201)
    def post(self):
        '''Create a new worker'''
        return worker_dao.create(api.payload), 201


worker_tasks = api.model('WorkerTasks', {
    'worker_id': fields.Integer(readonly=True, description='A worker unique identifier'),
    'status': fields.String(readonly=True, description='The different status of tasks'), 
    'count': fields.Integer(readonly=True, description='How many tasks of this type'),
})

@ns.route("/tasks")
class WorkerTaskList(Resource):
    '''Shows a list of all tasks in all workers, and lets you POST to add new workers'''
    @ns.doc('list_worker_tasks')
    @ns.marshal_list_with(worker_tasks)
    def get(self):
        '''List all workers'''
        return list(db.session.execute("""SELECT w.worker_id, e.status, count(e.task_id) as count 
            FROM worker w
            JOIN execution e ON (e.worker_id=w.worker_id)
            JOIN task t ON (e.task_id=t.task_id 
                AND e.latest)
            GROUP BY w.worker_id,e.status"""))
    

@ns.route("/<id>")
@ns.param("id", "The worker identifier")
@ns.response(404, "Worker not found")
class WorkerObject(Resource):
    @ns.doc("get_worker")
    @ns.marshal_with(worker)
    def get(self, id):
        """Fetch a worker given its identifier"""
        return worker_dao.get(id)

    @ns.doc("update_worker")
    @ns.expect(worker)
    @ns.marshal_with(worker, code=201)
    def put(self, id):
        """Update a worker"""
        #worker_dao.update_contact(id)
        if 'batch' in api.payload and api.payload['batch']=='':
            api.payload['batch']==None
        return worker_dao.update(id, api.payload)

    @ns.doc("delete_worker")
    @ns.marshal_with(worker)
    def delete(self, id):
        """Delete a worker"""
        return worker_dao.delete(id)

ping_parser = api.parser()
ping_parser.add_argument('load', type=str, help='Worker load', location='json')
ping_parser.add_argument('memory', type=float, help='Worker memory', location='json')
ping_parser.add_argument('stats', type=str, help='Worker other stats', location='json')

@ns.route("/<id>/ping")
@ns.param("id", "The worker identifier")
@ns.response(404, "Worker not found")
class WorkerPing(Resource):
    @ns.doc("update_worker_contact")
    @ns.expect(ping_parser)
    @ns.marshal_with(worker)
    def put(self, id):
        """Update a worker last contact"""
        args = ping_parser.parse_args()
        worker_dao.update_contact(id, args.get('load',''),args.get('memory',''),args.get('stats',''))
        return worker_dao.get(id)

callback_parser = api.parser()
callback_parser.add_argument('message', type=str, help='Callback message sent (idle)', location='json')

@ns.route("/<id>/callback")
@ns.param("id", "The worker identifier")
@ns.response(404, "Worker not found")
class WorkerCallback(Resource):
    @ns.doc("update_worker_contact")
    @ns.expect(callback_parser)
    def put(self, id):
        """Update a worker last contact"""
        message = callback_parser.parse_args().get('message','')
        worker = worker_dao.get(id)
        if message == 'idle' and worker.idle_callback:
            if db.session.query(Execution).filter(Execution.status=='running',
                    Execution.worker_id==worker.worker_id).count()>0:
                log.warning(f'Worker {worker.name} called idle callback but some tasks are still running, refusing...')
                return {'result':'still have running tasks'}
            if db.session.query(Task).filter(and_(Task.status.in_(['pending']),
                                    Task.batch==worker.batch)).count()>0:
                log.warning(f'Worker {worker.name} called idle but some tasks are still due...')
                return {'result':'still some work to do, lazy one!'}
            log.warning(f'Worker {worker.name} ({worker.worker_id}) called idle callback, launching: '+worker.idle_callback.format(**(worker.__dict__)))
            #worker.destroy()
            create_worker_destroy_job(worker, db.session, commit=False)
            #db.session.delete(worker)
            db.session.commit()
            return {'result':'ok'}
        else:
            log.warning(f'Worker {worker.name} called idle callback but has no idle command')
            return {'result':'nothing to do'}

deploy_parser = api.parser()
deploy_parser.add_argument('number', type=int, help='How many workers should be deployed', location='json')
deploy_parser.add_argument('region', type=str, help='Which provider region for worker', location='json')
deploy_parser.add_argument('provider', type=str, help='Specify the worker provider', location='json')
deploy_parser.add_argument('flavor', type=str, help='Which provider flavor/model for worker', location='json')
deploy_parser.add_argument('batch', type=str, help='Batch name (that must be shared by tasks) for worker', location='json')
deploy_parser.add_argument('concurrency', type=int, help='How many tasks should be run in parallel', location='json')
deploy_parser.add_argument('prefetch', type=int, help='How many extra tasks should be prefetched', location='json')

@ns.route("/deploy")
class WorkerDeploy(Resource):
    @ns.doc("deploy_worker_vm_and_process")
    @ns.expect(deploy_parser)
    def put(self):
        """Create and deploy one or several workers"""
        deploy_args = deploy_parser.parse_args()

        for _ in range(deploy_args['number']):
            db.session.add(
                Job(target='', 
                    action='worker_create', 
                    args={
                        'concurrency': deploy_args['concurrency'], 
                        'prefetch':deploy_args['prefetch'],
                        'flavor':deploy_args['flavor'],
                        'region':deploy_args['region'],
                        'provider':deploy_args['provider'],
                        'batch':deploy_args['batch']
                    }
                )
            )
        db.session.commit()


        return {'result':'ok'}

class ExecutionDAO(BaseDAO):
    ObjectType = Execution
    authorized_status = ['pending','accepted','running','failed','succeeded']

    def create(self, data):
        task = task_dao.get(data['task_id'])
        if task.status not in ['pending','paused']:
            api.abort(500, f"A new execution for task {task.task_id} is not possible")
        if 'status' in data:
            if data['status']=='running':
                task.status = 'running'
            elif data['status'] in ['pending','paused']:
                task.status = 'assigned'
            else:
                api.abort(500, f"A new execution cannot be created with a status {data['status']}")
        else:
            task.status='assigned'
        return super().create(data)

    def update(self, id, data):
        execution = self.get(id)
        modified = False
        for attr, value in data.items():
            if hasattr(execution,attr): 
                if getattr(execution,attr)!=value:
                    if attr=='status':
                        if value not in self.authorized_status:
                            api.abort(500,
                                f"Status {value} is not possible (only {' '.join(self.authorized_status)})")
                        task=task_dao.get(execution.task_id)
                        if execution.status=='pending':
                            if value=='running':
                                task.status = 'running'
                                task.modification_date = datetime.utcnow()
                            elif value=='accepted':
                                task.status = 'accepted'
                                task.modification_date = datetime.utcnow()
                            elif value in ['refused','failed']:
                                task.status = 'pending'
                                task.modification_date = datetime.utcnow()
                            elif value=='succeeded':
                                task.status = 'succeeded'
                                task.modification_date = datetime.utcnow()
                            else:
                                api.abort(500, f"An execution cannot change status from pending to {value}")
                        elif execution.status=='accepted':
                            if value in ['running','failed','succeeded','pending']:
                                task.status = value
                                task.modification_date = datetime.utcnow()
                            else:
                                log.exception(f"An execution cannot change status from accepted to {value}")
                                api.abort(500, f"An execution cannot change status from accepted to {value}")
                        elif execution.status=='running':
                            if value in ['succeeded', 'failed']:
                                task.status=value
                                task.modification_date = datetime.utcnow()
                            else:
                                log.exception(f"An execution cannot change status from running to {value}")
                                api.abort(500, f"An execution cannot change status from running to {value}")
                        else:
                            api.abort(500, f"An execution cannot change status from {execution.status} (only from pending, running or accepted)")
                    setattr(execution, attr, value)
                    modified = True
            else:
                raise Exception('Error: {} has no attribute {}'.format(
                    execution.__name__, attr))
        if modified:
            execution.modification_date = datetime.utcnow()
            db.session.commit()
        return execution

    def list(self,no_output=False,**args):
        sorting_column='execution_id'
        q=Execution.query
        if args:
            q=q.filter(process_filtering_args(Execution, args))
        if no_output:
            q=q.with_entities(Execution.execution_id,
                              Execution.command, 
                              Execution.status,
                              Execution.task_id,
                              Execution.creation_date,
                              Execution.modification_date,
                              Execution.pid,
                              Execution.output_files,
                              Execution.latest)

        return list(q.order_by(sorting_column).all())
 
execution_dao = ExecutionDAO()

execution = api.model('Execution', {
    'execution_id': fields.Integer(readonly=True, description='The execution unique identifier'), 
    'worker_id': fields.Integer(required=True, description='A worker unique identifier'),
    'task_id': fields.Integer(required=True, description='A task unique identifier'),
    'status': fields.String(readonly=True,
        description=f'The execution status: {", ".join(ExecutionDAO.authorized_status)}'), 
    'return_code': fields.Integer(required=False, description='The return code of the execution (when finished)'),
    'pid': fields.String(required=False, description='The process id (pid) of the execution'),
    'creation_date': fields.DateTime(readonly=True,
        description="timestamp of execution creation (on worker)"),
    'modification_date': fields.DateTime(readonly=True,
        description="timestamp of execution last modification"),
    'output': fields.String(readonly=True, description='The standard output of the execution'),
    'error': fields.String(readonly=True, description='The standard error of the execution (if any)'),
    'output_files': fields.String(readonly=True, description='A list of output files transmitted (if any)'),
    'command': fields.String(required=False, description='The command that was really launched for this execution (it case Task.execution is modified)'),
    'latest': fields.Boolean(readonly=True, description='Latest or current execution for the related task')
})


@ns.route("/<id>/executions")
@ns.param("id", "The worker identifier")
@ns.response(404, "Worker not found")
class WorkerExecutionObject(Resource):
    @ns.doc("get_worker_executions")
    @ns.marshal_list_with(execution)
    def get(self, id):
        """Fetch a worker executions given the worker identifier"""
        #worker_dao.update_contact(id)
        return execution_dao.list(worker_id=id, no_output=True)


@ns.route("/<id>/executions/<status>")
@ns.param("id", "The worker identifier")
@ns.param("status", "Filter only executions with this status")
@ns.response(404, "Worker not found")
class WorkerExecutionFilterObject(Resource):
    @ns.doc("get_worker_executions")
    @ns.marshal_list_with(execution)
    def get(self, id, status):
        """Fetch a worker executions given the worker identifier and the executions status"""
        #worker_dao.update_contact(id)
        return execution_dao.list(worker_id=id, status=status)

signal = api.model('Signal', {
    'execution_id': fields.Integer(readonly=True, description='The execution unique identifier'), 
    'worker_id': fields.Integer(readonly=True, description='A worker unique identifier'),
    'signal': fields.Integer(readonly=True, description='The signal to send to the execution (UNIX signal)'),
})

signal_parser = api.parser()
signal_parser.add_argument('execution_id', type=int, help='Execution identifier', location='json')
signal_parser.add_argument('signal', type=int, help='Signal to send', location='json')

@ns.route("/<id>/signals")
@ns.param("id", "The worker identifier")
@ns.response(404, "Worker not found")
class WorkerSignal(Resource):
    @ns.doc("get_worker_signals")
    @ns.marshal_list_with(signal)
    def get(self, id):
        """Fetch a worker executions given the worker identifier and the executions status"""
        signals = list(Signal.query.filter(Signal.worker_id==id))
        for sig in signals:
            db.session.delete(sig)
        db.session.commit()
        return signals
    
    @ns.doc("create_worker_signal")
    @ns.expect(signal_parser)
    def post(self, id):
        """Create a signal for the given worker about a certain execution with a certain signal"""
        args = signal_parser.parse_args()
        db.session.add(Signal(args['execution_id'], id, args['signal']))
        db.session.commit()


ns = api.namespace('executions', description='EXECUTION operations')

execution_filter = api.model('ExecutionFilter', {
    'task_id': fields.Integer(required=False,decription='A list of ids to restrict listing'),
    'status': fields.String(required=False, description="Filter with this status"),
    'latest': fields.Boolean(required=False, decription="Filter only for latest execution")
})
@ns.route('/')
class ExecutionList(Resource):
    '''Shows a list of all executions, and lets you POST to add new workers'''
    @ns.doc('list_executions')
    @ns.expect(execution_filter)
    @ns.marshal_list_with(execution)
    def get(self):
        '''List all executions'''
        return execution_dao.list(**api.payload) if api.payload else execution_dao.list()

    @ns.doc('create_execution')
    @ns.expect(execution)
    @ns.marshal_with(execution, code=201)
    def post(self):
        '''Create a new execution'''
        return execution_dao.create(api.payload), 201
    

@ns.route("/<id>")
@ns.param("id", "The execution identifier")
@ns.response(404, "Execution not found")
class ExecutionObject(Resource):
    @ns.doc("get_execution")
    @ns.marshal_with(execution)
    def get(self, id):
        """Fetch a execution given its identifier"""
        return execution_dao.get(id)

    @ns.doc("update_execution")
    @ns.expect(execution)
    @ns.marshal_with(execution, code=201)
    def put(self, id):
        """Update an execution"""
        return execution_dao.update(id, api.payload)


parser = api.parser()
parser.add_argument('text', type=str, help='Supplementary text', location='json')

@ns.route("/<id>/delete")
@ns.param("id", "The execution identifier")
@ns.response(404, "Execution not found")
class ExecutionObject(Resource):
    @ns.doc('delete_execution')
    def put(self,id):
        '''Delete an execution for this id'''
        for e in Execution.query.filter(Execution.execution_id==id):
            db.session.delete(e)
        db.session.commit()
        return {'result':'ok'}

@ns.route("/<id>/output")
@ns.param("id", "The execution identifier")
@ns.response(404, "Execution not found")
class ExecutionOutput(Resource):
    @ns.doc("update_execution_output")
    @ns.expect(parser)
    def put(self, id):
        """Add some data to the execution output"""
        x = execution_dao.get(id)
        args = parser.parse_args()
        execution_dao.update(id, 
            {'output':('' if x.output is None else x.output) + args['text']})
        return {'result':'Ok'}

@ns.route("/<id>/error")
@ns.param("id", "The execution identifier")
@ns.response(404, "Execution not found")
class ExecutionOutput(Resource):
    @ns.doc("update_execution_error")
    @ns.expect(parser)
    def put(self, id):
        """Add some data to execution error"""
        x = execution_dao.get(id)
        args = parser.parse_args()
        execution_dao.update(id, 
            {'error':('' if x.error is None else x.error) + args['text']})
        return {'result':'Ok'}

@ns.route("/<id>/output_files")
@ns.param("id", "The execution identifier")
@ns.response(404, "Execution not found")
class ExecutionOutputFiles(Resource):
    @ns.doc("update_execution_output")
    @ns.expect(parser)
    def put(self, id):
        """Update output files (files transferred from /output, i.e. results) for execution as a space separated file URL list"""
        args = parser.parse_args()
        execution_dao.update(id, 
            {'output_files':args['text']})
        return {'result':'Ok'}


ns = api.namespace('batch', description='BATCH level operations')

batch_parser = api.parser()
batch_parser.add_argument('signal', type=int, help='Optionnaly send signal to all running tasks', 
    required=False, location='json')


custom_batch = api.model('Batch', {
    'batch': fields.String(readonly=True, description='The name of the batch'), 
    'pending': fields.Integer(readonly=True,
        description='The number of task in pending state'), 
    'accepted': fields.Integer(readonly=True,
        description='The number of task in accepted state'), 
    'running': fields.Integer(readonly=True,
        description='The number of task in running state'), 
    'failed': fields.Integer(readonly=True,
        description='The number of task in succeeded state'), 
    'succeeded': fields.Integer(readonly=True,
        description='The number of task in failed state'), 
    'workers': fields.String(readonly=True, description='The workers used in that batch'),
})

@ns.route("/")
class BatchList(Resource):
    @ns.doc("list_batch")
    @ns.marshal_list_with(custom_batch)
    def get(self):
        """List the batches, their task statuses and workers"""
        if isinstance(db.session.bind.dialect, sqlite.dialect):
            worker_query='''SELECT batch,GROUP_CONCAT(name,',') FROM worker GROUP BY batch'''
        else:
            worker_query='''SELECT batch,STRING_AGG(name,',') FROM worker GROUP BY batch'''
        batch_query='''SELECT batch,status,count(task_id) FROM task GROUP BY batch,status ORDER BY batch,status'''
        batches = []
        batches_attributes = {}
        for batch,status,count in db.session.execute(batch_query):
            if batch not in batches:
                batches.append(batch)
                batches_attributes[batch]={'batch':batch}    
            batches_attributes[batch][status]=count
        for batch,workers in db.session.execute(worker_query):
            if batch in batches_attributes:
                batches_attributes[batch]['workers']=workers
        return [batches_attributes[batch] for batch in batches]
@ns.route("/<name>/stop")
@ns.param("name", "The batch name")
@ns.response(404, "Batch not found")
class BatchStop(Resource):
    @ns.doc("stop_a_batch")
    @ns.expect(batch_parser)
    def put(self, name):
        """Pause all workers for this batch - and kill current job if force is set"""
        if name=='Default':
            for w in Worker.query.filter(Worker.batch.is_(None)):
                w.status = 'paused'
        else:
            for w in Worker.query.filter(Worker.batch==name):
                w.status = 'paused'
        args = batch_parser.parse_args()
        if args.get('signal',False):
            log.warning(f'Sending signal {args["signal"]} to executions for batch {name}')
            if name=='Default':
                for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                                Execution.status=='running',
                                                Task.batch.is_(None))):
                    log.warning(f'Sending signal {args["signal"]} to execution {e.execution_id}')
                    db.session.add(Signal(e.execution_id, e.worker_id, args['signal']))
            else:
                for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                                Execution.status=='running',
                                                Task.batch==name)):
                    log.warning(f'Sending signal {args["signal"]} to execution {e.execution_id}')
                    db.session.add(Signal(e.execution_id, e.worker_id, args['signal']))
        db.session.commit()
        return {'result':'Ok'}

@ns.route("/<name>/go")
@ns.param("name", "The batch name")
@ns.response(404, "Batch not found")
class BatchGo(Resource):
    @ns.doc("_re_launch_a_batch")
    @ns.expect(batch_parser)
    def put(self, name):
        """(re)set all workers affected to this batch to running"""
        if name=='Default':
            for w in Worker.query.filter(Worker.batch.is_(None)):
                w.status = 'running'
        else:
            for w in Worker.query.filter(Worker.batch==name):
                w.status = 'running'
        args = batch_parser.parse_args()
        if args.get('signal',False):
            log.warning(f'Sending signal {args["signal"]} to executions for batch {name}')
            if name=='Default':
                for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                                Execution.status=='running',
                                                Task.batch.is_(None))):
                    log.warning(f'Sending signal {args["signal"]} to execution {e.execution_id}')
                    db.session.add(Signal(e.execution_id, e.worker_id, args['signal']))
            else:
                for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                                Execution.status=='running',
                                                Task.batch==name)):
                    log.warning(f'Sending signal {args["signal"]} to execution {e.execution_id}')
                    db.session.add(Signal(e.execution_id, e.worker_id, args['signal']))
        db.session.commit()
        return {'result':'Ok'}

@ns.route("/<name>")
@ns.param("name", "The batch name")
@ns.response(404, "Batch not found")
class BatchDelete(Resource):
    @ns.doc("delete_a_batch")
    def delete(self, name):
        """Delete all tasks and executions for this batch"""
        if name=='Default':
            log.warning('Deleting default batch')
            db.session.execute(delete(Execution).where(Execution.task_id.in_(
                select(Task.task_id).where(Task.batch.is_(None)))), 
                execution_options={'synchronize_session':False})
            db.session.execute(delete(Task).where(Task.batch.is_(None)))
        else:
            log.warning(f'Deleting batch {name}')
            db.session.execute(delete(Execution).where(Execution.task_id.in_(
                select(Task.task_id).where(Task.batch==name))), 
                execution_options={'synchronize_session':False})
            db.session.execute(delete(Task).where(Task.batch==name))
        db.session.commit()
        return {'result':'Ok'}



#     # ### 
#     #  #  
#     #  #  
#     #  #  
#     #  #  
#     #  #  
 #####  ### 


package_version = package_version()
@app.route('/ui/')
def ui(name=None):
    return render_template('ui.html', name=name, package_version=package_version)
@app.route('/ui/task/')
def task():
    return render_template('task.html',package_version=package_version)

@app.route('/ui/batch/')
def batch():
    return render_template('batch.html', package_version=package_version)



@app.route('/ui/get/')
def handle_get():
    json = request.args
    if 'delay' in json:
        sleep(int(json['delay']))
    if json['object']=='workers':
        log.info('sending workers')
        return jsonify({
            'workers':list([tryupdate(dict(row),'stats',json_module.loads,row.stats) for row in db.session.execute(
                '''SELECT 
                    worker_id,
                    name, 
                    batch,
                    status, 
                    concurrency,
                    prefetch,
                    (SELECT count(execution_id) FROM execution WHERE execution.worker_id=worker.worker_id AND
                                                                        execution.status='accepted') as accepted,
                    (SELECT count(execution_id) FROM execution WHERE execution.worker_id=worker.worker_id AND 
                                                                        execution.status='running') as running,
                    (SELECT count(execution_id) FROM execution WHERE execution.worker_id=worker.worker_id AND 
                                                                        execution.status='succeeded') as succeeded,
                    (SELECT count(execution_id) FROM execution WHERE execution.worker_id=worker.worker_id AND 
                                                                        execution.status='failed') as failed,
                    (SELECT count(execution_id) FROM execution WHERE execution.worker_id=worker.worker_id) as total,
                    load,
                    memory,
                    stats
                FROM worker
                ORDER BY worker.batch,worker.name''')]),
            'totals': next(iter([dict(row) for row in db.session.execute(
                '''SELECT
                    (SELECT count(task_id) FROM task WHERE status='pending') as pending,
                    (SELECT count(task_id) FROM task WHERE status IN ('assigned','accepted')) as assigned,
                    (SELECT count(task_id) FROM task WHERE status='running') as running,
                    (SELECT count(task_id) FROM task WHERE status='failed') as failed,
                    (SELECT count(task_id) FROM task WHERE status='succeeded') as succeeded
                '''
            )])) })

    elif json['object']=='tasks':
        order_by = json.get('order_by', None)
        filter_by = json.get('filter_by', None)
        worker = json.get('worker', None)

        log.warning(f"sending task ordered by {order_by} filtered by {filter_by} for worker {worker}")


        if order_by=='worker':
            sort_clause='ORDER BY worker.name, task.task_id DESC'
        elif order_by=='batch':
            sort_clause='ORDER BY task.batch, task.task_id DESC'
        else:
            sort_clause='ORDER BY task.task_id DESC'
        
        where_clauses = []

        if filter_by=='terminated':
            where_clauses.append("execution.status IN ('succeeded','failed')")
        elif filter_by:
            where_clauses.append(f"execution.status='{filter_by}'")

        if worker is not None:
            try:
                worker=int(worker)
                where_clauses.append(f"execution.worker_id={worker}")
            except:
                log.error(f'task filtering with worker is not possible: {worker} is not a valid id')

        where_clause = f'''WHERE {' AND '.join(where_clauses)}''' if where_clauses else ''

        if IS_SQLITE:
            trunc_output=f'SUBSTR(execution.output,-{UI_OUTPUT_TRUNC},{UI_OUTPUT_TRUNC})'
            trunc_error=f'SUBSTR(execution.error,-{UI_OUTPUT_TRUNC},{UI_OUTPUT_TRUNC})'
        else:
            trunc_output=f'RIGHT(execution.output,{UI_OUTPUT_TRUNC})'
            trunc_error=f'RIGHT(execution.error,{UI_OUTPUT_TRUNC})'
        

        #task_list = list([list(map(lambda x : str(x) if type(x)==type(datetime.utcnow()) else x ,row)) for row in db.session.execute(
        task_list = list([dict(row) for row in db.session.execute(
        f'''SELECT
        task.task_id,
        task.name,
        worker.name as worker_name,
        task.batch,
        execution.creation_date,
        execution.modification_date,
        execution.execution_id,
        {trunc_output} as output,
        {trunc_error} as error,
        task.command,
        execution.worker_id,
        task.status
        FROM task 
        LEFT JOIN execution ON (task.task_id=execution.task_id AND latest)
        LEFT JOIN worker ON execution.worker_id=worker.worker_id 
        {where_clause}
        {sort_clause}
        LIMIT {UI_MAX_DISPLAYED_ROW}
        '''
        )])
        
        detailed_tasks = json.getlist('detailed_tasks[]')
        if detailed_tasks:
            log.warning(f"detailing tasks {detailed_tasks}")
            for detailed_task in db.session.execute(f"""
                SELECT execution_id,output,error FROM execution 
                WHERE execution_id IN ({','.join([str(eid) for eid in detailed_tasks])})"""):
                for task in task_list:
                    if task['execution_id']==detailed_task['execution_id']:
                        task['output']=detailed_task['output']
                        task['error']=detailed_task['error']
                        break

        return jsonify({'tasks':task_list})
        
    elif json['object'] == 'batch':
        log.info('sending batch')
        if IS_SQLITE:
            duration_query='(JULIANDAY(e1.modification_date)-JULIANDAY(e1.creation_date))*24'
            worker_query='''SELECT batch,GROUP_CONCAT(name,',') as workers FROM worker GROUP BY batch ORDER BY name'''
        else:
            duration_query='EXTRACT ( EPOCH FROM (e1.modification_date-e1.creation_date)/3600 )'
            worker_query='''SELECT batch,STRING_AGG(name,',') as workers FROM (SELECT * FROM worker ORDER BY name) w GROUP BY batch'''
        batch_query=f'''SELECT * FROM (
    SELECT batch,status,COUNT(task_id) as count,MAX(duration) as max,MIN(duration) as min, AVG(duration) as avg FROM (
        SELECT {duration_query} as duration, e1.task_id, e1.status,task.batch FROM execution e1 JOIN task ON (
            task.task_id=e1.task_id AND e1.latest
        )
    ) AS e2 GROUP BY batch,status
    UNION	 
    SELECT batch,status, COUNT(task_id),NULL,NULL,NULL 
    FROM task WHERE task_id NOT IN (SELECT task_id FROM execution) GROUP BY batch,status
) AS b ORDER BY batch, status'''
        return jsonify({'batches':list([dict(row) for row in db.session.execute(batch_query)]),
                        'workers': list([dict(row) for row in db.session.execute(worker_query)])})

#@socketio.on('change_batch')
@app.route('/ui/change_batch')
def handle_change_batch():
    json = request.args
    Worker.query.filter(Worker.worker_id==json['worker_id']).update(
        {Worker.batch:json['batch_name'] or None})
    db.session.commit()
    return '"ok"'


#@socketio.on('concurrency_change')
@app.route('/ui/concurrency_change')
def handle_concurrency_change():
    json = request.args
    worker_id = json['id']
    change = json['change']
    log.info(f'changing concurrency for worker {worker_id}: {change}')
    if isinstance(db.session.bind.dialect, sqlite.dialect):
        log.info('Using sqlite SQL')
        Worker.query.filter(Worker.worker_id==worker_id).update(
            {Worker.concurrency: func.max(Worker.concurrency+change,0)})
    else:
        log.info('Using standard SQL')
        Worker.query.filter(Worker.worker_id==worker_id).update(
            {Worker.concurrency: func.greatest(Worker.concurrency+change,0)})
    db.session.commit()
    return '"ok"'

#@socketio.on('prefetch_change')
@app.route('/ui/prefetch_change')
def handle_prefetch_change():
    json = request.args
    worker_id = json['id']
    change = json['change']
    log.info(f'changing prefetch for worker {worker_id}: {change}')
    if isinstance(db.session.bind.dialect, sqlite.dialect):
        log.info('Using sqlite SQL')
        Worker.query.filter(Worker.worker_id==worker_id).update(
            {Worker.prefetch: func.max(Worker.prefetch+change,0)})
    else:
        log.info('Using standard SQL')
        Worker.query.filter(Worker.worker_id==worker_id).update(
            {Worker.prefetch: func.greatest(Worker.prefetch+change,0)})
    db.session.commit()
    return '"ok"'

@app.route('/ui/pause_unpause_worker')
def handle_pause_unpause_worker():
    json = request.args
    worker_id = json['id']
    status = json['status']
    Worker.query.filter(Worker.worker_id==worker_id).update({Worker.status:status})
    log.info(f'changing status for worker {worker_id}: {status}')
    db.session.commit()
    return '"ok"'


@app.route('/ui/clean_worker')
def handle_clean_worker():
    json = request.args
    worker_id = json['worker_id']
    db.session.add(Signal(execution_id=None, worker_id=worker_id, signal=SIGNAL_CLEAN))
    db.session.commit()
    log.info(f'sending clean signal for worker {worker_id}')
    return '"ok"'

@app.route('/ui/restart_worker')
def handle_restart_worker():
    json = request.args
    worker_id = json['worker_id']
    db.session.add(Signal(execution_id=None, worker_id=worker_id, signal=SIGNAL_RESTART))
    db.session.commit()
    log.info(f'sending restart signal for worker {worker_id}')
    return '"ok"'

#@socketio.on('create_worker')
@app.route('/ui/create_worker')
def handle_create_worker():
    json = request.args
    concurrency = int(json['concurrency'])
    flavor = json['flavor']
    if not flavor:
        return jsonify(error='Flavor must be specified')
        #return None
    region = json['region']
    provider = json['provider']
    if not region:
        return jsonify(error='Region must be specified')
        #return None
    batch = json['batch'] or None
    prefetch = int(json['prefetch'])
    number = int(json['number'])
    for _ in range(number):
        db.session.add(
            Job(target='', 
                action='worker_create', 
                args={
                    'concurrency': concurrency, 
                    'prefetch':prefetch,
                    'flavor':flavor,
                    'region':region,
                    'provider': provider,
                    'batch':batch
                }
            )
        )
    db.session.commit()
    return '"ok"'

#@socketio.on('batch_action')
@app.route('/ui/batch/action')
def handle_batch_action():
    """Gathering all the action dealing with batch like pause, break, stop, clear, go."""
    json = request.args
    if json['action'] in ['stop','break','pause','simple pause','pause only batch']:
        #Same function as in the API set all workers affected to this batch to running and can also interrupt the running tasks with signal 3 and 9
        name=json['name']
        if name=='Default':
            name=None
        for w in Worker.query.filter(Worker.batch==name):
                w.status = 'paused'
        if json['action']=='break':
            signal = 9
        elif json['action']=='stop':
            signal = 3
        elif json['action']=='simple pause':
            signal = 0
        elif json['action']=='pause':
            #TODO: make a more efficient query
            for t in Task.query.filter(and_(
                        Task.batch==name,
                        Task.status.in_(['running','accepted']))):
                t.status = 'paused'
            signal = 20
            db.session.commit()
        log.warning(f'Sending signal {signal} to executions for batch {name}')
        for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                        Execution.status=='running',
                                        Task.batch==name)):
            log.warning(f'Sending signal {signal} to execution {e.execution_id}')
            db.session.add(Signal(e.execution_id, e.worker_id, signal ))
        db.session.commit()
        log.warning('result pause :Ok')
    elif json['action'] in ['go','simple go']: 
        #Same function as in the API (re)set all workers affected to this batch to running
        name=json['name']
        """(re)set all workers affected to this batch to running"""
        for w in Worker.query.filter(Worker.batch==name):
            w.status = 'running'
        if json['action']=='go':
            signal=18
            for t in Task.query.filter(Task.batch==name):
                if t.status == 'paused':
                    t.status='running'
            for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                            Execution.status=='running',
                                            Task.batch==name)):
                log.warning(f'Sending signal {signal} to execution {e.execution_id}')
                db.session.add(Signal(e.execution_id, e.worker_id, signal ))
        db.session.commit()
        log.warning('result go : Ok')
    elif json['action']=='clear':
        #Same function as in the API clear() Delete all tasks and executions for this batch
        name=json['name']
        """Delete all tasks and executions for this batch"""
        # execution are deleted by cascade
        if name=='Default':
            name=None
        for t in Task.query.filter(Task.batch==name):
            db.session.delete(t)
        db.session.commit()
        log.warning(f'result clear batch {name}: Ok ')
    return '"ok"'

#@socketio.on('task_action')
@app.route('/ui/task/action')
def handle_task_action():
    """Gathering all the action dealing with task like break, stop, delete, modify, restart"""
    #The code essentially is from the API code with a few modifications
    json = request.args
    task=json['task_id']
    if json['action'] in ['break','stop','pause','resume']: 
        #A signal 3 or 9 is created and causes only the interruption of the task with id same structure as in the API 
        task=json['task_id']
        for t in Task.query.filter(Task.task_id==task):
            if json['action'] == 'break':
                type='break'
                signal = 9
            elif json['action'] == 'stop':
                signal = 3
                type='stop'
            elif json['action'] == 'pause':
                signal = 20
                type='pause'
                t.status='paused'
            elif json['action'] == 'resume':
                signal = 18
                type='resume'
                t.status='running'
            log.warning(f'Sending signal {signal} to executions for task {task}')
            for e in db.session.scalars(select(Execution).join(Execution.task).where(
                                            Execution.status=='running',
                                            Task.task_id==task)):
                log.warning(f'Sending signal {signal} to execution {e.execution_id}')
                db.session.add(Signal(e.execution_id, e.worker_id, signal ))
        db.session.commit()
        log.warning(f'result {type} : Ok')
    elif json['action']=='delete': 
        #Delete the task in the data base
        for t in Task.query.filter(Task.task_id==task):
            db.session.delete(t)
        db.session.commit()
        log.warning('result delete: Ok')
    elif json['action']=='modify': 
        #Changing the command for a task in the data base and moving it in the task queue. It doesn't create a new task.
        for t in Task.query.filter(Task.task_id==task):
            t.command =json["modification"]
            t.status='pending'
        db.session.commit()
        log.warning('result modify : Ok')
    elif json['action']=='restart': 
        #Relaunching the execution of a task.
        for t in Task.query.filter(Task.task_id==task):
            t.status='pending'
        db.session.commit()
        log.warning('result restart : Ok')
    return '"ok"'

#@socketio.on('delete_worker') #Delete a worker.
@app.route('/ui/delete_worker')
def delete_worker():
    """Delete a worker in db"""
    json = request.args
    worker_dao.delete(json['worker_id'], session=db.session)
    return '"ok"'
    

#@socketio.on('jobs')
@app.route('/ui/jobs')
def handle_jobs():
    """Provide UI with job list"""
    return jsonify(jobs = [to_dict(job) for job in db.session.query(Job).order_by(Job.job_id.desc()).all()])

@app.route('/ui/delete_job')
def delete_job():
    """Delete a job in db"""
    json = request.args
    job = db.session.query(Job).get(json['job_id'])
    if job:
        db.session.delete(job)
        db.session.commit()
    else:
        log.warning(f"Job {json['job_id']} already deleted")
    return '"ok"'

@app.route('/ui/delete_jobs')
def delete_jobs():
    """Delete terminated jobs"""
    if db.session.execute(
            select(func.count()).select_from(Job).where(Job.status=='succeeded')
            ).scalar_one()>0:
        log.warning('Here')
        db.session.execute(delete(Job).where(Job.status=='succeeded'))
    elif db.session.execute(
            select(func.count()).select_from(Job).where(Job.status=='failed')
            ).scalar_one()>0:
        log.warning('There')
        db.session.execute(delete(Job).where(Job.status=='failed'))
    elif db.session.execute(
            select(func.count()).select_from(Job).where(Job.status=='pending')
            ).scalar_one()>0:
        db.session.execute(delete(Job).where(Job.status=='pending'))
    else:
        return '"nothing to do"'
    db.session.commit()
    return '"ok"'

@app.route('/ui/restart_job')
def restart_job():
    """Restart a job in db"""
    json = request.args
    job = db.session.query(Job).get(json['job_id'])
    if job:
        job.status = 'pending'
        job.retry = 0
        db.session.commit()
    else:
        log.warning(f"Job {json['job_id']} already deleted")
    return '"ok"'

#ns = api.namespace('live', description='Very basic API for the UI')

@app.route('/live/ping')
def live_ping():
    """Simply return ok"""
    return '"ok"'

 #####     ##     ####   #    #   ####   #####    ####   #    #  #####       #####  #    #  #####   ######    ##    #####  
 #    #   #  #   #    #  #   #   #    #  #    #  #    #  #    #  #    #        #    #    #  #    #  #        #  #   #    # 
 #####   #    #  #       ####    #       #    #  #    #  #    #  #    #        #    ######  #    #  #####   #    #  #    # 
 #    #  ######  #       #  #    #  ###  #####   #    #  #    #  #    #        #    #    #  #####   #       ######  #    # 
 #    #  #    #  #    #  #   #   #    #  #   #   #    #  #    #  #    #        #    #    #  #   #   #       #    #  #    # 
 #####   #    #   ####   #    #   ####   #    #   ####    ####   #####         #    #    #  #    #  ######  #    #  #####  


def get_nodename(session):
    worker_names = list(map(lambda x: x[0], 
        session.execute(select(Worker.name))))
    log.warning(f'Worker names: {worker_names}')
    i=1
    while f'node{i}' in worker_names:
        i+=1
    return f'node{i}'


def create_worker_object(concurrency, flavor, region, provider, batch, prefetch, db_session):
    """Create a worker object in db - this must be called linearly not in async way
    """
    hostname = get_nodename(db_session)
    idle_callback = WORKER_IDLE_CALLBACK.format(hostname=hostname)
    log.info(f'Creating a new worker {hostname}: concurrency:{concurrency}, \
flavor:{flavor}, region:{region}, provider:{provider}, prefetch:{prefetch}')
    w = Worker(name=hostname, hostname=hostname, concurrency=concurrency, status='offline', 
            batch=batch, idle_callback=idle_callback, prefetch=prefetch)
    db_session.add(w)
    db_session.commit()
    return w
    

def background():
    # while some tasks are pending without executions:
    #   look for a running worker:
    #      create a pending execution of this task for this worker


    with app.app_context():
        session = Session(db.engine)
    worker_process_queue = {}
    other_process_queue = []
    log.info('Starting thread for {}'.format(os.getpid()))
    ansible_workers = list(session.query(Worker).filter(and_(
                    Worker.status=='running',
                    Worker.idle_callback.is_not(None))).with_entities(
                        Worker.hostname))
    if ansible_workers:
        log.warning(f'Making sure workers {",".join([w.hostname for w in ansible_workers])} has access to server')
        process = PropagatingThread(
                    target=run,
                    args = (SERVER_CRASH_WORKER_RECOVERY,),
                    kwargs= {'shell': True, 'check':True}
                )
        other_process_queue.append(('Worker access task',process))
        process.start()

    while True:
        log.warning('Starting main loop')
        try:
            task_list = list(session.query(Task).filter(
                    Task.status=='pending').with_entities(Task.task_id, Task.batch))
            if task_list:
                task_attributions = False
                worker_list = list(session.query(Worker).filter(
                            Worker.status=='running').with_entities(
                            Worker.worker_id,Worker.batch,Worker.concurrency,Worker.prefetch))
                execution_per_worker = {worker_id: count for worker_id,count in 
                                session.query(Execution.worker_id,func.count(Execution.task_id)).filter(and_(
                                    Execution.worker_id.in_(list([w.worker_id for w in worker_list])),
                                    Execution.status.in_(['running','pending','accepted']))
                                ).group_by(
                                    Execution.worker_id
                                )
                }
                
                for task in task_list:
                    for worker in worker_list:
                        if worker.batch != task.batch:
                            continue
                        if execution_per_worker.get(worker.worker_id,0)<(worker.concurrency+worker.prefetch):
                            session.add(Execution(worker_id=worker.worker_id,
                                task_id=task.task_id))
                            session.query(Task).filter(Task.task_id==task.task_id).update(
                                {'status':'assigned'}
                            )
                            execution_per_worker[worker.worker_id] = execution_per_worker.get(worker.worker_id,0)+1
                            log.info(f'Execution of task {task.task_id} proposed to worker {worker.worker_id}')
                            task_attributions = True
                            break
                if task_attributions:
                    session.commit()
            now = datetime.utcnow()
            log.warning('Looking for offline/online workers')
            session.expire_all()
            for worker in session.query(Worker).filter(Worker.status.in_(['offline','running'])):
                change = False
                log.warning(f'Assessing worker {worker.name}')
                if worker.last_contact_date is None or (
                            now - worker.last_contact_date
                        ).total_seconds() > WORKER_OFFLINE_DELAY:
                    log.warning(f'... late: {worker.last_contact_date}')
                    if worker.status=='running':
                        log.warning(f'Worker {worker.name} ({worker.worker_id}) lost, marked as offline')
                        worker.status = 'offline'
                        change = True
                else:
                    log.warning('... good')
                    if worker.status=='offline':
                        log.warning(f'Worker {worker.name} ({worker.worker_id}) recovered, marked as running')
                        worker.status = 'running'
                        change = True
                if change:
                    session.commit()
            
            change = False
            for job in list(session.query(Job).filter(Job.status == 'pending')):

                if job.action == 'worker_destroy':
                    change=True
                    if ('create',job.target) in worker_process_queue:
                        worker,worker_create_process,job_id = worker_process_queue[('create',job.target)]
                        if worker_create_process.poll() is None:
                            worker_create_process.terminate()
                            log.warning(f'Worker {job.target} creation process has been terminated')
                            del(worker_process_queue[('create',job.target)])
                            session.query(Job).get(job_id).status='failed'
                    worker = Namespace(**job.args)
                    host_exist_in_ansible = bool(json_module.loads(scitq_inventory(host=job.target)))
                    if host_exist_in_ansible:
                        if len(worker_process_queue)<WORKER_CREATE_CONCURRENCY:
                            log.warning(f'Launching destroy process for {job.target}, command is "{worker.idle_callback}"')
                            worker_delete_process = Popen(
                                    worker.idle_callback,
                                    stdout = PIPE,
                                    stderr = PIPE,
                                    shell = True,
                                    encoding = 'utf-8'
                                )
                            job.status='running'
                            worker_process_queue[('destroy',job.target)]=(worker, worker_delete_process, job.job_id)
                            log.warning(f'Worker {job.target} destruction process has been launched')
                    else:
                        log.warning(f'Deleting worker {worker.name} ({worker.worker_id})')
                        real_worker = session.query(Worker).get(worker.worker_id)
                        if real_worker is not None:
                            change = True
                            session.delete(real_worker)
                            job.status='succeeded'
                
                if job.action == 'worker_create':
                    change = True
                    worker = create_worker_object(db_session=session,
                        **job.args)
                    job.action = 'worker_deploy'
                    job.target = worker.name
                    job.args = dict(job.args)
                    job.args['worker_id'] = worker.worker_id
                    job.retry = WORKER_CREATE_RETRY
                    job.status = 'pending'
                
                if job.action == 'worker_deploy':
                    if job.target not in worker_process_queue and len(
                                worker_process_queue)<WORKER_CREATE_CONCURRENCY:
                        if ('destroy',job.target) in worker_process_queue:
                            log.warning(f'Trying to recreate worker {job.target} after destruction too soon, waiting a little bit...')
                            continue
                        change = True
                        log.warning(f'Launching creation process for worker {job.target}.')
                        worker = Namespace(**job.args)
                        log.warning(f'Launching command is "'+WORKER_CREATE.format(
                                hostname=job.target,
                                concurrency=worker.concurrency,
                                flavor=worker.flavor,
                                region=worker.region,
                                provider=worker.provider,
                            )+'"')
                        worker_create_process = Popen(
                            WORKER_CREATE.format(
                                hostname=job.target,
                                concurrency=worker.concurrency,
                                flavor=worker.flavor,
                                region=worker.region,
                                provider=worker.provider
                            ),
                            stdout = PIPE,
                            stderr = PIPE,
                            shell = True,
                            encoding = 'utf-8'
                        )
                        worker.name = worker.hostname = job.target
                        job.status = 'running'
                        worker_process_queue[('create',job.target)]=(worker, worker_create_process, job.job_id)
                        log.warning(f'Worker {job.target} creation process has been launched')

            if change:
                session.commit()                

            change = False
            for ((action,worker_name),(worker,worker_process,job_id)) in list(worker_process_queue.items()):
                returncode = worker_process.poll()
                if returncode is not None:
                    change = True
                    job = session.query(Job).get(job_id)
                    del(worker_process_queue[(action,worker_name)])
                    if returncode == 0:
                        log.warning(f'Process {action} succeeded for worker {worker.name}.')
                        job.log = worker_process.stdout.read()
                        job.status = 'succeeded'

                        if action=='destroy':
                            #session.execute(Worker.__table__.delete().where(
                            #    Worker.__table__.c.worker_id==worker.worker_id))
                            log.warning(f'Deleting worker {worker.name} ({worker.worker_id})')
                            real_worker = session.query(Worker).get(worker.worker_id)
                            if real_worker is not None:
                                session.delete(real_worker)
                            else:
                                log.error(f'Could not find a worker with worker_id {worker.worker_id}')
                            #worker_dao.delete(worker.worker_id, is_destroyed=True)
                    else:
                        stderr = worker_process.stderr.read()
                        log.warning(f'Process {action} failed for worker {worker.name}: {stderr}')
                        job.log = worker_process.stdout.read() + stderr
                        log.warning(f'Job output is {job.log}')
                        if job.retry > 0:
                            job.retry -= 1
                            job.status = 'pending'
                        else:
                            job.status = 'failed'
                            if action=='create':
                                worker = session.query(Worker).get(job.args['worker_id'])
                                worker.status = 'failed'

            for job in list(session.query(Job).filter(Job.status == 'running')):
                if job.action=='worker_deploy':
                    action='create'
                elif job.action=='worker_destroy':
                    action='destroy'
                else:
                    action=job.action
                if (action, job.target) not in worker_process_queue:
                    log.warning(f'Job {(job.action, job.target)} seems to have failed, not in {worker_process_queue}')
                    job.status='failed'
                    change = True

            if change:
                session.commit()
                
            for process_name, process in list(other_process_queue):
                try:
                    if not process.is_alive():
                        other_process_queue.remove((process_name, process))
                        log.warning(f'Job {process_name} is done.')
                except Exception as e:
                    log.exception(f'Job {process_name} failed: {e}')
                    other_process_queue.remove((process_name, process))

                    

            



                
        except Exception:
            log.exception('An exception occured during server main loop:')
            while True:
                sleep(MAIN_THREAD_SLEEP)
                try:
                    log.warning('Trying to reconnect...')
                    with app.app_context():
                        session = Session(db.engine)
                    break
                except Exception:
                    pass
        sleep(MAIN_THREAD_SLEEP)

if not os.environ.get('SCITQ_PRODUCTION'):
    Thread(target=background).start()


def main():
    app.run(debug=True)

if __name__ == "__main__":
    #raise RuntimeError('Do not launch directly, launch with "FLASK=scitq.server flask run"')
    #main()
    pass