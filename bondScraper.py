
import pandas as pd
import numpy as np
import os
import sys

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_year(filename):
    return filename[:4]
    
def get_gov_type(filename):
    return filename[4:-4]

def merge_columns(df):
    strJoin = lambda x:" ".join(x.astype(str))
    dfmerged = df[0:6].apply(strJoin)
    print(dfmerged)
    return dfmerged
    
def flattenHierarchicalCol(col,sep = ' '):
    if not type(col) is tuple:
        return col
    else:
        new_col = ''
        for leveli,level in enumerate(col):
            if not level == '':
                if not leveli == 0:
                    new_col += str(sep)
                if not (str(sep).startswith("Unnamed")):
                    new_col += str(level)
        return new_col

def clean_sheet(xls_file, sheet, year, gov_type):
    # merge cells in all columns after first five?
    # remove first six rows
    df1 = xls_file.parse(sheet, header=[2,3,4,5,6]);

    
    df1.columns = df1.columns.map(flattenHierarchicalCol)
    mi = df1.columns
    print("Values: " + ', '.join([str(x) for x in mi.values]))
    sys.exit();
 
    # insert year and government type columns
    df1.insert(3, 'Government Type', gov_type)
    df1.insert(4, 'Year', year)
    
    # merge multi-row headings in columns 5 onward
    df2 = merge_columns(df1)
    
    # pivot columns 5-on

    # get rid of NaN rows

    # fill in non-null values with 0

for folder in os.listdir('TX Bond Data'):
    if not folder.startswith('.'):
        for file in os.listdir('TX Bond Data/%s' % folder):
            if not file.startswith('.'):
                year = get_year(file)
                gov_type = get_gov_type(file)
                filepath = 'TX Bond Data/%s/%s' % (folder, file)
                xls_file = pd.ExcelFile(filepath)
                
                # loop through each sheet in the file
                for sheet in xls_file.sheet_names:
                    df = clean_sheet(xls_file, sheet, year, gov_type)
    
                # concatenate to master sheet
                
