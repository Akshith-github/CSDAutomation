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

# Loads contents of the .env file into the script's environment
if __name__ == "__main__":
    if os.path.exists(".env"):
        load_dotenv()