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
import sys
import logging
import os

class VideoSlicer:
    '''
    Extracts a timeboxed slice from a video file 
    '''
    
    def __init__(self, source, start, end, log_stream=sys.stdout):
        '''
        source => source video file name
        start => start of desired slice, in seconds
        end => end of desired slice, in seconds
        log_stream => optional, define the stream to which log is written (default = sys.stdout)
        '''
        self.log_stream = log_stream
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            stream=log_stream)
        self.source = source
        self.target = self.__get_name(source) + '-extract.ogm'
        self.start = start * gst.SECOND
        self.duration = (end - start + 1) * gst.SECOND

    def run(self):
        '''
        Runs the extrating. The strategy is four-phased:
        1) Separates video and audio parts from the source video. GNonLin doesn't work fine with 
        audio and video simultaneous streams. The generated files are on OGM/OGG format, because
        in out tests, GNonLin only worked fine with this format.
        2) Extracts video slice from video-only file generated in step 1
        3) Extracts audio slice from audio file generated in step 1
        4) Joins audio and video slices to a video (audio+video) file
        '''
        try:
            self._prepare_environment()
            logging.info('Starting separating audio and video...') 
            self.convert_to_ogm_parts()
            logging.info('Separating done.')
        
            logging.info('Slicing video part...')
            self.slice_video()
            logging.info('Video slicing done.')
            
            logging.info('Slicing audio part...')
            self.slice_audio()
            logging.info('Audio slicing done.')
            
            logging.info('Joining video and audio...')
            self.join_all()
            logging.info('Extracting process done.')
        finally:
            logging.info('Cleaning environment...')
            self._clean_environment()
            logging.info('Done.')
            
    def _prepare_environment(self):
        self.temporary_files = []
        
    def _clean_environment(self):
        '''
        Removes temporary files at the end of processing 
        '''
        for file_name in self.temporary_files:
            os.remove(file_name)
            
    def __get_name(self, file_name):
        return file_name[:file_name.rindex('.')]
    
    def convert_to_ogm_parts(self):
        '''
        Step 1. See run() docstring
        '''
        source_name = self.__get_name(self.source)
        self.video_ogg_name = source_name + '-video.ogm'
        self.audio_ogg_name = source_name + '-audio.ogg'
        pipeline = gst.parse_launch(
            ("filesrc location=%s ! decodebin name=d " + 
             " d. ! queue ! theoraenc ! oggmux ! filesink location=%s.ogm " + 
             " d. ! queue ! audioconvert ! vorbisenc ! oggmux ! filesink location=%s.ogg") %
             (self.source, 
              source_name + '-video',
              source_name + '-audio'))
        self.configure_message_handling(pipeline)
        pipeline.set_state(gst.STATE_PLAYING)
        self.current_pipeline = pipeline
        self.temporary_files.append(self.video_ogg_name)
        self.temporary_files.append(self.audio_ogg_name)
        gtk.main()
        
    def slice_video(self):
        '''
        Step 2. See run() docstring
        '''
        self.video_part = self.__get_name(self.source) + '-video-part.ogm'
        pipeline = gst.parse_launch(
           ('gnlfilesource location=%s start=0 media-start=%d ' + 
              'duration=%d media-duration=%d ! theoraenc ! oggmux ! ' + 
              'filesink location=%s') % 
              (self.video_ogg_name, self.start, self.duration, self.duration, self.video_part))
        self.configure_message_handling(pipeline)
        pipeline.set_state(gst.STATE_PLAYING)
        self.temporary_files.append(self.video_part)
        self.current_pipeline = pipeline
        gtk.main()
        
    def slice_audio(self):
        '''
        Step 3. See run() docstring
        '''
        self.audio_part = self.__get_name(self.source) + '-audio-part.ogg'
        pipeline = gst.parse_launch(
            ("gnlfilesource location=%s start=0 media-start=%d duration=%d media-duration=%d ! " + 
                "audioconvert ! vorbisenc ! oggmux ! filesink location=%s") %
            (self.audio_ogg_name, self.start, self.duration, self.duration, self.audio_part))
        self.configure_message_handling(pipeline)
        pipeline.set_state(gst.STATE_PLAYING)
        self.temporary_files.append(self.audio_part)
        self.current_pipeline = pipeline
        gtk.main()
                    
    def join_all(self):
        '''
        Step 4. See run() docstring
        '''
        pipeline = gst.parse_launch(
            ("filesrc location=%s ! decodebin ! theoraenc ! mux. " +  
             "filesrc location=%s ! decodebin ! audioconvert ! vorbisenc ! mux. " + 
                 "oggmux name=mux ! filesink location=%s") %
            (self.video_part, self.audio_part, self.target))
        self.configure_message_handling(pipeline)
        pipeline.set_state(gst.STATE_PLAYING)
        self.current_pipeline = pipeline
        gtk.main()
                        
    def configure_message_handling(self, pipeline):
        '''
        Register callback for message processing
        '''
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)
        
    def on_message(self, bus, message):
        '''
        Process messages for terminating processing
        '''
        if message.type in (gst.MESSAGE_EOS, gst.MESSAGE_SEGMENT_DONE):
            self.current_pipeline.set_state(gst.STATE_NULL)
            gtk.main_quit()

# usage example            
if __name__ == '__main__':
    VideoSlicer(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).run()