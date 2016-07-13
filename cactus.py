import pandas as pd
import numpy as np
import os
import sys
from openpyxl.writer.excel import ExcelWriter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# referenced this StackOverflow answer on flattening column: http://stackoverflow.com/a/29437514

def get_year(filename):
    return filename[:4]

def get_gov_type(filename):
    return filename[4:-4]

def merge_header_rows(df):
    for i in range(3, len(df.columns) - 2):
        new_header_val = ''
        for j in range(0, 5):
            val = str(df.iat[j,i])
            if (val != "nan"):
                new_header_val += val + " "
        #df.iat[4,i] = new_header_val
        df.rename(columns={df.columns.values[i]: new_header_val}, inplace=True)
    df2 = df.ix[6:]
    return df2
    
def clean_sheet(xls_file, sheet, year, gov_type):
    df1 = xls_file.parse(sheet, header = None, index_col = None)

    # drop first two rows
    df2 = df1.ix[2:]

    # merge headers
    df3 = merge_header_rows(df2)

    df3.rename(columns={df3.columns.values[0]: 'Govt ID #', df3.columns.values[1]: 'Issuer/Government Name', df3.columns.values[2]: 'County'}, inplace=True)

    df3.insert(3, 'Government Type', gov_type)
    df3.insert(4, 'Year', year)

    df4 = df3.drop(df3.index[[6]])
    df4.to_csv("peyroux.csv", sep=",")
    print("REACHED")
    sys.exit()
    # debugging: print out column values
    mi = df3.columns
    print("Values: " + ', '.join([str(x) for x in mi.values]))

    # handle last rows
    df3 = df3[df3['Govt ID #'].notnull()]

    # pivot columns 5-on
   # df3 = df2.rename(columns={' Issuer/Government Name':'Issuer/Government Name', ' County':'County'})
    df4 = pd.melt(df3, id_vars=['Govt ID #', 'Issuer/Government Name', 'County', 'Government Type', 'Year'])

    # fill in non-null values with 0
    df5 = df4.fillna(0)

    df5.to_csv("baebae.csv", sep=',', encoding='utf-8')
    print('REACHED')
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
