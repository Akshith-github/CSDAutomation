""" 
Tasks:
1. Install box in your laptop and try to access from python script. # done instatllation manually

2. Upload a sample excel sheet to box (as discussed) and read it from python script.
"""

"""
Code Modules:
    1) Read Excel File => return dataframe

"""

import os
import pandas as pd

def getExcelDf(filePath):
    # check if path exists
    if os.path.exists(filePath):
        # print("Located file ")
        # check if file is in correct format
        if filePath.endswith(".xlsx"):
            # print("Located excel file")
            # read excel file
            df = pd.read_excel(filePath)
            df.set_index("id_no", inplace=True)
            return df
        else:
            print("File is not in correct format")
            # raise error
            # raise Exception("File is not in correct format")
            return None
    else:
        print("File not found")
        # raise error
        # raise Exception("File not found")
        return None
