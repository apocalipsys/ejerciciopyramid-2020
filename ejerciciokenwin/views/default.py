#This file content the config views and the Views class for the renderers templates
#Este archivo contiene las configuracion devistas y la clase Views (Vistas) para los templates
# uncomment the two lines below if you want to see the logs and comment level = INFO in development.ini and uncomment level = DEBUG
# descomentar las dos lineas debajo si queres ver los logs y en development.ini comentar level = INFO y descomentar level = DEBUG
#import logging
#log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from ..models import User, BlogPosts, Score, Tasks
from datetime import datetime
from ..security import get_user
import base64
import os
import shutil
from ejerciciokenwin import static_dir
from .geoloc import Localization
import pytz




#Views class/ Clase vistas
@view_defaults(renderer='../templates/home.jinja2')
class Views:
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession

    # Greeting function time adecuate
    # Funcion para saludar adecuada al horiario
    def greeting(self):
        try:
            geloc = self.request.localization
            timezone = pytz.timezone(geloc.tz)
            time_now = datetime.now()
            com = time_now.astimezone(timezone)
            h = com.hour
            dayparts = {12: 'Good morning', 18: 'Good afternoon', 24: 'Good night'}
            greet = [v for k, v in dayparts.items() if h < k][0]
            return greet, geloc
        except:
            return None, None

    #Delete user view/Borrar usuario view (solo admin)
    @view_config(route_name='delete_user', renderer='../templates/admin.jinja2')
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



    #Edit user view/Vista de edicion de usuario (only admin/solo admin)
    @view_config(route_name='edit_user', renderer='../templates/edit.jinja2')
    def edit_user(self):

        # if no user no func/si no hay usuario no hay funcion
        # Role validation/validacion de rol
        if self.out_or_stay(): return HTTPFound(location='/error')

        role = ''
        username = self.request.matchdict['user']
        next_url = self.request.route_url('admin')

        if not next_url:
            next_url = self.request.route_url('home')
        user = self.db.query(User).filter_by(name=username).first()

        # Form validate
        # Validacion del formulario
        if 'form.submitted' in self.request.params:
            role = self.request.params['role']
            self.db.query(User).filter_by(name=username).update({User.role: role}, synchronize_session=False)
            self.request.session.flash(f'User {user.name} edited', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)

        message = self.request.session.flash(f'You can edit the role of {username}', queue='', allow_duplicate=True)

        return dict(name='Edit',
                    message=message,
                    next_url=next_url,
                    user=user,
                    role=role
                    )


    #home view/vista home
    @view_config(route_name='home', renderer='../templates/home.jinja2')
    def home(self):
        return {'name':'Home'}


    #Welcome view/vista de binvenida
    @view_config(route_name='welcome', renderer='../templates/welcome.jinja2')
    def welcome(self):

        posts = self.db.query(BlogPosts).filter_by(user_id=self.request.user.id).all()

        ip_client = self.request.client_addr
        print(ip_client)
        g, geloc = self.greeting()
        print(g, geloc)
        if self.request.user.role == 'admin':
            self.request.session.flash(f'{"Hello " if g == None else g} You are the Administrator', queue='', allow_duplicate=False)
            return HTTPFound(location='/admin')
        if geloc == None:
            return {'name': 'Welcome', 'greeting': g, 'posts': posts, 'city': 'some','country': 'where'}
        return {'name':'Welcome','greeting':g, 'posts':posts, 'city':geloc.city_name, 'country':geloc.country_name}


    #Profile view/Vista de perfil de usuario
    @view_config(route_name='profile', renderer='../templates/profile.jinja2')
    def profile(self):
        username = self.request.matchdict['user']
        next_url = self.request.route_url('profile', user=username)

        # if no user no func/si no hay usuario no hayget_users funcion
        # User validation/validacion de usuario
        if self.out_or_stay(username=username): return HTTPFound(location='/error')

        if not next_url:
            next_url = self.request.route_url('home')
        profile = self.db.query(User).filter_by(name=username).first()

        #if form is submited save the imaga to the database/Si confirma el formulario guarda la imagen del perfil en la base de datos
        if 'form.submitted' in self.request.params:
            filename = self.request.params['image'].filename
            input_file = self.request.params['image'].file
            file_path = os.path.join(static_dir, 'static', filename)

            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)
            print(file_path)
            img = open(file_path, 'rb')
            image = img.read()
            img.close()

            self.db.query(User).filter_by(name=username).update({User.image: image}, synchronize_session=False)
            self.request.session.flash(f'User {profile.name} image changed', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)

        #image/imagen
        image = base64.b64encode(profile.image).decode('ascii')

        return {'name': 'Profile', 'user': profile, 'img':image, 'next_url':next_url}

    #post view/ vista de posteo
    @view_config(route_name='posts', renderer='../templates/posts.jinja2')
    def posts(self):
        username = self.request.matchdict['user']
        next_url = self.request.route_url('welcome')

        # if no user no func/si no hay usuario no hay funcion
        # User validation/validacion de usuario
        if self.out_or_stay(username=username): return HTTPFound(location='/error')

        if not next_url:
            next_url = self.request.route_url('home')
        user = self.db.query(User).filter_by(name=username).first()

        #post form/formulario post
        if 'form.submitted' in self.request.params:
            post_title = self.request.params['post_title']
            post_text = self.request.params['post_text']
            if self.request.localization is not None:
                city_name = self.request.localization.city_name
                province_name = self.request.localization.province_name
                country_name = self.request.localization.country_name
                ip = self.request.localization.ip

                post = BlogPosts(title=post_title,text=post_text,user_id=user.id,
                                 city_name=city_name,province_name=province_name,country_name=country_name,ip=ip)
            else:
                post = BlogPosts(title=post_title, text=post_text, user_id=user.id,
                                 city_name=None, province_name=None, country_name=None, ip=None)
            self.db.add(post)
            self.request.session.flash(f'User {user.name} has posted a new post', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)

        return {'name': 'Posts', 'user': user, 'next_url': next_url}

    #post by user view/ vista de post por usuario
    @view_config(route_name='posts_by_user', renderer='../templates/posts_by_user.jinja2')
    def posts_by_user(self):
        username = self.request.matchdict['user']
        next_url = self.request.route_url('welcome')
        if not next_url:
            next_url = self.request.route_url('home')
        user = self.db.query(User).filter_by(name=username).one()
        posts = self.db.query(BlogPosts).filter_by(user_id=user.id).all()
        image = base64.b64encode(user.image).decode('ascii')

        return {'name': 'Posts by user', 'user': user, 'next_url': next_url, 'posts':posts, 'img':image}

    #delete post view(only owners/ borrar post (solo owners)
    @view_config(route_name='delete_post', renderer='../templates/welcome.jinja2')
    def delete_post(self):
        next_url = self.request.route_url('welcome')
        if not next_url:
            next_url = self.request.route_url('home')
        # if no user no func/si no hay usuario no hay funcion
        # User validation/validacion de usuario
        username = None if not self.request.user else self.request.user.name
        if self.out_or_stay(username=username): return HTTPFound(location='/error')

        post_id =self.request.matchdict['post_id']
        post = self.db.query(BlogPosts).filter_by(id=post_id).one()
        self.db.delete(post)
        self.request.session.flash(f'The post titled {post.title} has been deleted succesfully', queue='', allow_duplicate=True)

        return HTTPFound(location=next_url)

    #Edit post view (only owners/ Vista editor de post(solo propietarios)
    @view_config(route_name='edit_post', renderer='../templates/edit_post.jinja2')
    def edit_post(self):
        next_url = self.request.route_url('welcome')
        if not next_url:
            next_url = self.request.route_url('home')
        user = self.request.matchdict['user']
        # if no user no func/si no hay usuario no hay funcion
        # User validation/validacion de usuario
        if self.out_or_stay(username=user): return HTTPFound(location='/error')

        post_id = self.request.matchdict['post_id']
        post = self.db.query(BlogPosts).filter_by(id=post_id).one()

        if 'form.submitted' in self.request.params:
            post_title = self.request.params['post_title']
            post_text = self.request.params['post_text']
            if self.request.localization is not None:
                city_name = self.request.localization.city_name
                province_name = self.request.localization.province_name
                country_name = self.request.localization.country_name
                ip = self.request.localization.ip

                self.db.query(BlogPosts).filter_by(id=post.id).update({BlogPosts.title: post_title,
                                                                   BlogPosts.text: post_text, BlogPosts.date:datetime.utcnow(),
                                                                   BlogPosts.city_name:city_name, BlogPosts.country_name:country_name,
                                                                   BlogPosts.province_name:province_name, BlogPosts.ip:ip},
                                                                  synchronize_session=False)
            else:
                self.db.query(BlogPosts).filter_by(id=post.id).update({BlogPosts.title: post_title,
                                                                       BlogPosts.text: post_text,
                                                                       BlogPosts.date: datetime.utcnow()},
                                                                      synchronize_session=False)
            self.request.session.flash(f'User {user} has edited {post.title} post', queue='', allow_duplicate=True)
            return HTTPFound(location=next_url)

        return {'name': 'Edit Post',  'next_url': next_url, 'post': post, 'user':user}

    ##Administrator view/vista administrador
    @view_config(route_name='admin', renderer='../templates/admin.jinja2')
    def admin(self):
        users = self.db.query(User).filter_by(name=User.name).all()
        posts = self.db.query(BlogPosts).filter_by(user_id=self.request.user.id).all()
        tasks = self.db.query(Tasks).filter_by(user_id=User.id).all()

        #Access validation/validacion de acceso
        if self.out_or_stay(): return HTTPFound(location='/error')
        count = 0
        title = str(self.request.user.name).capitalize()+' Account'
        return dict(name=title, users=users, posts=posts, tasks=tasks, count=count)


    #pseudodecorator
    def out_or_stay(self, username=None):
        # if no user no func/si no hay usuario no hay funcion
        if self.request.user is None: return True

        # Role or username validation/validacion de rol
        user = get_user(self.request)
        if user.role != 'admin' and username is None: return True
        if user.role == 'admin' and username is None: return False
        if username != user.name: return True
        else: return False