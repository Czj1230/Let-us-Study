import unittest
import sys
sys.path.append('../')
from api.seat import *
from app import app
import logging
logger = logging.getLogger()

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
 
logging.basicConfig(filename='mylog.txt', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class TestOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING']=True
        cls.app = app.test_client()
        logging.info("set up completed")

    def teardown_class(self):
        logging.info("tear down completed")

    def test_list_countdown(self):
        response = self.app.get("/countdown/list/1")
        assert b'"all_countdowns"' in response.data

if __name__ == '__main__':
    unittest.main(verbosity=2)