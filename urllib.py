from werkzeug.utils import secure_filename

import cgi
import logging
import os
import posixpath
import urllib.request
import shutil
import urllib.parse

logger = logging.getLogger('sherbang.script_helpers')


class FileExistsException(Exception):
    def __init__(self, filename):
        super().__init__('{} already exists'.format(filename))
        self.filename = filename


def get_filename(urllib_response):
    """
    Attempt to get the filename out of the response headers.  Failing that, use
    the filename part of the URL.  Sanitize the filename to make it safe to use
    locally.
    """
    cd_header = urllib_response.headers.get('Content-Disposition', '')
    _, params = cgi.parse_header(cd_header)
    if 'filename' in params:
        filename = params['filename']
    else:
        path = urllib.parse.urlsplit(urllib_response.geturl()).path
        filename = posixpath.basename(path)

    filename = secure_filename(filename)

    return filename


def download_file(url, output_dir=None, overwrite=False):
    """
    Download the file from `url` and save it locally under `output_dir`.

    If overwrite is True then existing files matching the same filename will
    be overwritten, otherwise a FileExistsException will be raised.
    """
    with urllib.request.urlopen(url) as response:
        file_name = get_filename(response)
        if output_dir:
            file_name = os.path.join(output_dir, file_name)

        if overwrite is not True and os.path.exists(file_name):
            exc = FileExistsException(
                'File already exists: "{}"'.format(file_name))
            exc.filename = file_name
            raise exc
        else:
            logger.info(
                'Downloading {} to {}'.format(response.geturl(), file_name)
                )
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

    return file_name
