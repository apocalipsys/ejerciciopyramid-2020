from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from ..models import User, BlogPosts, Score, Tasks
from datetime import datetime
from ..security import get_user
import base64
import os
import shutil
from ejerciciokenwin import static_dir
import json
from pyramid import response
from http import cookies

#Views class/ Clase vistas
@view_defaults(renderer='../templates/home.jinja2')
class Views:
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession

    #Delete user view/Borrar usuario view (solo admin)
    @view_config(request_method = ['GET'], route_name='extract_json', renderer='json')
    def extract_json(self):
        user = json.dumps(self.request.user.name)
        password = json.dumps(self.request.user.password_hash)
        #user_session = json.dumps(self.request.dbsession.user)
        us = self.db.query(Score).filter_by(user_id=self.request.user.id)

        return {'name':'home view', 'user': user, 'password':password, 'user_score': [u.score for u in us]}#, 'user_session':user_session}

    @view_config(request_method = ['GET'], route_name='user_list', renderer='json')
    def user_list(self):
        #users = self.request.all_users
        users = self.db.query(User).filter_by(name=User.name).all()
        us = self.request.matchdict['user']
        if us == 'capo':
            return {'name':'junziono', 'users':[user.name for user in users]}
        return HTTPFound(location='/error')

    @view_config(request_method=['POST'], route_name='add', renderer='json')
    def add(self):
        user = self.request.matchdict['user']
        password = self.request.matchdict['password']
        register = User(name=user, password=password, role='guest')
        self.db.add(register)
        return{'name': user, 'registration':'succes'}

    @view_config(request_method=['DELETE'], route_name='del', renderer='json')
    def deluser(self):
        user = self.request.matchdict['user']
        user_to_delete = self.db.query(User).filter_by(name=user).one()
        self.db.delete(user_to_delete)
        return{'name': user,'state':'deleted!'}

    @view_config(request_method=['GET'], route_name='getcookie', renderer='json')
    def getcookie(self):
        c = cookies.SimpleCookie()
        user = self.request.user.name
        ip_remote = self.request.remote_addr
        ip_client = self.request.client_addr
        c['user'] = user
        c['clientip'] = ip_client
        c['remoteip'] = ip_remote


        return {'user': user, 'ip remote': ip_remote, 'ip client': ip_client, 'cookie':c.output()}


