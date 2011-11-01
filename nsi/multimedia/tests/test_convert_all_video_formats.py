import unittest
from should_dsl import should
import os

from nsi.multimedia.transform.flv_converter import FlvConverter

class TestConvertVideoFormat(unittest.TestCase):

    def setUp(self):
        self.input_file = "inputs/cachorros.mpg"
        self.output = "output/test.flv"

    def test_avi_to_flv(self):
        conversor = FlvConverter(source=self.input_file, target=self.output)
        conversor.run()
        size_of_output_file = os.path.getsize(self.output)
        size_of_output_file |should| be_greater_than(0)
        os.system("rm %s"%(self.output))



if __name__ == '__main__':
    unittest.main()
