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
            "id_no": [1, 2, 3, 4],
            "status": ["Accepted", "Rejected", "Accepted", "Accepted"],
            "clientMail": ["a@gmail.com","a@gmail.com","a@gmail.com","a@gmail.com"],
            "Message": ["this is approved","this is rejected","this is approved","this is approved"]
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
    