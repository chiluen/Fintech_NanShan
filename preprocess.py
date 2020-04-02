import h5py
import xlrd
import numpy as np

def fileload(filename):  #load for one sheet
    dataset = []
    
    print('Loading for data...')
    workbook = xlrd.open_workbook(filename)
    table = workbook.sheets()[0]
    
    print('Start to preprocess ' + workbook.sheet_names()[0])
    for row in range(table.nrows):
        dataset.append(table.row_values(row))
    print('Finish')
    return np.array(dataset)

def fileload_merge(filename_1, filename_2):
    dataset = []
    
    print('Loading for data...')
    workbook_1 = xlrd.open_workbook(filename_1)
    workbook_2 = xlrd.open_workbook(filename_2)
    table_1 = workbook_1.sheets()[0]
    table_2 = workbook_2.sheets()[0]
    
    print('Start to preprocess ' + workbook_1.sheet_names()[0])
    for row in range(table_1.nrows):
        dataset.append(table_1.row_values(row))
    print('Start to preprocess ' + workbook_2.sheet_names()[0])
    for row in range(1,table_2.nrows): #exclude title
        dataset.append(table_2.row_values(row))
    print('Finish')
    return np.array(dataset)

def main():
    filename = ['./data/CLAIM_ACCT_FIN_1.xlsx', './data/CLAIM_ACCT_FIN_2.xlsx', './data/COV_ACCT_FIN.xlsx', './data/CUST_PROPERTY_FIN_1.xlsx', './data/CUST_PROPERTY_FIN_2.xlsx', './data/CUST_RELATION_FIN.xlsx']
    h5_filename = ['CLAIM_ACCT_FIN', 'COV_ACCT_FIN', 'CUST_PROPERTY_FIN', 'CUST_RELATION_FIN']
    dataset = []
    
    #process data
    dataset.append(fileload_merge(filename[0], filename[1])) 
    dataset.append(fileload(filename[2]))
    dataset.append(fileload_merge(filename[3],filename[4]))
    dataset.append(fileload(filename[5]))
    
    #load to h5py
    dtype = h5py.special_dtype(vlen=str)
    with h5py.File('fintech.h5','w') as f:
        for i in range(len(dataset)):
            d = f.create_dataset(h5_filename[i], dataset[i].shape, dtype = dtype)
            d[:] = dataset[i]

if __name__ == '__main__':
    main()