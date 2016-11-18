import datetime
import hashlib
import os
import shelve
import shutil
import uuid

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response, FileResponse


"""
This REST API provides a file resource to upload, update, download
and delete files.
"""
@view_defaults(route_name='files', renderer='json')
class RESTView(object):
    def __init__(self, request):
        self.request = request
        self.path_db = request.registry.settings['path_database']
        self.path_tmp = request.registry.settings['path_tmp']
        self.path_file_storage = request.registry.settings['path_file_storage']

    def db_fetch_file(self, file_id):
        with shelve.open(self.path_db, flag='r') as db:
            if file_id not in db:
                raise LookupError('File with uuid %s does not exist!' % uuid)
            else:
                return db[file_id]

    def db_add_file(self, file_id, data):
        with shelve.open(self.path_db, flag='w') as db:
            if file_id in db:
                raise Error('File with uuid %s already exists!' % uuid)
            else:
                db[file_id] = data

    def db_update_file(self, file_id, data):
        with shelve.open(self.path_db, flag='w') as db:
            if file_id not in db:
                raise LookupError('File with uuid %s does not exist, cannot update!' % uuid)
            else:
                db[file_id] = data

    def db_delete_file(self, file_id):
        with shelve.open(self.path_db, flag='w') as db:
            if file_id in db:
                del db[file_id]
            else:
                raise LookupError('File with uuid %s does not exist, cannot delete!' % uuid)

    """
    Helper method to calculate hash of file
    """
    def hash_file(self, filename, hasher):
        BLOCKSIZE = 65536
        with open(filename, 'rb') as infile:
            buf = infile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = infile.read(BLOCKSIZE)
        return hasher.hexdigest()

    @view_config(request_method='PUT')
    def put(self):
        try:
            # Create a fresh uuid for the new file
            file_id = str(uuid.uuid4())
            # Use PUT /files to create a new file
            input_file = self.request.POST['file'].file
            # Write the data into a temporary file
            temp_file_path = os.path.join(self.path_tmp, '%s' % file_id) + '~'
            input_file.seek(0)
            with open(temp_file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)
            # Now that we know the file has been fully saved to disk move it into place.
            target_file_path = os.path.join(self.path_file_storage, '%s' % file_id)
            os.rename(temp_file_path, target_file_path)
            # Calculate file hash
            filehash_md5 = self.hash_file(target_file_path, hashlib.md5())
            filehash_sha1 = self.hash_file(target_file_path, hashlib.sha1())
            filehash_sha256 = self.hash_file(target_file_path, hashlib.sha256())
            # Gather all data about the file
            file_data = dict(uuid=file_id,name=self.request.POST['file'].filename, key=str(uuid.uuid4()), create_utc=str(datetime.datetime.utcnow()), sha256=filehash_sha256, sha1=filehash_sha1, md5=filehash_md5)
            # Store file data in database
            self.db_add_file(file_id, file_data)
            # Hopefully everything worked out, so return the data from the file
            return file_data
        except:
            return dict(success=False)

    @view_config(request_method='GET', route_name='files_uuid')
    def get(self):
        # Use GET /files/<uuid> to retrieve the file
        file_id = self.request.matchdict['file_id']
        try:
            file_data = self.db_fetch_file(file_id)
            external_filename = file_data['name']
            file_response = FileResponse(os.path.join(self.path_file_storage, '%s' % file_id))
            file_response.content_disposition = 'attachment; filename=%s' % external_filename
            return file_response
        except:
            return dict(success=False)

    @view_config(request_method='GET', route_name='file_details')
    def get_info(self):
        # Use GET /files/<uuid>/info to get file details
        file_id = self.request.matchdict['file_id']
        try:
            file_data = self.db_fetch_file(file_id)
            del file_data['key'] # Remove the secret key only the creator is supposed to know
            return file_data
        except:
            return dict(success=False)

    @view_config(request_method='DELETE', route_name='file_uuid_key')
    def delete(self):
        # Use DELETE /files/<uuid>/<key> to delete file
        file_id = self.request.matchdict['file_id']
        file_key = self.request.matchdict['file_key']
        try:
            file_data = self.db_fetch_file(file_id)
        except:
            return dict(success=False)
        if file_data['key'] == file_key:
            # Delete file and db entry
            file_path = os.path.join(self.path_file_storage, '%s' % file_id)
            os.remove(file_path)
            self.db_delete_file(file_id)
            return dict(success=True)
        else:
            return dict(success=False)

