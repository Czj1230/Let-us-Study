import unittest
import sys
sys.path.append('../')
from api.student import *
from app import app
import logging
logger = logging.getLogger()

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
 
logging.basicConfig(filename='mylog.txt', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class TestStudent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING']=True
        cls.app = app.test_client()
        logging.info("set up completed")

    def teardown_class(self):
        logging.info("tear down completed")

    def test_getRanking(self):
        response = self.app.get('/student/getRanking')
        assert b'"name":' in response.data

if __name__ == '__main__':
    unittest.main(verbosity=2)