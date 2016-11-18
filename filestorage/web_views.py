import cgi

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    return dict()
    # This is how params can be passed to the renderer
    #return dict(name=request.matchdict['name'])

"""
# /howdy?name=alice which links to the next view
@view_config(route_name='hello')
def hello_view(request):
    name = request.params.get('name', 'No Name')
    body = '<p>Hi %s, this <a href="/goto">redirects</a></p>'
    # cgi.escape to prevent Cross-Site Scripting (XSS) [CWE 79]
    return Response(body % cgi.escape(name))


# /goto which issues HTTP redirect to the last view
@view_config(route_name='redirect')
def redirect_view(request):
    return HTTPFound(location="/problem")


# /problem which causes a site error
@view_config(route_name='exception')
def exception_view(request):
    raise Exception()

# /get which shows a file by its uuid
@view_config(route_name='get_file')
def get_file_view(request):
    body = 'Param: $(uuid)' % request.matchdict
    return Response(body)

view_config(route_name='home', renderer='json')
def hello_json(request):
    return [1, 2, 3]
"""
