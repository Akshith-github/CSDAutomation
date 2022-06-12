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

# import libraries
import os 
from dotenv import load_dotenv
import pandas as pd




# Loads contents of the .env file into the script's environment
# if __name__ == "__main__":

try:
    load_dotenv() # Loads contents of the .env file into the script's environment
    # print(os.environ["COUCH_URL"])
    # print(os.environ["COUCH_DB"])
    # print(os.environ["pathToBox"])
    # print(os.environ["fileName"])
    # print(os.environ["fromEmail"])
    # print(os.environ["toEmail"])
    # print(os.environ["password"])
    # print(os.environ["smtpServer"])
    # print(os.environ["smtpPort"])
except Exception as e:
    print("Error: ",e)
    exit()

# Get Dfs from Excel and DB
from utils.excelUtils import getExcelDf

try:
    xlDf = getExcelDf(os.path.join(os.environ["pathToBox"],os.environ["fileName"]))
except Exception as e:
    print("failed to get excel dataframe")
    print("Error: ",e)

    exit()

from utils.dbUtils import getDbDf

try:
    dbDf = getDbDf(os.environ["COUCH_URL"],os.environ["COUCH_DB"])
except Exception as e:
    print("failed to get db dataframe")
    print("Error: ",e)
    exit()

# gen diff df

from utils.reportUtils import diffDf
try:
    diffDf = diffDf(dbDf,xlDf)
except Exception as e:
    print("failed to generate diff dataframe")
    print("Error: ",e)
    exit()

# prereport filtering of diffDf records
def PreReport(diffDf):
    # New records in DB
    # status_db will be ""
    # status_xl will be something
    for i in diffDf.index:
        # new records in Xl
        if diffDf.loc[i]["status_db"] == "" :
            for attr in [ 'ProjectTitle_db', 'ReportNumber_db', 'Date_db', 
                        'ToName_db', 'ProjectDetails_db', 'status_db', 
                        'Message_db', 'Incharge_db', 'clientMail_db']:
                diffDf.loc[i][attr] = "NA"
        # records in DB but not in Xl
        if diffDf.loc[i]["status_xl"] == "" :
            diffDf.drop(i,inplace=True)
    return diffDf

try:
    diffDf = PreReport(diffDf)
except Exception as e:
    print("failed to prereport processing")
    print("Error: ",e)
    exit()

# for i in diffDf.index:
#     print(diffDf.loc[i][["status_xl","status_db"]])

try:
    RepNum = pd.read_excel(os.path.join(os.environ["pathToBox"],os.environ["varFile"]))
    RepNum=RepNum[RepNum['var']=='ReportNumber']['value'][0]
    RepNum=RepNum+1
except Exception as e:
    print("failed to get report number")
    print("Error: ",e)
    exit()

def updateRepNum(RepNum,log=False):
    try:
        RepNum = str(RepNum)
        upDf = pd.read_excel(os.path.join(os.environ["pathToBox"],os.environ["varFile"]),index_col=0)
        if 'var' in upDf.columns:
            upDf.set_index('var',inplace=True)
        upDf.loc['ReportNumber'] = RepNum
        if log:
            print("updating reportNum to ",RepNum," at ",os.path.join(os.environ["pathToBox"],os.environ["varFile"]))
        upDf.to_excel(os.path.join(os.environ["pathToBox"],os.environ["varFile"]))
        # print(upDf)
    except Exception as e:
        print("failed to update report number")
        print("Error: ",e)
        exit()
    return RepNum

# generate reports
from utils.reportUtils import genReport
try:
    for id_no in diffDf.index:
        rec = diffDf.loc[id_no]
        fileName="Report_"+str(RepNum)+"_"+rec['clientMail_xl']+".docx"
        # in tmp folder of box
        # print(fileName)
        if(os.path.exists(os.path.join(os.environ["pathToBox"],"tmp",fileName))):
            os.remove(os.path.join(os.environ["pathToBox"],"tmp",fileName))
        genReport(rec.to_dict(),os.path.join(os.environ["pathToBox"],"tmp",fileName))
        updateRepNum(RepNum)
        RepNum = RepNum+1

except Exception as e:
    print("failed to generate reports")
    print("Error: ",e)
    exit()

