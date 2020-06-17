import os
import numpy as np
import pandas as pd 

working_dir = "C:/users/user/desktop"
os.chdir(working_dir)

read_file_name1 = "repurchase_info.csv"
read_file_name2 = "dummy_info.csv"
read_file_name3 = "illness_code.csv"
data_info = pd.read_csv(read_file_name1)
data_dummy = pd.read_csv(read_file_name2)
data_illness = pd.read_csv(read_file_name3)

data_info = data_info.drop(["claim_settle_dt"] , axis = 1)
data_info_columns = list(data_info.columns)

counter = -1
for col in data_info_columns:
  counter += 1
  print(counter ,col)

label_col = [0]
data_label = data_info.iloc[:,label_col]

numerical_col = [1,2,3,20,26]
data_numerical = data_info.iloc[:,numerical_col]

dummy_col = [19,24,25]
pd_dum_col = list(data_dummy.columns)

binary_col = [i for i in range(1,27,1)]
exlusive_col = numerical_col + dummy_col

b_c_len = len(binary_col) 
for i in range(b_c_len):
  if binary_col[i] in exlusive_col:
    binary_col[i] = -1

while(-1 in binary_col):
  binary_col.remove(-1)


data_binary = data_info.iloc[:,binary_col]
pd_bin_col = list(data_binary.columns)

print(data_numerical.columns)
print(data_dummy.columns)
print(data_binary.columns)

pd_num_col = list(data_numerical.columns)
for col in pd_num_col:
  average = data_numerical[col].mean()
  std = data_numerical[col].std()
  data_numerical[col] = (data_numerical[col] - average) / std

concat_list1 = [data_label , data_numerical , data_illness , data_dummy , data_binary]
p_and_b = pd.concat(concat_list1 , axis = 1)

concat_list2 = [data_label , data_numerical[["REIMBURSED_YR_TW" , "ternure_m" , "AGE"]] ,  data_illness , data_binary["GENDER"]]
personal = pd.concat(concat_list2 , axis = 1)

print(pd_bin_col)
print(pd_dum_col)
concat_list3 = [data_label ,data_numerical["CLIENT_INCOME"] , data_dummy[pd_dum_col[7:-5]] ,data_binary[pd_bin_col[:-1]]]
behavioral = pd.concat(concat_list3 , axis = 1)
print(p_and_b.head(5))
print(personal.head(5))
print(behavioral.head(5))


write_file_name1 = "personal_and_behavioral.csv"
write_file_name2 = "personal.csv"
write_file_name3 = "behavioral.csv"
with open(write_file_name1 , "w" , encoding = "utf-8") as w_file:
  pass
with open(write_file_name2 , "w" , encoding = "utf-8") as w_file:
  pass
with open(write_file_name3 , "w" , encoding = "utf-8") as w_file:
  pass

p_and_b.to_csv(write_file_name1 , index = False , header = True)
personal.to_csv(write_file_name2 , index = False , header = True)
behavioral.to_csv(write_file_name3, index = False , header = True)
print("Finished!")
