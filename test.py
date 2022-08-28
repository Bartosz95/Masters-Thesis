from myTSR import MyTSR
from test_TSR import TestTSR
import pandas as pd
import xlrd


test_tsr = TestTSR([0, 1, 2], "images/Benchmark")
df, df_percent, data = test_tsr.test()

df.to_csv('results.csv')
df_percent.to_csv('results_percent.csv')
print(df_percent)

#cameras = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2] ]
#old = pd.read_excel('wyniki.xlsx', 'Arkusz2', na_values=['NA'])

#old.set_value(0, 0, 1111, True)
#old.update(old.get(0,0))
#print(old.get('Blue'))
#for camera in cameras:





#print(old.head())
#
#
