'''

Copyright (C) 2017-2019 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from sregistry.logger import bot
from sregistry.utils import (
    parse_image_name,
    remove_uri
)

import sys
import os


def push(self, path, name, tag=None):
    '''push an image to your Storage. If the collection doesn't exist,
       it is created.
   
       Parameters
       ==========
       path: should correspond to an absolute image path (or derive it)
       name: should be the complete uri that the user has requested to push.
       tag: should correspond with an image tag. This is provided to mirror Docker

    '''
    path = os.path.abspath(path)
    bot.debug("PUSH %s" % path)

    if not os.path.exists(path):
        bot.error('%s does not exist.' %path)
        sys.exit(1)

    # Parse image names
    names = parse_image_name(remove_uri(name), tag=tag)

    # Get the size of the file
    file_size = os.path.getsize(path)
    chunk_size = 4 * 1024 * 1024
    storage_path = "/%s" %names['storage']

    # Create / get the collection
    collection = self._get_or_create_collection(names['collection'])

    # The image name is the name followed by tag
    image_name = os.path.basename(names['storage'])
 
    # prepare the progress bar
    progress = 0
    bot.show_progress(progress, file_size, length=35)

    # Put the (actual) container into the collection
    with open(path, 'rb') as F:
        self.conn.put_object(names['collection'], image_name,
                             contents= F.read(),
                             content_type='application/octet-stream')

    # Finish up
    bot.show_progress(iteration=file_size,
                      total=file_size,
                      length=35,
                      carriage_return=True)

    # Newline to finish download
    sys.stdout.write('\n')
