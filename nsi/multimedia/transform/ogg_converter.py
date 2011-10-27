##############################################################################
#
# Copyright (c) 2009 ISrg (NSI, IFF, BRAZIL) and Contributors. 
#                                                     All Rights Reserved.
#                     Rodrigo S. Manhaes <rmanhaes@gmail.com> 
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
import logging
import sys
from subprocess import Popen

from nsi.multimedia.utils import replace_file_extension

class OggConverter:
    '''
    Converts a video input file to OGM. We elected OGM as our canonical video format. 
    '''
    
    def __init__(self, source, target=None, log_stream=sys.stdout):
        '''
        source is the input file (not altered)
        target is the output file (created or overriden)
        '''
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s [%(module)s] %(message)s',
                            stream=log_stream)
        self.source = source
        self.target = target
        self.log_stream = log_stream

    
    def run(self):
        '''
        Runs the conversion
        '''
        command = "ffmpeg -r 60 -i %s -vcodec libtheora -acodec libvorbis  %s"%(self.source, self.target or replace_file_extension(self.source, "ogv"))
        process = Popen(command.split(),stdout=self.log_stream)
        output, error = process.communicate()
        print error
            
#usage example
if __name__ == '__main__':
    OggConverter(sys.argv[1]).run()
