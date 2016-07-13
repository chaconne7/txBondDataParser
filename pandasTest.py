import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

district_types = ("CCD", "CITY", "CNTY", "HHD", "OSD", "WD")
debt_types = ("Tax Backed Debt", "Revenue Debt", "Lease Obligation")
column_dictionary = {"CCD Tax Backed Debt": [], "CITY Tax Backed Debt": [], "CNTY": []}
frames = []

# include column for type!!

def addSheet(debtType, xls_file):
    df1 = xls_file.parse(debtType);
    
    # delete first seven rows
    df2 = df1.ix[6:]

    # insert year column, name columns                                                                                               
    df2.insert(3,'Year','2015')
    df2.columns = ['Govt ID #', 'Issuer/Government Name', 'County', 'Year', columns.split(',')];
    
     # reshape dataset
     df3 = pd.melt(df2, id_vars = ['Govt ID #', 'Issuer/Government Name', 'County', 'Year'], value_vars = ['Tax-Supported Debt Principal Outstanding as of 8/31/14','Tax-Supported Debt Interest Outstanding as of 8/31/14','Tax-Supported Debt Service Outstanding as of 8/31/14','2013 M&O Tax Rate','2013 I&S Tax Rate','2013 TOTAL Tax Rate','2013 Tax Year Assessed Valuation (AV)','Taxing District Population','Student HeadcountFall 2013 + Spring 2014 Flex','Debt Ratio: Tax Debt to Assessed Valuation (AV)','Debt Ratio: Tax Debt Service to AV','Debt Ratio: Tax Debt Per Capita','Debt Ratio: Tax Debt Per Student Headcount'])

     # get rid of NaN rows                                                                                                               
     df4 = df3.dropna(subset=['Govt ID #']) 

     # fill in non-null values with 0                                                                                                   
     df5 = df4.fillna(0)
     frames.append(df5)



for year in range (2003, 2016):
    for districtType in district_types:
        filepath = 'TX Bond Data/TX %s Data/%s%s.xls' % (districtType, toString(year), districtType)
        print(filepath)
        xls_file = pd.ExcelFile(filepath)
        # go through each type in the sheet, so call helper function three times
        for debtType in debtTypes:
            addSheet(debtType, districtType, xls_file)
concatDF = pd.concat(frames)
concatDF.to_csv('concatDataTest.csv', sep=',')
print(concatDF)
