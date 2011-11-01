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
import logging
import sys
from subprocess import Popen
from nsi.multimedia.transform.base_converter import BaseConverter
from nsi.multimedia.transform.ogg_converter import OggConverter
from nsi.multimedia.transform.flv_converter import FlvConverter


class FlvOgmConverter(BaseConverter):
    '''
    Converts a given video file to OGM and FLV. OGM is needed for GNonLin manipulation
    and FLV is the format accepted by FlowPlayer.
    '''

    def run(self):
        '''
        Runs the conversion
        '''
        OggConverter(self.source, self.target, self.log_stream).run()
        FlvConverter(self.source, self.target, self.log_stream).run()


if __name__ == '__main__':
    FlvOgmConverter(source=sys.argv[1]).run()
