import os
import numpy as np
import pandas as pd 

working_dir = "C:/users/user/desktop"
os.chdir(working_dir)

read_file_name = "repurchase_info.csv"
data = pd.read_csv(read_file_name)
data = data.drop(["claim_settle_dt"] , axis = 1)
data_columns = list(data.columns)
#print(data_columns)
counter = -1
for col in data_columns:
  counter += 1
  print(counter ,col)

numerical_col = [1,2,3,20,26]
data_numerical = data.iloc[:,numerical_col]

dummy_col = [19,24,25]
data_dummy = data.iloc[:,dummy_col]

binary_col = [i for i in range(1,27,1)]
exlusive_col = numerical_col + dummy_col

b_c_len = len(binary_col) 
for i in range(b_c_len):
  if binary_col[i] in exlusive_col:
    binary_col[i] = -1

while(-1 in binary_col):
  binary_col.remove(-1)

data_binary = data.iloc[:,binary_col]

print(data_numerical.columns)
print(data_dummy.columns)
print(data_binary.columns)

pd_num_col = list(data_numerical.columns)
for col in pd_num_col:
  average = data_numerical[col].mean()
  std = data_numerical[col].std()
  data_numerical[col] = (data_numerical[col] - average) / std

pd_dum_col = list(data_dummy.columns)
test = data_dummy.groupby(pd_dum_col[0])
add_columns = []
for col in pd_dum_col:
  dum_col = list(data_dummy.groupby(col).count().index)
  for n_col in dum_col:
    add_columns.append(n_col)

for col in add_columns:
  data_dummy[col] = 0


row = data_dummy.shape[0]
col = len(pd_dum_col)


counter = 0
for i in range(row):
  for j in range(col):
    value = data_dummy.iloc[i,j]
    index = col + add_columns.index(value)
    data_dummy.iloc[i,index] = 1
    counter += 1
    print(counter)

print(pd_dum_col)
data_dummy = data_dummy.drop(columns = pd_dum_col)
print(data_dummy.head(5))
write_file_name = "dummy_info.csv"
with open(write_file_name , "w" , encoding = "utf-8") as w_file:
  pass

data_dummy.to_csv(write_file_name , index = False , header = True)
print("Finished!")
