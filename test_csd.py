# python test_csd.py

import unittest

from numpy import diff
from run import *
from utils.excelUtils import getExcelDf
from utils.dbUtils import getDbDf,create_dummy_db
from utils.reportUtils import diffDf,genReport

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
8. Test Case for status message updates:
    => test_8status_message_new() : test Case for status message updates
         : new xlsx records in new db
         Create new db , Create new xlsx file with new records
            Read new xlsx file and compare with db
            Update status message in db
            Read db and compare with xlsx
"""


class CSDTest(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     print("setUpClass")
    
    def setUp(self) -> None:
        print("=>setUp",end=" ")
        # create dummy excel dataframe and save it as test.xlsx
        #             status	clientMail	Message
        # id_no			
        # 1      	Accepted	a@gmail.com	this is approved
        import pandas as pd
        df = pd.DataFrame(
            {
        "id_no": [1,2,3,4,5,6,7,8,9,10],
        "ProjectTitle": ["Project1","Project2","Project3","Project4","Project5","Project6","Project7","Project8","Project9","Project10"],
        "ReportNumber": ["Report1","Report2","Report3","Report4","Report5","Report6","Report7","Report8","Report9","Report10"],
        "ToName": ["To1","To2","To3","To4","To5","To6","To7","To8","To9","To10"],
        "ProjectDetails": ["ProjectDetails1","ProjectDetails2","ProjectDetails3","ProjectDetails4","ProjectDetails5","ProjectDetails6","ProjectDetails7","ProjectDetails8","ProjectDetails9","ProjectDetails10"],
        "status": ["status1","status2","status3","status4","status5","status6","status7","status8","status9","status10"],
        "Date": ["01-01-2020","02-02-2020","03-03-2020","04-04-2020","05-05-2020","06-06-2020","07-07-2020","08-08-2020","09-09-2020","10-10-2020"], 
        "Message": ["Message1","Message2","Message3","Message4","Message5","Message6","Message7","Message8","Message9","Message10"],
        "Incharge": ["Incharge1","Incharge2","Incharge3","Incharge4","Incharge5","Incharge6","Incharge7","Incharge8","Incharge9","Incharge10"],
        "clientMail": ["a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com"]
    }
        )
        df.set_index('id_no', inplace=True)
        self.fileName = "test.xlsx"
        df.to_excel(self.fileName)
        self.orgDf = df
        self.dfColumns = ['ProjectTitle', 'ReportNumber', 'ToName', 'ProjectDetails', 'status',
       'Date', 'Message', 'Incharge', 'clientMail']
        # temp Db setup
        load_dotenv()
        self.couch,self.Orgdb,self.orgdbdf= create_dummy_db(os.environ.get("COUCH_URL"),
        "test_db"+str(randint(0,100)))
        print("setUp<=")



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
        # print("File exists")

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
        # print(df.columns)
        # df.set_index('id_no', inplace=True)
        df= df[self.dfColumns]
        # print(df)
        
        self.assertTrue(df.equals(self.orgdbdf))
        print("DB connection works")
        #EOF test 5
    
    def test_6excel_db_operations_case1(self):
        # case 1 No change in status
        print("6.test_excel_db_operations case 1")
        #create new empty db
        load_dotenv()
        #load excel data
        xldf = getExcelDf(self.fileName)
        dbdf = getDbDf(os.environ.get("COUCH_URL"), self.Orgdb.name)
        dbdf = dbdf[self.dfColumns]
        # print(diffDf(dbdf,xldf))
        self.assertTrue(diffDf(dbdf,xldf).empty)

    def test_7excel_db_operations_case2(self):
        # case 2 New records in excel
        print("7.test_excel_db_operations case 2")
        #create new empty db
        load_dotenv()
        #load excel data
        xldf = getExcelDf(self.fileName)
        # dbdf = getDbDf(os.environ.get("COUCH_URL"), self.Orgdb.name)
        # dbdf = dbdf[self.dfColumns]
        # insert new records in excel
        # print(xldf.columns)
        newRec = pd.DataFrame(
            {
                "id_no": [11],
                "ProjectTitle": ["ProjectTitle11"],
                "ReportNumber": ["ReportNumber11"],
                "ToName": ["ToName11"],
                "ProjectDetails": ["ProjectDetails11"],
                "status": ["status11"],
                "Date": ["01-01-2020"],
                "Message": ["Message11"],
                "Incharge": ["Incharge11"],
                "clientMail": ["cd@gmail.com"]
            },
        )
        newRec.set_index('id_no', inplace=True)
        xldf = pd.concat([xldf,newRec])
        xldf.to_excel(self.fileName)

        # Now use diffdf and check if new records are inserted
        dbdf = getDbDf(os.environ.get("COUCH_URL"), self.Orgdb.name)
        dbdf = dbdf[self.dfColumns]
        dfRes=diffDf(dbdf,xldf)
        # print(dfRes.iloc[0].to_dict())
        # assert one new record is inserted
        self.assertEqual(len(dfRes),1)
        
    def test_7excel_db_operations_case3(self):
        # case 3 Record deleted from xl => no update
        print("7.test_excel_db_operations case 3")
        #create new empty db
        load_dotenv()
        #load excel data
        xldf = getExcelDf(self.fileName)
        xldf.drop([1])
        xldf.to_excel(self.fileName)
        xlDf = getExcelDf(self.fileName)
        dbdf = getDbDf(os.environ.get("COUCH_URL"), self.Orgdb.name)
        dbdf = dbdf[self.dfColumns]
        dfRes=diffDf(dbdf,xlDf)
        # assert no update
        self.assertTrue(dfRes.empty)
    
    def test_7excel_db_operations_case4(self):
        # case 4 Record updated in xl => update in db
        print("7.test_excel_db_operations case 4")
        load_dotenv()
        #load excel data
        xldf = getExcelDf(self.fileName)
        xldf.iloc[1]['ProjectTitle'] = "ProjectTitle1_1"
        xldf.iloc[1]['status'] = "status1_1"
        # new records in excel
        newRec = pd.DataFrame(
            {
                "id_no": [11],
                "ProjectTitle": ["ProjectTitle11"],
                "ReportNumber": ["ReportNumber11"],
                "ToName": ["ToName11"],
                "ProjectDetails": ["ProjectDetails11"],
                "status": ["status11"],
                "Date": ["01-01-2020"],
                "Message": ["Message11"],
                "Incharge": ["Incharge11"],
                "clientMail": ["cd@gmail.com"]
            },
        )
        newRec.set_index('id_no', inplace=True)
        xldf = pd.concat([xldf,newRec])

        dbDf = getDbDf(os.environ.get("COUCH_URL"), self.Orgdb.name)
        dbDf = dbDf[self.dfColumns]
        dfRes=diffDf(dbDf,xldf)
        # assert two records are updated
        self.assertEqual(len(dfRes),2)
        





        

if __name__ == "__main__":
    unittest.main()