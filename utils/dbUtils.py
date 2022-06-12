import couchdb,os

# function that creartes a connection to couchdb
def create_connection(url,dbName=None):
    # create the connection to couchdb
    couch = couchdb.Server(url)
    # create the database
    if dbName == None:
        return couch
    else:
        db = couch[dbName]
        return couch,db

# function that creates dummy db and returns couch,db,df
def create_dummy_db(url,dbName):
    # create the connection to couchdb
    couch = create_connection(url)
    # create dummy dataframe
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
    # create the database
    db = couch.create(dbName)
    # save the dataframe to database
    for index,row in df.iterrows():
        tmpDict = row.to_dict()
        tmpDict['id_no'] = index
        # print(tmpDict)
        db.save(tmpDict)
    return couch,db,df


# function that returns the dataframe of the database
def get_dataframe_from_db(db):
    # read all records of database
    records = [db[id] for id in db]
    # convert to pandas dataframe
    import pandas as pd
    dbDf= pd.DataFrame(records)
    dbDf['id_no'] = dbDf['id_no'].astype(int)
    return dbDf

# function that returns df of the database <=url,dbName => dbDf
def getDbDf(url,dbName):
    # create the connection to couchdb
    couch,db = create_connection(url,dbName)
    # read all records of database
    records = [db[id] for id in db]
    # convert to pandas dataframe
    import pandas as pd
    dbDf= pd.DataFrame(records)
    dbDf['id_no'] = dbDf['id_no'].astype(int)
    dbDf.set_index('id_no', inplace=True)
    return dbDf














#
#  def save_email(db,df):
#     # create the email
#     email = {
#         "subject": "Status Update",
#         "body": "Hi,\n\nYour status has been updated.\n\nRegards,\n\nTeam",
#         "to": df['clientMail'],
#         "from": os.environ["MAIL_USERNAME"],
#         "attachments": [
#             {
#                 "name": "status.txt",
#                 "content": df['status']
#             }
#         ]
#     }
#     # save the email to draft

# now lets read