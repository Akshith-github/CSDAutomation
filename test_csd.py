# python test_csd.py

import unittest
from run import *
from utils.excelUtils import getExcelDf
from utils.dbUtils import getDbDf,create_dummy_db
from random import randint

""" 
Tasks:
1. Install box in your laptop and try to access from python script. # done instatllation manually

2. Upload a sample excel sheet to box (as discussed) and read it from python script. # done uploading manually

3. Install couch db and upload all the rows that you have in Excel (for first run) , 
then from next run onwards compare excel rows and rows present in db.
# two methods 
    - local CouchDB instance # done
    - remote CouchDB instance # need to search for remote service
# python script to operate on couchdb
    - CouchDB python package is to be used # done

4. Figure out rows for which status is modified. For each row :- Write a document,  
prepare a dummy template and read few values from row and place it at placeholder in document.

5. Prepare draft email with attachment, subject, receiver email (take it from Excel), 
sender will be your email. Save the email in draft of your outlook

"""

"""
Tests:
1. Test if environment variables are set
    => test_1env_vars() : test if environment variables are set
2. Test if file exists
    => test_2file_exists() : test if file exists
3. Test if file is in correct format
    => test_3file_format() : test if file is in correct format
4. Test if file read works
    => test_4file_read() : test if file read works
5. Test if db connection works
    => test_5db_connection() : test if db connection works
7. Test if excel data and db data operations are correct
    => test_7excel_db_operations() : test if excel data and db data operations are correct

"""


class CSDTest(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     print("setUpClass")
    
    def setUp(self) -> None:
        print("setUp")
        # create dummy excel dataframe and save it as test.xlsx
        #             status	clientMail	Message
        # id_no			
        # 1      	Accepted	a@gmail.com	this is approved
        import pandas as pd
        df = pd.DataFrame(
            {
                "id_no": [1, 2, 3, 4],
                "status": ["Accepted", "Rejected", "Accepted", "Accepted"],
                "clientMail": ["a@gmail.com", "b@gmail.com", "b@gmail.com", "c@gmail.com"],
                "Message": ["this is approved", "this is rejected", "this is approved", "this is approved"],
            }
        )
        df.set_index('id_no', inplace=True)
        self.fileName = "test.xlsx"
        df.to_excel(self.fileName)
        self.orgDf = df
        # temp Db setup
        load_dotenv()
        self.couch,self.Orgdb,self.orgdbdf= create_dummy_db(os.environ.get("COUCH_URL"),
        "test_db"+str(randint(0,100)))



    def tearDown(self) -> None:
        print("tearDown")
        # remove test.xlsx
        os.remove(self.fileName)
        # remove temp db
        self.couch.delete(self.Orgdb.name)
    
    # @classmethod
    # def tearDownClass(self) -> None:
    #     print("tearDownClass")
    
    def test_1env_vars(self):
        """ Test if environment variables are set """
        print("1.test_env_vars")
        self.assertTrue(".env" in os.listdir())

        # load env variables
        load_dotenv()
        """ 
            pathToBox="C:/Users/akshi/Box"
            fileName="sample.xlsx"
            COUCH_URL="http://root:1234@localhost:5984"
            COUCH_DB="csdtempdb"
        """
        vars = ["pathToBox", "fileName", "COUCH_URL", "COUCH_DB"]
        # print([os.environ.get(var) is not None   for var in vars])

        self.assertTrue(
            all(
                [os.environ.get(var) is not None   for var in vars]
                ))
        print("All environment variables are set")
             
    def test_2file_exists(self):
        print("2.test_file_exists")
        load_dotenv()
        pathToBox = os.environ.get("pathToBox")
        fileName = os.environ.get("fileName")
        self.assertTrue(os.path.exists(os.path.join(pathToBox, fileName)))
        print("File exists")

    def test_3file_format(self):
        print("3.test_file_format")
        load_dotenv()
        pathToBox = os.environ.get("pathToBox")
        fileName = os.environ.get("fileName")
        self.assertTrue(fileName.endswith(".xlsx"))
        print("File is in correct format")  
        #EOF test 3

    
    def test_4file_read(self):
        print("4.test_file_read")
        df = getExcelDf(self.fileName)
        # print(df)
        self.assertTrue(df.equals(self.orgDf))
        print("File read works")
        #EOF test 4
        

    def test_5db_connection(self):
        print("5.test_db_connection")
        load_dotenv()
        df = getDbDf(os.environ.get("COUCH_URL"), self.Orgdb.name)
        df.set_index('id_no', inplace=True)
        df= df[['status', 'clientMail', 'Message']]
        self.assertTrue(df.equals(self.orgdbdf))
        print("DB connection works")
        #EOF test 5
    
    def test_6excel_db_operations(self):
        print("6.test_excel_db_operations")

if __name__ == "__main__":
    unittest.main()    