from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from ..models import User, Tasks
from datetime import datetime, date, time, timedelta
from ..security import get_user

#Task class/ Clase Task
@view_defaults(renderer='../templates/home.jinja2')
class Task:
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession

    @view_config(route_name='tasks', renderer='../templates/tasks.jinja2')
    def tasks(self):

        # if no user no func/si no hay usuario no hay funcion
        # Role validation/validacion de rol
        if self.out_or_stay(): return HTTPFound(location='/error')

        next_url = self.request.route_url('admin')

        if not next_url:
            next_url = self.request.route_url('home')
        users = self.db.query(User).all()

        # Form validate
        # Validacion del formulario
        if 'form.submitted' in self.request.params:
            user_name = self.request.params['user_name']
            task_text = self.request.params['task_text']
            user = self.db.query(User).filter_by(name=user_name).first()
            task = Tasks(task=task_text,user_id=user.id,done=False, active=False)
            self.db.add(task)
            self.request.session.flash(f'You give a task to {user.name} ', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)
        tasks = self.db.query(Tasks).all()

        return {'name': 'Tasks', 'users': users, 'next_url': next_url,
                'users_tasks': tasks}


    @view_config(route_name='tasks_by_user', renderer='../templates/tasks_by_user.jinja2')
    def tasks_by_user(self):

        username = self.request.matchdict['user']
        user = self.db.query(User).filter_by(name=username).first()

        # if no user no func/si no hay usuario no hay funcion
        # Role validation/validacion de rol
        if self.out_or_stay(username=username): return HTTPFound(location='/error')

        next_url = self.request.route_url('tasks_by_user', user=username)

        if not next_url:
            next_url = self.request.route_url('home')

        # Form validate
        # Validacion del formulario
        if 'finish' in self.request.params:
            actived_at = ''
            sub_time = ''
            task_id = self.request.params['finish']
            print(f'Task id finished: {task_id}')
            date = datetime.utcnow()
            date_query = self.db.query(Tasks).filter_by(id=task_id).all()

            #########################################
            # This horrible way of manage intervals of
            # time is a "temporary" solution. str to datetime,
            # datetime to timedelta for operate in the
            # subtraction and then convert it to str
            # to store in the database.
            for c in date_query:
                actived_at = c.active_date
                sub_time = c.time_working
            time_working  = date - actived_at
            sub_time = datetime.strptime(sub_time, '%H:%M:%S.%f').time()
            sub_time = datetime.combine(date.min, sub_time) - datetime.min
            time_working += sub_time
            time_working = str(time_working)
            ##########################################

            self.db.query(Tasks).filter_by(id=task_id).update({Tasks.done: True, Tasks.finish: date, Tasks.time_working: time_working, Tasks.active: False}, synchronize_session=False)
            self.request.session.flash(f'You Finished a task $$$ ;) ', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)

        if 'active' in self.request.params:
            task_id = self.request.params['active']
            print(f'Task id active and not finished: {task_id}')
            date = datetime.utcnow()
            self.db.query(Tasks).filter_by(id=task_id).update({Tasks.done: False, Tasks.active: True, Tasks.active_date: date}, synchronize_session=False)
            self.request.session.flash(f"You ACTIVE let's do it!", queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)

        if 'pause' in self.request.params:
            task_id = self.request.params['pause']
            actived_at = ''
            sub_time = ''
            print(f'Task id finished: {task_id}')
            date = datetime.utcnow()
            date_query = self.db.query(Tasks).filter_by(id=task_id).all()

            #########################################
            # This horrible way of manage intervals of
            # time is a "temporary" solution. str to datetime,
            # datetime to timedelta for operate in the
            # subtraction and then convert it to str
            # to store in the database puuuff
            for c in date_query:
                actived_at = c.active_date
                sub_time = c.time_working
            time_working = date - actived_at
            sub_time = datetime.strptime(sub_time, '%H:%M:%S.%f').time()
            sub_time = datetime.combine(date.min, sub_time) - datetime.min
            time_working += sub_time
            time_working = str(time_working)
            ##########################################

            print(f'Task id non active and not finished(paused): {task_id}')
            self.db.query(Tasks).filter_by(id=task_id).update({Tasks.done: False, Tasks.active: False, Tasks.time_working: time_working}, synchronize_session=False)
            self.request.session.flash(f'You Puased  the task ', queue='', allow_duplicate=True)
            return  HTTPFound(location=next_url)

        tasks = self.db.query(Tasks).order_by(Tasks.date.desc()).filter_by(user_id=user.id).all()

        return {'name': 'Tasks by user', 'user':user, 'next_url': next_url,
                'user_tasks': tasks}

    # pseudodecorator
    def out_or_stay(self, username=None):

        # if no user no func/si no hay usuario no hay funcion
        if self.request.user is None: return True

        # Role or username validation/validacion de rol
        user = get_user(self.request)
        print(user.role)
        if user.role != 'admin' and username is None: return True
        if user.role == 'admin' and username is None: return False
        if user.role == 'admin' and username is not  None: return False
        if username != user.name:
            return True
        else:
            return False

