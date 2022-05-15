import couchdb
from dotenv import load_dotenv

load_dotenv()
couch = couchdb.Server()

import os
path=os.environ["pathToBox"]
fileName = os.environ["fileName"] 

os.chdir(path)

if fileName in os.listdir():
    print("Located file ")

import pandas as pd
xlData = pd.read_excel(fileName,index_col=0)
print(xlData)