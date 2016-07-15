import pandas as pd
import numpy as np
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# referenced this StackOverflow answer on flattening column: http://stackoverflow.com/a/29437514

def get_year(filename):
    return filename[:4]

def get_gov_type(filename):
    return filename[4:-4]

def merge_header_rows(df):
    rows, cols, = df.shape
    for coli in range(0, cols - 3):
        new_header_val = ''
        for rowi in range(0, 5):
            val = str(df.iloc[rowi,coli + 3]).encode('utf-8')
            if (val != "nan"):
                new_header_val += val + " "
        df.rename(columns={df.columns.values[coli + 3]: new_header_val}, inplace=True)

    df2 = df.iloc[5:]
    return df2
    
def clean_sheet(xls_file, sheet, year, gov_type):
    df1 = xls_file.parse(sheet, header = None, index_col = None)

    # drop empty rows
    df1.dropna(how="all", inplace=True)

    # drop first two rows
    df2 = df1.iloc[2:]

    # merge headers
    df3 = merge_header_rows(df2)

    # name first three columns
    df3.rename(columns={df3.columns.values[0]: 'Govt ID #', df3.columns.values[1]: 'Issuer/Government Name', df3.columns.values[2]: 'County'}, inplace=True)

    # insert gov type and year columns
    df3.insert(3, 'Government Type', gov_type)
    df3.insert(4, 'Year', year)

    # debugging: print out column values
#    mi = df3.columns
 #   print("Values: " + ', '.join([str(x).encode('utf-8') for x in mi.values]))

    # handle last rows
    df4 = df3[df3['Govt ID #'].notnull()]

    # pivot columns 5-on
    df5 = pd.melt(df4, id_vars=['Govt ID #', 'Issuer/Government Name', 'County', 'Government Type', 'Year'])

    # fill in non-null values with 0
    df6 = df5.fillna(0)

    df7 = df6.ix[1:]
    print('REACHED')
    return df7

frames = []
for folder in os.listdir('TX Bond Data'):
    if not folder.startswith('.'):
        for file in os.listdir('TX Bond Data/%s' % folder):
            gov_type = get_gov_type(file)
            if not file.startswith('.'):
                year = get_year(file)
#                gov_type = get_gov_type(file)
                filepath = 'TX Bond Data/%s/%s' % (folder, file)
                xls_file = pd.ExcelFile(filepath, index_col=None)
                print(filepath)
                # loop through each sheet in the file
                for sheet in xls_file.sheet_names:
                    if not (sheet == "Total Debt Outstanding" or sheet == "Total"):
                        df = clean_sheet(xls_file, sheet, year, gov_type)
                        frames.append(df)
                        
# concatenate for master sheet
concatDF = pd.concat(frames)
concatDF.to_csv("masterTXBondData.csv", sep=',')
