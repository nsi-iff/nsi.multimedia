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

import unittest
from utils import replace_file_extension

class UtilsTest(unittest.TestCase):
    def test_replace_ok(self):
        self.assertEquals('teste.ogg', replace_file_extension('teste.mpeg', 'ogg'))
        self.assertEquals('teste.teste.ogg', replace_file_extension('teste.teste.mpeg', 'ogg'))
        self.assertEquals('arquivo.ogg', replace_file_extension('arquivo.mpeg', 'ogg'))
        self.assertEquals('teste.ogg', replace_file_extension('teste', 'ogg'))
        
    def test_replace_wrong_input(self):
        try:
            self.assertEquals('output.ogg', replace_file_extension(None, 'ogg'))
            self.fail()
        except AttributeError:
            pass
        try:
            self.assertEquals('output.ogg', replace_file_extension(10, 'ogg'))
            self.fail()
        except AttributeError:
            pass
                
if __name__ == '__main__':
    unittest.main()