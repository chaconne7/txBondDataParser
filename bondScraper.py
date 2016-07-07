import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_year(filename):
    return filename[:4]
    
def get_district_type(filename):
    return filename[4:-4]

for folder in os.listdir('TX Bond Data'):
    if not folder.startswith('.'):
        for file in os.listdir('TX Bond Data/%s' % folder):
            if not file.startswith('.'):
                print file
                print(get_year(file))
                print file
                print(get_district_type(file))
