#!/usr/bin/env python3
# coding: utf-8


import h5py
import numpy as np
from collections import defaultdict
from tqdm import tqdm

path = "data/fintech.h5"
f = h5py.File(path, "r")
CLAIM_ACCT = f['CLAIM_ACCT_FIN']
COV_ACCT = f['COV_ACCT_FIN']


# 把Policy_holder, Policy_RK, 時間最久的date抓出來
#CLAIM ：(Policy_holder, Policy_RK, time)

dic_CLAIM = defaultdict(list)
for i in range(1, CLAIM_ACCT.shape[0]):
    now_policy = CLAIM_ACCT[i][2]
    now_holder = CLAIM_ACCT[i][10]
    now_date = CLAIM_ACCT[i][7]
    if dic_CLAIM[now_holder, now_policy] == []:
        dic_CLAIM[now_holder, now_policy] = [float(now_date)]
    else:
        dic_CLAIM[now_holder, now_policy].append(float(now_date))
        dic_CLAIM[now_holder, now_policy] = [min(dic_CLAIM[now_holder, now_policy])]

#COV ：(Policy_holder, Policy_RK, time)
dic_COV = defaultdict(list)

for i in range(1, COV_ACCT.shape[0]):
    now_policy = COV_ACCT[i][1]
    now_holder = COV_ACCT[i][7]
    now_date = COV_ACCT[i][4] #EFFECTIVE_DT
    if dic_COV[now_holder, now_policy] == []:
        dic_COV[now_holder, now_policy] = [float(now_date)]
    else:
        dic_COV[now_holder, now_policy].append(float(now_date))
        dic_COV[now_holder, now_policy] = [min(dic_COV[now_holder, now_policy])]


# 把兩邊的Policy_RK 依據時間串起來

compare_list_CLAIM = []
compare_list_COV = []
used_holder = ""
COV_keys_list = list(dic_COV.keys())
CLAIM_keys_list = list(dic_CLAIM.keys())
relation = [] #(Policy_holder_RK, POLICY_CLAIM_RK, POLICY_COV_RK)
pbar = tqdm(total=len(COV_keys_list[:-2]))
for counter, data in enumerate(COV_keys_list[:-2]):
        
    pbar.update(1)
    
    #讓同一個holder可以被濾掉
    if data[0] == used_holder:
        continue
   
    used_holder = data[0] #目前正處理的policy_holder
    for i in range(len(COV_keys_list)-2): #把同一個policy holder的所有資訊裝起來
        if COV_keys_list[i][0] == used_holder:
            temp = list(COV_keys_list[i])
            temp.append(dic_COV[COV_keys_list[i]][0])
            compare_list_COV.append( temp )
    
    for i in range(len(CLAIM_keys_list)-2):
        if CLAIM_keys_list[i][0] == used_holder:
            temp = list(CLAIM_keys_list[i])
            temp.append(dic_CLAIM[CLAIM_keys_list[i]][0])
            compare_list_CLAIM.append(temp)
            
    for d_COV in compare_list_COV: #去做對比
        for d_CLAIM in compare_list_CLAIM:
            if d_COV[2] > d_CLAIM[2]:
                relation.append([d_COV[0], d_CLAIM[1], d_COV[1]])
                
    compare_list_CLAIM = [] 
    compare_list_COV = []

relation.insert(0,['Policy_holder_RK', 'POLICY_CLAIM_RK', 'POLICY_COV_RK'])
relation = np.array(relation)
dtype = h5py.special_dtype(vlen=str)
with h5py.File('relation.h5','w') as f:
    d = f.create_dataset('repurchase', relation.shape, dtype = dtype)
    d[:] = relation

