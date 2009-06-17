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
import logging
import sys

class FlvOgmConverter(object):
    '''
    Converts a given video file to OGM and FLV. OGM is needed for GNonLin manipulation
    and FLV is the format accepted by FlowPlayer.
    '''
    
    def __init__(self, source, target=None, log_stream=sys.stdout):
        '''
        source is the input file (not altered)
        target is a dictionary with the output file names (at "ogm" and "flv" keys)
        '''
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s [%(module)s] %(message)s',
                            stream=log_stream)
        self._create_pipeline(source, target or
            {'ogm': self._replace_file_extension(source, "convert.ogm"), 
             'flv': self._replace_file_extension(source, "convert.flv")})
        self._configure_message_handling()
        
    def _create_pipeline(self, source, target):
        '''
        Create a pipeline in the form:
                                                 |--> queue --> theoraenc ------------------------------>|
                              |--> queue --> tee |                                                       | oggmux --> filesink
                              |                  |--> queue --> ffenc_flv -------------------     ------>|
        filesrc --> decodebin |                                                              |   |
                              |                  |--> queue --> audioconvert --> vorbisenc --|---        |
                              |--> queue --> tee |                                           ------------| flvmux --> filesink
                                                 |--> queue --> audioconvert --> lame ------------------>|
        '''
        self.pipeline = gst.parse_launch(
            ('''filesrc location=%s ! decodebin name=d   
                   d. ! queue ! tee name=video 
                     video. ! queue ! theoraenc ! omux. 
                     video. ! queue ! ffenc_flv ! fmux.  
                   d. ! queue ! tee name=audio 
                     audio. ! queue ! audioconvert ! vorbisenc ! omux. 
                     audio. ! queue ! audioconvert ! lame ! fmux. 
                   flvmux name=fmux ! filesink location=%s 
                   oggmux name=omux ! filesink location=%s''') % 
            (source, target["flv"], target["ogm"])
        )
        
    def _configure_message_handling(self):
        '''
        Registers callback for receiving bus messages
        ''' 
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
        
    def _replace_file_extension(self, file_name, new_extension):
        return file_name[:file_name.rindex('.')] + "." + new_extension
    
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
            
            
if __name__ == '__main__':
    FlvOgmConverter(source=sys.argv[1]).run()