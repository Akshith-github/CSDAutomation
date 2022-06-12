import pandas as pd

def diffDf(dbDf,xlData):
    import pandas as pd
    mergedDf = dbDf.merge(
        xlData, left_index=True, right_index=True, how='outer',suffixes=('_db','_xl'))
    mergedDf.fillna('',inplace=True)
    filteredDf = mergedDf[mergedDf['status_xl'] != mergedDf['status_db']]
    return filteredDf

def genReport(DataRecDict,resDocName):
    from docxtpl import DocxTemplate
    import os
    doc = DocxTemplate(os.path.join(os.environ["pathToBox"],"template.docx"))
    context = DataRecDict
    context["Subject"] = "Report for " + context["ToName_xl"] + " about " + context["ProjectTitle_xl"]
    import datetime
    context["Date"] = datetime.datetime.now().strftime("%d-%m-%Y")
    context["Time"] = datetime.datetime.now().strftime("%H:%M:%S")
    doc.render(context)
    doc.save(os.path.join(os.environ["pathToBox"],resDocName))