#This is a config file, necesary to include the views, moludes, models and so on
#Este archivo de configuracion sirve para incluir las vistas, modelo de base de datos, modulos etc.

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
import os

static_dir = os.path.abspath(os.path.dirname(__file__))


def main(global_config, **settings):
    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
    with Configurator(settings=settings,session_factory=my_session_factory) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        #config.add_jinja2_renderer('.html')
        config.include('.security')
        config.include('.routes')
        config.scan('.views')

    return config.make_wsgi_app()
