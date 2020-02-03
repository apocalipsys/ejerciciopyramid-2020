#This file will be necesary for the security of the app
#Este archivo sera necesario para la seguridad de la app
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import User, Tasks, BlogPosts


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id

def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user

def get_tasks(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        tasks = request.dbsession.query(Tasks).filter_by(user_id=user_id).all()
        return tasks

def get_users(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        all_users = request.dbsession.query(User).all()
        return all_users

def includeme(config):
    settings = config.get_settings()
    authn_policy = MyAuthenticationPolicy(
        settings['auth.secret'],
        hashalg='sha512',
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(get_tasks, 'tasks', reify=True)
    config.add_request_method(get_users, 'all_users', reify=True)
