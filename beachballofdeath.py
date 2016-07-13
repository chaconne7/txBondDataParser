# Categorize each file, find only the city files
# Convert each city to a 2D array
# Create simple that transforms the 2D array into an array of dicts or something else useful
# Try running the transformations on all of the city files
import pandas
import glob
from openpyxl.writer.excel import ExcelWriter

files = glob.glob("TX Bond Data/TX CITY Data/*.xls")

print files

def parseFile(filename):
    # Convert each file to a 2D array
    print filename

for file in files:
    parseFile(file)
