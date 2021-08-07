# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 13:53:42 2021

@author: lee
"""

import os
import pandas as pd
from numpy import *

classifier="FastShapelets"
res_stat_pos=os.path.join(os.getcwd(),"{}.csv".format(classifier))

def get_subdir(dir_path):
#    dir_path = "D:\\Java_Code\\tsml-experiments\\results\\FastShapelets\\Predictions\\ACSF1"
    dir_list = os.listdir(dir_path)
    full_path_list=[os.path.join(dir_path,x) for x in dir_list]
    full_path_list = list(filter(lambda x: os.path.isdir(x) and ".xlsx" not in x and ".csv" not in x, full_path_list))
   # full_dir_list = list(filter(lambda x: os.path.isdir(os.path.join(dir_path,x)), dir_list))
#print(full_path_list)
    return full_path_list


def get_csv_files(dir_path):
#    dir_path = "D:\\Java_Code\\tsml-experiments\\results\\FastShapelets\\Predictions\\ACSF1"
    csv_files = os.listdir(dir_path)
    full_path_list=[os.path.join(dir_path,x) for x in csv_files]
    full_path_list = list(filter(lambda x: "csv" in x,  full_path_list))
    
    full_path_list=[]
    for csv_file in csv_files:
        full_path_list.append(os.path.join(dir_path, csv_file))
#print(full_path_list)
    return full_path_list

def get_csv_result(file_path):
 #   file_path ="D:\\Java_Code\\tsml-experiments\\results\\FastShapelets\\Predictions\\ACSF1\\testFold0.csv"
    with open(file_path) as f:
        content = f.readlines()
        res = content[2].split(',')[0]
# print(res)
#     print(content)
    return float(res)

if __name__=="__main__":
    dir_path = os.path.join(os.getcwd(),classifier,"Predictions") 
    dataset_result_list = get_subdir(dir_path)
    df = pd.DataFrame()
    for dataset_result in dataset_result_list:
        dataset_name=dataset_result.split("\\")[-1]
        csv_file_list = get_csv_files(dataset_result)
       # print(dataset_name, csv_file_list)
        res = [get_csv_result(x) for x in csv_file_list]
        single_dataset_stat_dict = {"dataset":[dataset_name]}
        for i,fold in enumerate(csv_file_list):
         #   print(fold)
            single_dataset_stat_dict[fold.split('.')[0].split('\\')[-1]] = [res[i]]
        if len(res)>0:
            single_dataset_stat_dict["average_acc"]=mean(res)
        df = pd.concat([df, pd.DataFrame.from_dict(single_dataset_stat_dict)],axis=0, ignore_index=True)
    df.to_csv(res_stat_pos)
    
    ########
    dft = pd.read_excel("UCRTemplate.xlsx")
    dft.dropna(how="all")
    df_joint = dft.set_index('Dataset').join(df.set_index('dataset'))
    df_joint.to_csv(res_stat_pos.replace(".csv","_integ.csv"))