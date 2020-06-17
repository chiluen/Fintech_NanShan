import os 
import pandas as pd 
import numpy as np 

working_dir = "c:/users/user/desktop"
os.chdir(working_dir)

data1 = pd.read_csv("personal_and_behavioral.csv")
data2 = pd.read_csv("personal.csv")
data3 = pd.read_csv("behavioral.csv")

write_file_name = "repurchase_data.xlsx"
with pd.ExcelWriter(write_file_name) as writer:
  data1.to_excel(writer , sheet_name = "personal_and_behavioral")
  data2.to_excel(writer , sheet_name = "personal")
  data3.to_excel(writer , sheet_name = "behavioral")
  writer.save()
print("Finished!")