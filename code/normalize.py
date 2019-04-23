# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 22:16:16 2019

@author: vaibhav gaikwad
"""

def normalize_data(data):
    new_file_data = data.loc[:,]
    # class normalization - 0/1 based no. of bugs (if bugs == 0 then 0, else 1)
    for row_index in range(0, len(data)):
       if (new_file_data["Class"][row_index] != 0):
           new_file_data.loc[row_index:row_index, "Class"] = 1
    #class_values = new_file_data.loc[:, "Class"].tolist()
    
    # data normalization - 0/1 based no. median (if data < median then 0, else 1)
    for col_index in range(1, 21):       
        col_name = "A%d" % (col_index)
        col_median = data.loc[:, col_name].median()
        #print("%s [median:%f], " % (col_name, col_median), end=" ")       
       # print("%s [median:%f], " % (col_name, col_median))
        for row_index in range(0, len(data)):
            if (data[col_name][row_index] < col_median):
                new_file_data.loc[row_index:row_index, col_name] = 0                
            else:
                new_file_data.loc[row_index:row_index, col_name] = 1
    return new_file_data