#In this file you define the routes that you'll use in the app
#En este archivo se configurar las rutas que vas a usar
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('delete_user','/{user}/delete')
    config.add_route('admin','/admin')
    config.add_route('welcome', '/welcome')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')