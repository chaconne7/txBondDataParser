import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_year(filename):
    return filename[:4]
    
def get_gov_type(filename):
    return filename[4:-4]

def clean_sheet(filename, year, gov_type):
    # merge cells in all columns after first five?
    # remove first six rows
    df1 = xls_file.parse(gov_type)

    # insert year and governemnt type columns
    df2 = df1.insert(3, 'Government Type', gov_type)
    df3 = df2.insert(4, 'Year', year)
    
    

for folder in os.listdir('TX Bond Data'):
    if not folder.startswith('.'):
        for file in os.listdir('TX Bond Data/%s' % folder):
            if not file.startswith('.'):
                year = get_year(file)
                gov_type = get_gov_type(file)
                filepath = 'TX Bond Data/%s/%s' % (folder, file)
                xls_file = pd.ExcelFile(filepath)
                df = clean_sheet(xls_file, year, district_type)
                
                
