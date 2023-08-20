import unittest
import sys
sys.path.append('../')
from api.order import *
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

    def test_list_merchant_order(self):
        response = self.app.get('/order/listForMerchant/3')
        logging.debug(response.data)
        logging.debug(type(response.data))
        assert b'"merchantName": "22"' in response.data
    
    def test_list_merchant_order_empty(self):
        response = self.app.get('/order/listForMerchant/333')
        logging.debug(response.data)
        logging.debug(type(response.data))
        assert b'"merchantName": null' in response.data
    
    def test_list_student_order(self):
        response = self.app.get('/order/listForStudent/1')
        logging.debug(response.data)
        logging.debug(type(response.data))
        assert b'"merchantName": "22"' in response.data

if __name__ == '__main__':
    unittest.main(verbosity=2)