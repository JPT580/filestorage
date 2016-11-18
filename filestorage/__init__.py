import os
import shelve

from wsgiref.simple_server import make_server
from pyramid.config import Configurator


"""
Main entrance point that returns a wsgi application
"""
def main(global_config, **settings):
    config = Configurator(settings=settings)

    # Home view when visiting the app on /
    config.add_route('home', '/')

    # REST-API view behind /files
    config.add_route('files', '/files')
    config.add_route('files_uuid', '/files/{file_id}')
    config.add_route('file_details', '/files/{file_id}/info')
    config.add_route('file_uuid_key', '/files/{file_id}/{file_key}')

    # Route for static files
    config.add_static_view(name='static', path='filestorage:static')

    # Add pyramid_jinja2 module to app config for web_views
    config.include('pyramid_jinja2')

    # Do a config scan to get all the views
    config.scan()

    # Make sure the infrastructure (folders, database) are set up
    setup_infrastructure(config.registry.settings)

    # Finally build and return the app
    app = config.make_wsgi_app()
    return app


"""
Checkup routine to make sure folders and database are fine
"""
def setup_infrastructure(settings):
    # Check temp folder
    tmp_folder = settings['path_tmp']
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
    if not os.access(tmp_folder, os.W_OK):
        raise PermissionError('Unable to write to temporary folder: %s' % tmp_folder)
    # Check file storage folder
    path_file_storage = settings['path_file_storage']
    if not os.path.exists(path_file_storage):
        os.makedirs(path_file_storage)
    if not os.access(path_file_storage, os.W_OK):
        raise PermissionError('Unable to write to file storage folder: %s' % path_file_storage)
    # Make sure shelve database works (and exists)
    path_database = settings['path_database']
    db = shelve.open(path_database, flag='c')
    db.close()
    pass

