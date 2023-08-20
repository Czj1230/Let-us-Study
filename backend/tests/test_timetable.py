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

class TestTimeTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING']=True
        cls.app = app.test_client()
        logging.info("set up completed")

    def teardown_class(self):
        logging.info("tear down completed")

    def test_list_timeTable(self):
        response = self.app.get('/timetable/list/1')
        assert b'"all_timetables"' in response.data

if __name__ == '__main__':
    unittest.main(verbosity=2)