import pandas as pd
import numpy as np
import os

from openpyxl.writer.excel import ExcelWriter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# referenced this StackOverflow answer on flattening column: http://stackoverflow.com/a/29437514

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

# read sheet to a dataframe, drop any empty rows, export to csv
# and then reimport as an excel file
def drop_empty_rows(xls_file):
    dftest = xls_file.parse(sheet, index_col=None, header=None)
    dftest.dropna(how="all", inplace=True)
    writer = pd.ExcelWriter('pandassimple.xlsx', engine='xlsxwriter')
    dftest.to_excel(writer, sheet_name = 'Sheet1')
    xls_file = pd.ExcelFile(filepath, index_col=None)
    return xls_file

def clean_sheet(xls_file, sheet, year, gov_type):
    fixed_file = drop_empty_rows(xls_file)

    df1 = fixed_file.parse(sheet, header=[2,3,4,5,6], index_col=None)

    df1.columns = df1.columns.map(flattenHierarchicalCol)
 
    # insert year and government type columns
    df1.insert(2, 'Government Type', gov_type)
    df1.insert(3, 'Year', year)

    # name first column and convert it from index to regular column
    df1.index.name = 'Govt ID #'
    df1.reset_index(level=0, inplace=True)

    # debugging: print out column values
    mi = df1.columns
#    print("Values: " + ', '.join([str(x) for x in mi.values]))
    
    # handle last rows
    df2 = df1[df1['Govt ID #'].notnull()]

    # pivot columns 5-on
    df3 = df2.rename(columns={' Issuer/Government Name':'Issuer/Government Name', ' County':'County'}) 
    df4 = pd.melt(df3, id_vars=['Govt ID #', 'Issuer/Government Name', 'County', 'Government Type', 'Year'])

    # fill in non-null values with 0                                      
    df5 = df4.fillna(0)

    df5.to_csv("baebae.csv", sep=',', encoding='utf-8')
    print("REACHED")
    return df3


frames = []
for folder in os.listdir('TX Bond Data'):
    if not folder.startswith('.'):
        for file in os.listdir('TX Bond Data/%s' % folder):
            if not file.startswith('.') and not (get_gov_type(file) == "CNTY" or get_gov_type(file) == "HHD"):
            #or get_gov_type(file) == "ISD"):
                year = get_year(file)
                gov_type = get_gov_type(file)
                filepath = 'TX Bond Data/%s/%s' % (folder, file)
                xls_file = pd.ExcelFile(filepath, index_col=None)
                print(filepath)
                # loop through each sheet in the file
                for sheet in xls_file.sheet_names:
                    if not (sheet == "Total Debt Outstanding"):
                        df = clean_sheet(xls_file, sheet, year, gov_type)
                        frames.append(df)

# concatenate for master sheet
concatDF = pd.concat(frames) 
concatDF.to_csv("masterTXBondData.csv", sep=',')               
