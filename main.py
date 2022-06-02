import couchdb,os
from dotenv import load_dotenv
import pandas as pd

load_dotenv() # Loads contents of the .env file into the script's environment


# Create the connection to the CouchDB database
couch = couchdb.Server(os.environ["COUCH_URL"])

# import os
path=os.environ["pathToBox"]
fileName = os.environ["fileName"] # Excel sheet File Name

# Excel sheet data
    # Read the Excel sheet

    # goto the file parent folder path
os.chdir(path)

    # check if the file exists
if fileName not in os.listdir():
    print("File not found")
    exit()
print("Located file ")

    # read the file
xlData = pd.read_excel(fileName,index_col=0)
print(xlData)

# read all records of database
    # read db name from .env file
dbName = os.environ["COUCH_DB"]
db = couch[dbName]

    # read all records of database
records = [db[id] for id in db]
# convert to pandas dataframe
dbDf= pd.DataFrame(records)

dbDf['id_no'] = dbDf['id_no'].astype(int)

    # merge the two dataframes together
mergedDf = dbDf[['id_no','status']].merge(xlData, on='id_no', how='outer',suffixes=('_db','_xl'))
print(mergedDf)
# mergedDf.head()

# Now filter the rows that have status_xl and status_db as different
# and save them to a new dataframe

# filter the dataframe
filteredDf = mergedDf[mergedDf['status_xl'] != mergedDf['status_db']]
print(filteredDf)

# Mail Module and Db Update
'''
    For each row in the filtered dataframe,
        # Mail Module
        Using the filtered dataframe, save an email in draft with the following content:
        1. Subject: "Status Update"
        2. Body: Message body containing status of project, and Message column in the filtered dataframe
        3. To: client email address from the filtered dataframe
        4. From: from os enviroment variable
        5. Attach: Same message body as the body of the email
        6. Save the email as a draft
        # Db Update
        Using the filtered dataframe, update the status and all other details of the project in the database
'''

