#This file is for initialize the db content
#Este archivo sirve para inicializar el contenido de la base de datos
import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models

#In this function i add some users for start to work
#En esta funcion agregue algunos usuarios por defencto
def setup_models(dbsession):
    # When you login as admin, and then deleted all the users, if you want to add this all default users again,
    # by using 'initialize_ejerciciokenwin_db  development.ini' command, you must to comment the two lines below.
    # Si te logueaste como admin, y despues borraste todos los usuarios y luego queres agregarlos denuevo
    # usando el comando 'initialize_ejerciciokenwin_db  development.ini' tenes que comentar las dos lineas que siguen.
    admin = models.User(name='admin', password='admin', role='admin')
    dbsession.add(admin)

    s = -1
    roles = ['guest','developer','salesman','company','customer']
    names = ['homer', 'bart', 'lisa', 'marge', 'maggie']
    for _ in range(5):
        s += 1
        users = models.User(name=names[s], password=names[s] , role=roles[s])
        dbsession.add(users)
    #pass

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
