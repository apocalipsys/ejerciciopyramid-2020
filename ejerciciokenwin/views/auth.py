#This file manipulate the commits with the database
#En este archivo se hacen las consultas y otras acciones que interactua con la base de datos

from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
import re
from ..models import User


# Function to log in
# Funcion para loguearse
@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    next_url = request.route_url('welcome')
    if not next_url:
        next_url = request.route_url('home')
    message = ''
    login = ''
    # Form validate
    # Validacion del formulario
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(name=login).first()
        # User Validate
        # Validacion del usuario
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = request.session.flash('Logging error', queue='', allow_duplicate=True)

    return dict(name='Log in',
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )

#Register function
#Funcion de registro
@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    next_url = request.route_url('welcome')
    if not next_url:
        next_url = request.route_url('home')
    message = ''
    register = ''
    # Form validate and letters/numbers (regex) for the username
    # Validacion del formulario y solo se permiten letras y numeros para nombres de usuario
    if 'form.submitted' in request.params:
        register = request.params['register']
        regex_search = re.search(r'[^A-Za-z0-9]+',register)
        if regex_search is not None:
            message = request.session.flash('Only letters and numbers are permitted', queue='', allow_duplicate=True)
            return dict(name='Register',
                        message=message,
                        url=request.route_url('register'),
                        next_url=next_url,
                        register=register,
                        )
        password = request.params['password']
        role = 'guest'
        user = User(register,password,role)
        # User existis Validate and the adding
        # Validacion de existencia de usuario y agregado del mismo
        if not user.check_user(user.name,request):
            request.dbsession.add(user)
            user = request.dbsession.query(User).filter_by(name=register).first()
            headers = remember(request, user.id)
            request.session.flash('Your registration has been successful', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url, headers=headers)
        message = request.session.flash('Registration error', queue='', allow_duplicate=True)

    return dict(name='Register',
        message=message,
        url=request.route_url('register'),
        next_url=next_url,
        register=register,
    )

#Logout function
#Funcion para salir
@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('home')
    return HTTPFound(location=next_url, headers=headers)

#Forbidden view function
@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)