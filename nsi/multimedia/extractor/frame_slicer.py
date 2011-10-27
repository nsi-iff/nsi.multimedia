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

class FrameSlicer:
    '''
    Extracts frames from a video file, given a timebox
    
    This class has a bug: the extraction process never ends up, i.e. the gst.MESSAGE_EOS is
    never dispatched.  
    '''
    
    def __init__(self, input, output_pattern, start, end, log_stream=sys.stdout):
        '''
        input is the input file (not altered, must be an OGG Media File)
        output_pattern is the pattern for output image files (created or overridden). 
          Example: output-04%d.jpg will generate output-0001.jpg, output-0002.jpg and so on.
        start and end are the timebox borders (inclusive) and must be expressed in seconds
        '''
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s [%(module)s] %(message)s',
                            stream=log_stream)
        self._create_pipeline(input, output_pattern, start, end)
        self._configure_message_handling()
    
    def _create_pipeline(self, source, output_pattern, start, end):
        '''
        Creates a pipeline in the form:
        
        gnlcomposition
        -----------------
        | gnlfilesource | --> jpegenc --> multifilesink 
        -----------------   
        '''
        duration_in_nanos = (end - start + 1) * gst.SECOND
        start_in_nanos = start * gst.SECOND
        self.pipeline = gst.parse_launch(
            ("gnlfilesource location=%s start=0 duration=%d media-start=%d " + 
                 "media-duration=%d ! jpegenc ! multifilesink location=%s") % 
             (source, duration_in_nanos, start_in_nanos, duration_in_nanos, output_pattern))
        
    def _configure_message_handling(self):
        '''
        Registers callback for receiving bus messages
        ''' 
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
    
    def run(self):
        '''
        Runs the extracting
        '''
        self.pipeline.set_state(gst.STATE_PLAYING)
        logging.info('Extracting started...')
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
    FrameSlicer(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])).run()