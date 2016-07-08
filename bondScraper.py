import pandas as pd
import numpy as np
import os
import sys

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# referenced this StackOverflow answer for flattening column: http://stackoverflow.com/a/29437514

def get_year(filename):
    return filename[:4]
    
def get_gov_type(filename):
    return filename[4:-4]

def flattenHierarchicalCol(col,sep = ' '):
    if not type(col) is tuple:
        return col
    else:
        new_col = ''
        for leveli,level in enumerate(col):
            if not (level == '' or str(level).startswith("Unnamed")):
                if not leveli == 0:
                    new_col += str(sep)
                new_col += str(level)
        return new_col

def clean_sheet(xls_file, sheet, year, gov_type):

    # remove first six rows
    df1 = xls_file.parse(sheet, header=[2,3,4,5,6], index_col=None)

    df1.columns = df1.columns.map(flattenHierarchicalCol)
 
    # insert year and government type columns
    df1.insert(2, 'Government Type', gov_type)
    df1.insert(3, 'Year', year)

    # name first column and convert it from index to regular column
    df1.index.name = 'Govt ID #'
    df1.reset_index(level=0, inplace=True)

    # debugging: print out column values
    mi = df1.columns
    print("Values: " + ', '.join([str(x) for x in mi.values]))
    
    # handle last rows
    df2 = df1[df1['Govt ID #'].notnull()]

    # pivot columns 5-on
    df3 = df2.rename(columns={' Issuer/Government Name':'Issuer/Government Name', ' County':'County'}) 
    df4 = pd.melt(df3, id_vars=['Govt ID #', 'Issuer/Government Name', 'County', 'Government Type', 'Year'])

    df4.to_csv("bangbangbang.csv", sep=',')
    sys.exit()


frames = []
for folder in os.listdir('TX Bond Data'):
    if not folder.startswith('.'):
        for file in os.listdir('TX Bond Data/%s' % folder):
            if not file.startswith('.'):
                year = get_year(file)
                gov_type = get_gov_type(file)
                filepath = 'TX Bond Data/%s/%s' % (folder, file)
                xls_file = pd.ExcelFile(filepath, index_col=None)
                
                # loop through each sheet in the file
                for sheet in xls_file.sheet_names:
                    df = clean_sheet(xls_file, sheet, year, gov_type)
                    frames.append(df)

# concatenate for master sheet
concatDF = pd.concat(frames) 
concatDF.to_csv("masterTXBondData.csv", sep=',')               
