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

import pygst
pygst.require('0.10')
import gst
import gtk
import time
import logging
import sys

from nsi.multimedia.utils import replace_file_extension

class FlvConverter:
    '''
    Converts a video input file to FLV. This format is accepted by the FlowPlayer web player. 
    '''
    
    def __init__(self, source, target=None, log_stream=sys.stdout):
        '''
        source is the input file (not altered)
        target is the output file (created or overriden)
        '''
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s [%(module)s] %(message)s',
                            stream=log_stream)
        self._create_pipeline(source, target if target is not None else replace_file_extension(source, "flv"))
        self._configure_message_handling()
    
    def _create_pipeline(self, source, target):
        '''
        Creates a pipeline in the form:
                              |--> queue --> theoraenc ------------------->|
        filesrc --> decodebin |                                            | oggmux --> filesink
                              |--> queue --> audioconvert --> vorbisenc -->|
        '''
        self.pipeline = gst.parse_launch(
            (" filesrc location=%s ! decodebin name=d " +  
                 "d. ! queue ! ffmpegcolorspace ! ffenc_flv ! mux. " + 
                 "d. ! queue ! audioconvert ! lame ! mux. " + 
             "ffmux_flv name=mux ! filesink location=%s") % 
             (source, target))
        
    def _configure_message_handling(self):
        '''
        Registers callback for receiving bus messages
        ''' 
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
    
    def run(self):
        '''
        Runs the conversion
        '''
        self.pipeline.set_state(gst.STATE_PLAYING)
        logging.info('Conversion started...')
        gtk.main()
    
    def _on_message(self, bus, message):
        '''
        Callback for message processing
        '''
        if message.type == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            logging.info('Terminated')
            gtk.main_quit()
            
#usage example
if __name__ == '__main__':
    FlvConverter(sys.argv[1]).run()