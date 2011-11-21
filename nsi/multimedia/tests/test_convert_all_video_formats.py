import unittest
from should_dsl import should
import os
from subprocess import Popen, PIPE, STDOUT

#from nsi.multimedia.transform.flv_converter import FlvConverter
from nsi.multimedia.transform.ogg_converter import OggConverter

class TestConvertVideoFormat(unittest.TestCase):

    def setUp(self):
        self.input_file = "tests/inputs/parkour.flv"
        self.output_flv = "tests/output/test.flv"
        self.output_ogv = "tests/output/test.ogv"

#    def test_mpg_to_flv(self):
#        conversor = FlvConverter(source=self.input_file, target=self.output_flv)
#        conversor.run()
#        size_of_output_file = os.path.getsize(self.output_flv)
#        size_of_output_file |should| be_greater_than(0)
#        os.system("rm %s"%(self.output_flv))

    def test_mpg_to_ogv(self):
        conversor = OggConverter(source=self.input_file, target=self.output_ogv)
        import pdb;pdb.set_trace()
        conversor.run()
        conversor.get_duration(self.input_file) |should| equal_to(conversor.get_duration(self.output_ogv))
        os.system("rm %s"%(self.output_ogv))



if __name__ == '__main__':
    unittest.main()
