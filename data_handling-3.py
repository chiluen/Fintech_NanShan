import os
import numpy as np 
import pandas as pd 

working_dir = "c:/users/user/desktop"
os.chdir(working_dir)

code_list = []

read_file_name = "illness.txt"
data = pd.read_csv(read_file_name)
with open(read_file_name , "r" , encoding = "utf-8") as r_file:
  for line in r_file.readlines():
    line = line.strip()
    code = line[0]
    if code not in code_list:
      code_list.append(code)

  r_file.close()

code_list.pop(0)
code_list.sort()

for code in code_list:
  data[code] = 0

print(data.columns) 

row = data.shape[0]
for i in range(10):
  value = data.iloc[i,0][0]
  index = 1 + code_list.index(value)
  data.iloc[i,index] = 1

data = data.drop(columns = ["illness_code"])
print(data.head(5))

write_file_name = "illness_code.csv"
with open(write_file_name , "w" , encoding = "utf=8") as w_file:
  pass

data.to_csv(write_file_name, index = False , header = True)
print("Finished!")
