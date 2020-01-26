#Generates a 404 page when the app doesn't find the route
#Genera una pagina 404 cuando en la applicacion no se encuentra la ruta
from pyramid.view import notfound_view_config


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}
