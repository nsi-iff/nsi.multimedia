import unittest
from should_dsl import should
import os
from subprocess import Popen, PIPE, STDOUT
from nsi.multimedia.utils import get_duration
import time

#from nsi.multimedia.transform.flv_converter import FlvConverter
from nsi.multimedia.transform.ogg_converter import OggConverter
from nsi.multimedia.transform.flv_converter import FlvConverter

class TestConvertVideoFormat(unittest.TestCase):

    def setUp(self):
        self.input_file = "inputs/cachorros.mpg"
        self.output_flv = "output/test.flv"
        self.output_ogv = "output/test.ogv"

    def test_mpg_to_flv(self):
        conversor = FlvConverter(source=self.input_file, target=self.output_flv)
        conversor.run()
        time.sleep(20)
        abs(get_duration(self.input_file) - get_duration(self.output_flv)) |should| be_less_than(5)
        os.system("rm %s"%(self.output_flv))

    def test_mpg_to_ogv(self):
        conversor = OggConverter(source=self.input_file, target=self.output_ogv)
        conversor.run()
        time.sleep(20)
        abs(get_duration(self.input_file) - get_duration(self.output_ogv)) |should| be_less_than(5)
        os.system("rm %s"%(self.output_ogv))



if __name__ == '__main__':
    unittest.main()
