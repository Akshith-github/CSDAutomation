import pandas as pd
import os

os.chdir("C:/Users/akshi/Box")
df1 = pd.DataFrame(columns=["id_no","status","clientMail","Message"],)
df1.set_index('id_no')
print(df1)
print(df1.columns)
df1.to_excel("sample.xlsx",index=0)