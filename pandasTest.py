import pandas as pd
import numpy as np

# generalize by putting in a for loop and making year in xls_file and df insert statement an index
xls_file = pd.ExcelFile('TX Bond Data/TX CCD Data/15CCDTRLP.xls')
xls_file.sheet_names

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

tdDF1 = xls_file.parse('Tax-Supported Debt')

# delete first seven rows
tdDF2 = tdDF1.ix[6:]

# insert year column and name columns
tdDF2.insert(3,'Year','2015')
tdDF2.columns = ['Govt ID #', 'Issuer/Government Name', 'County', 'Year', 'Tax-Supported Debt Principal Outstanding as of 8/\
31/14','Tax-Supported Debt Interest Outstanding as of 8/31/14','Tax-Supported Debt Service Outstanding as of 8/31/14','2013 M&O Tax Rate','2013 I&S Tax Rate','2013 TOTAL Tax Rate','2013 Tax Year Assessed Valuation (AV)','Taxing District Population','Student Headcount Fall 2013 + Spring 2014 Flex','Debt Ratio: Tax Debt to Assessed Valuation (AV)','Debt Ratio: Tax Debt Service to AV','Debt Ratio: Tax Debt Per Capita','Debt Ratio: Tax Debt Per Student Headcount']

# reshape dataset
tdDF3 = pd.melt(tdDF2, id_vars = ['Govt ID #', 'Issuer/Government Name', 'County', 'Year'], value_vars = ['Tax-Supported Debt Principal Outstanding as of 8/31/14','Tax-Supported Debt Interest Outstanding as of 8/31/14','Tax-Supported Debt Service Outstanding as of 8/31/14','2013 M&O Tax Rate','2013 I&S Tax Rate','2013 TOTAL Tax Rate','2013 Tax Year Assessed Valuation (AV)','Taxing District Population','Student Headcount Fall 2013 + Spring 2014 Flex','Debt Ratio: Tax Debt to Assessed Valuation (AV)','Debt Ratio: Tax Debt Service to AV','Debt Ratio: Tax Debt Per Capita','Debt Ratio: Tax Debt Per Student Headcount'])

# get rid of NaN rows
tdDF4 = tdDF3.dropna(subset=['Govt ID #'])

#print(tdDF4)

# fill in non-null values with 0
tdDF5 = tdDF4.fillna(0)

#print(tdDF5)

#---------------- REVENUE DEBT ---------------------------
rdDF1 = xls_file.parse('Revenue Debt')

# delete first seven rows                                                                                                                         
rdDF2 = rdDF1.ix[6:]

# insert year column and name columns                                                                                                            
rdDF2.insert(3,'Year','2015')
rdDF2.columns = ['Govt ID #', 'Issuer/Government Name', 'County', 'Year', 'Revenue Debt Principal Outstanding as of 8/31/14', 'Revenue Debt Interest Outstanding as of 8/31/14', 'Revenue Debt Service Outstanding as of 8/31/14', 'Taxing District Population', 'Student Headcount Fall 2013 + Spring 2014 Flex', 'Debt Ratio: Revenue Debt per Capita', 'Debt Ratio: Revenue Debt Per Student Headcount']

# reshape dataset                                                                                                                                  
rdDF3 = pd.melt(rdDF2, id_vars = ['Govt ID #', 'Issuer/Government Name', 'County', 'Year'], value_vars = ['Revenue Debt Principal Outstanding as of 8/31/14', 'Revenue Debt Interest Outstanding as of 8/31/14', 'Revenue Debt Service Outstanding as of 8/31/14', 'Taxing District Population', 'Student Headcount Fall 2013 + Spring 2014 Flex', 'Debt Ratio: Revenue Debt per Capita', 'Debt Ratio: Revenue Debt Per Student Headcount'])

# get rid of NaN rows                                                                                                                            
rdDF4 = rdDF3.dropna(subset=['Govt ID #'])

#print(tdDF4)                                                                                                                                      
# fill in non-null values with 0                                                                                                                  
rdDF5 = rdDF4.fillna(0)
print(rdDF5)
