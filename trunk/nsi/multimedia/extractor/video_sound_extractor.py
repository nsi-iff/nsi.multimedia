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

import gst
import logging
import sys
import gtk

from nsi.multimedia.utils import replace_file_extension

class VideoSoundExtractor:
    '''
    Extracts sound from a video file, storing it on a mp3 audio file
    '''
    
    def __init__(self, source, target=None, log_stream=sys.stdout):
        '''
        source is the name of the file video from which sound will be extracted (source file is not altered)
        target is the name of the resulting mp3 audio file (target file is created or overridden)
        '''
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            stream=log_stream)
        self.source = source
        self.target = target or replace_file_extension(source, 'mp3')
        self._create_pipeline()
        self._configure_message_handling()


    def _create_pipeline(self):
        '''
        Creates a pipeline in the form:
                              |--> queue --> fakesink
        filesrc --> decodebin |
                              |--> audioconvert --> lame --> filesink
        '''
        self.pipeline = gst.parse_launch(
            ('filesrc location=%s ! decodebin name=d ' + 
            'd. ! queue  ! fakesink ' + 
            'd. ! audioconvert ! lame ! filesink location=%s') %
            (self.source, self.target)) 
        
    def _configure_message_handling(self):
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
        
    def run(self):
        logging.info('Running...')
        self.pipeline.set_state(gst.STATE_PLAYING)
        gtk.main()
        
    def _on_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            logging.info('Done')
            gtk.main_quit() 
            
# usage example
if __name__ == '__main__':
    VideoSoundExtractor(argv[1]).run()
