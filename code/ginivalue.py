# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 00:09:43 2019

@author: vaibhav gaikwad
"""
import math 
import pandas as pd
import time
import gc
import normalize as norm
import csv_reader as csv

###########################################################################################################
def find(lst, element, equals):
    result = []
    length = len(lst)
    for i in range(0, length):
        if(equals == True):
            if(lst[i] == element):
                result.append(i)
                #print(result)
        if(equals == False):
            if(lst[i] != element):
                result.append(i)     
    return result
##########################################################################################################
def get(lst, indicies):
    result = []
    for i in range(0, len(indicies)):
        result.append(lst[indicies[i]])
    return result
##########################################################################################################
def ginivalue(fault):
    if(len(fault) == 0):
        return 0
    indexes_good_code = find(fault,  0, True)
    count_good_code = len(indexes_good_code)
    count_bad_code = len(fault) - count_good_code
    probability_good_code = count_good_code / len(fault)   
    probability_bad_code = count_bad_code / len(fault)
    gini = 1 - math.pow(probability_good_code, 2) - math.pow(probability_bad_code, 2) 
    return gini
##########################################################################################################
def entropy(fault):
    if(len(fault) == 0):
        return 0
    indexes_good_code = find(fault,  0, True)
    count_good_code = len(indexes_good_code)
    count_bad_code = len(fault) - count_good_code
    probability_good_code = count_good_code / len(fault)   
    probability_bad_code = count_bad_code / len(fault)
    print([probability_good_code, probability_bad_code])
    entropy_value = -probability_good_code * (math.log2(probability_good_code if probability_good_code > 0 else 1)) -probability_bad_code * (math.log2(probability_bad_code if probability_bad_code > 0 else 1)) 
    return entropy_value
##########################################################################################################
def ginisplit(data, fault, method):
    index_good_code = find(data,  0, True)
    index_bad_code = find(data, 0, False)
    index_in_class_for_good_code = get(fault, index_good_code)
    index_in_class_for_bad_code = get(fault, index_bad_code)
    
    gini_good_code = 0
    gini_bad_code = 0
    if(method == "gini"):
        gini_good_code = ginivalue(index_in_class_for_good_code)
        gini_bad_code = ginivalue(index_in_class_for_bad_code)
    else:
        gini_good_code = entropy(index_in_class_for_good_code)
        gini_bad_code = entropy(index_in_class_for_bad_code)    
    
    gini_split = ((len(index_good_code) / len(data))* gini_good_code) + ((len(index_bad_code) / len(data))* gini_bad_code)
    return gini_split
##########################################################################################################
def info_gain(data, fault, method):
    gain = 0
    entropy_parent = entropy(fault)
    gini_split_value = ginisplit(data, fault, method)
    gain = entropy_parent - gini_split_value
    return gain
##########################################################################################################
def create_info_gain_writer():
    file = "%s%s_infogain.xlsx" % (csv.WRITE_FOLDER, csv.BITS_ID)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    return writer

def close_info_gain_writer(writer):
    writer.save();
    return

##########################################################################################################

info_gain_writer = create_info_gain_writer()

for file_index in range(1, 57):   
    print("---------- processing file '%s.csv' ----------------" % (file_index))
    start_time = time.time()
    info_gain_values = []
    normalized_data = norm.normalize_data(csv.read_csv_data(file_index))
    for col_index in range(1, 21):
        col_name =  "A%d" % (col_index)
        data = normalized_data.loc[:, col_name].tolist()
        #print(data)
        clas = normalized_data.loc[:, "Class"].tolist()
        #gini_value = ginisplit(data, clas) 
        #entropy_value = entropy(data, clas)
        ig = info_gain(data, clas, "entropy")
        info_gain_values.append(ig)
        #print("%s[%f]" % (col_name, ig))
    
    elapsed_time = time.time() - start_time
    info_gain_dataframe = pd.DataFrame({"Information Gain": info_gain_values});
    
    info_gain_dataframe.to_excel(info_gain_writer, sheet_name="%s.csv" % (file_index), index = False)
    
    del [normalized_data,info_gain_dataframe]
    gc.collect()
    new_file_data = pd.DataFrame()
    #print("max_gain:%f, for column:%s" % (max_gain, max_gain_col))
    print("---------- finished in '%f' time ----------" % (elapsed_time))
    
close_info_gain_writer(info_gain_writer)