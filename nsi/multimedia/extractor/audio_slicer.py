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

class AudioSlicer:
    '''
    Extracts a sound file from another, given both start and end times
    '''
    
    def __init__(self, source, target, start, end, log_stream=sys.stdout):
        '''Extracts a desired timebox from a file to another. source and target params
           refers to the input and output files. start and end are the times, in seconds,
           of the desired timebox.'''
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s [%(module)s] %(message)s',
                            stream=log_stream)
        self._create_pipeline(source, target, start, end)
        self._configure_message_handling()
    
    def _create_pipeline(self, source, target, start, end):
        '''
        Creates a pipeline in the form:
        
        gnlcomposition
        -----------------
        | gnlfilesource | --> audioconvert --> lame --> filesink 
        -----------------   
        '''
        self.pipeline = gst.Pipeline('slicer')
        comp = gst.element_factory_make('gnlcomposition', 'mycomposition')
        comp.connect('pad-added', self._on_pad)
        self.convert = gst.element_factory_make('audioconvert', 'convert')
        self.pipeline.add(self.convert)
        mp3_encoder = gst.element_factory_make('lame', 'mp3-encoder')
        self.pipeline.add(mp3_encoder)
        self.convert.link(mp3_encoder)
        out = gst.element_factory_make('filesink', 'out')
        out.set_property('location', target)
        self.pipeline.add(out)
        mp3_encoder.link(out)
        
        audio1 = gst.element_factory_make('gnlfilesource', 'audio1')
        audio1.set_property('location', source)
        audio1.set_property('start', long(start) * gst.SECOND)
        audio1.set_property('duration', long(end-start) * gst.SECOND)
        self.pipeline.add(comp)
        comp.add(audio1)
        
    def _configure_message_handling(self):
        '''Registers callback for receiving bus messages''' 
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
    
    def run(self):
        '''Runs the slicing'''
        logging.info('Starting slicing process...')
        self.pipeline.set_state(gst.STATE_PLAYING)
        gtk.main()
    
    def _on_pad(self, comp, pad):
        '''Callback for connecting dynamic pads'''
        convpad = self.convert.get_compatible_pad(pad, pad.get_caps())
        pad.link(convpad)
        logging.info("Pad added")
    
    def _on_message(self, bus, message):
        '''Callback for message processing'''
        if message.type == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            logging.info('Slicing terminated')
            gtk.main_quit()
            
            
if __name__ == '__main__':
    slicer = AudioSlicer(
        source=sys.argv[1],
        target=sys.argv[2], 
        start=int(sys.argv[3]), 
        end=int(sys.argv[4]))
    slicer.run()