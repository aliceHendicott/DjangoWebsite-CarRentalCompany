import pandas as panda
import numpy as np
import datetime

sdata = panda.read_csv('StoresTable.csv')

sdata = sdata.replace('  ', '', regex=True)

sdata.to_csv('UpdatedStoresTable.csv', index=False)
