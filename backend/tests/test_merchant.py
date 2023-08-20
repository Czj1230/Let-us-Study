import unittest
import sys
sys.path.append('../')
from api.merchant import *
from app import app
import logging
logger = logging.getLogger()

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
 
logging.basicConfig(filename='mylog.txt', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class TestMerchant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING']=True
        cls.app = app.test_client()
        logging.info("set up completed")

    def teardown_class(self):
        logging.info("tear down completed")

    def test_list_all_merchant(self):
        response = self.app.get('/merchant/list')
        # logging.debug(response.data)
        assert b'"merchantName":' in response.data
        assert b'"merchantGrade":' in response.data
    
    def test_insert_merchant(self):
        #为了不影响数据的cleanness，模拟插入失败的场景
        response = self.app.post('/merchant/insert', content_type = 'application/json', data = '{"username":"11","password":"unit","email":"unit@fudan.edu.cn","phone_number":"000"}')
        logging.debug(response.data)
        assert b'"status": 0' in response.data
    
    def test_set_merchant(self):
        response = self.app.post('/merchant/setting/2',content_type = 'application/json', data = '{"merchantName":"11","merchantShowName":"", "merchantLocation":"","merchantStartTime":null,"merchantEndTime":null}')
        logging.debug(response.data)
        assert b'"status": 1' in response.data



if __name__ == '__main__':
    unittest.main(verbosity=2)