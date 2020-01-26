#This file content the config views and the Views class for the renderers templates
#Este archivo contiene las configuracion devistas y la clase Views (Vistas) para los templates
# uncomment the two lines below if you want to see the logs and comment level = INFO in development.ini and uncomment level = DEBUG
# descomentar las dos lineas debajo si queres ver los logs y en development.ini comentar level = INFO y descomentar level = DEBUG
#import logging
#log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from ..models import User
from datetime import datetime
from ..security import get_user

#Greeting function time adecuate
#Funcion para saludar adecuada al horiario
def greeting():
    h = datetime.today().hour
    dayparts = {12:'Good morning',18:'Good afternoon',24:'Good night'}
    greet =[v for k,v in dayparts.items() if h < k][0]
    return greet


@view_defaults(renderer='../templates/home.jinja2')
class Views:
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession

    @view_config(route_name='delete_user', renderer='../templates/welcome.jinja2')
    def delete_user(self):
        user = self.request.matchdict['user']

        if self.request.user is None: return HTTPFound(location='/error')

        #Delete validation by role/validacion para borrar usuarios
        admin = get_user(self.request)
        if user == self.request.user.name and admin.role == 'admin':
            self.request.session.flash(f"A user can't delete him/her self", queue='', allow_duplicate=True)
            return HTTPFound(location='/error')
        try:
            if admin.role == 'admin':
                query = self.db.query(User).filter_by(name=user).one()

                self.db.delete(query)
                self.request.session.flash(f'User {user} deleted', queue='', allow_duplicate=True)
        except:
            return HTTPFound(location='/error')

        return HTTPFound(location='/admin')

    #home view/vista home
    @view_config(route_name='home', renderer='../templates/home.jinja2')
    def home(self):
        return {'name':'Home'}

    #Welcome view/vista de binvenida
    @view_config(route_name='welcome', renderer='../templates/welcome.jinja2')
    def welcome(self):
        g = greeting()
        if self.request.user.name == 'admin':
            self.request.session.flash(f'{g} You are the Administrator', queue='', allow_duplicate=True)
            return HTTPFound(location='/admin')

        return {'name':'Welcome','greeting':g}

    #Administrator view/vista administrador
    @view_config(route_name='admin', renderer='../templates/welcome.jinja2')
    def admin(self):
        users = self.db.query(User).filter_by(name=User.name).all()
        #if no user no func/si no hay usuario no hay funcion
        if self.request.user is None: return HTTPFound(location='/error')

        #Role validation/validacion de rol
        user = get_user(self.request)
        if user.role  != 'admin':
            return HTTPFound(location='/error')

        title = str(self.request.user.name).capitalize()+' Account'
        return dict(name=title, users=users)

