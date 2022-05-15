import pandas as pd
import os
'''
This script is used to create a Base XLSX file intended to be used as a template for the 
CSD automation

It contains the following columns:
    1. id_no
    2. status
    3.clientMail
    4.Message
'''


os.chdir("C:/Users/akshi/Box")
df1 = pd.DataFrame(columns=["id_no","status","clientMail","Message"],)
df1.set_index('id_no')
print(df1)
print(df1.columns)
df1.to_excel("sample.xlsx",index=0)