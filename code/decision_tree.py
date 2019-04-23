# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:08:57 2019

@author: vaibhav gaikwad
"""

# Importing the required packages 
import normalize as norm
import csv_reader as csv
import pandas as pd
import datetime
import gc
# pip install -t . numpy scipy scikit-learn
#pip install -t . scikit-learn metrics 
from sklearn.metrics import confusion_matrix 
#from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split
   
# Function to perform training with entropy. 
def train_using_entropy(dataframe):
    dataframe = dataframe.dropna() # drop rows with missing values
    data = dataframe[["A1", "A2", "A3", "A4" , "A5", "A6", "A7" , "A8", "A9", "A10", "A11", "A12", "A13", "A14" , "A15" , "A16", "A17", "A18", "A19" , "A20" ]]
    clas = dataframe[["Class"]]
    data_train, data_test, clas_train, clas_test = train_test_split(data, clas, test_size=0.3)
    # Decision tree with entropy 
    model = DecisionTreeClassifier(criterion = "entropy", random_state = 0, max_depth = None, min_samples_leaf = 1,splitter='best')  
    # Performing training 
    model.fit(data_train, clas_train) 
    return [model,  data_test, clas_test]
  
def create_performance_writer():
    file = "%s%s_performance.xlsx" % (csv.WRITE_FOLDER, csv.BITS_ID)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    return writer

def close_performance_writer(writer):
    writer.save();
    return

performance_writer = create_performance_writer()
results_dataframe = pd.DataFrame(columns=["Accuracy","F-Measure"]);

for file_index in range(1, 57):   
    print("---------- processing file '%s.csv' ----------------" % (file_index))
    start_time = datetime.datetime.utcnow()
    normalize_data = norm.normalize_data(csv.read_csv_data(file_index))
    answers = train_using_entropy(normalize_data)
    model = answers[0]
    data_test = answers[1]
    clas_test = answers[2] 
    
    # Prediction using entropy 
    clas_predicted = model.predict(data_test)
    
    tn, fp, fn, tp = confusion_matrix(clas_test, clas_predicted).ravel()
    print([tn, tp, fp, fn])
    accuracy = (tp + tn) / (tn + fp + fn + tp)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2*recall*precision / (recall + precision)
    #f_score = (2*tp) / ((2*tp)+fp+fn)  
    print("accuracy:%f, f-score:%f" % (accuracy, f_score))
    results_dataframe = results_dataframe.append({"Accuracy" : accuracy, "F-Measure": f_score}, ignore_index = True)
    del [normalize_data]
    gc.collect()
    elapsed_time = datetime.datetime.utcnow() - start_time
    print("---------- finished in '%f' time ----------" % (elapsed_time.total_seconds()))
    
results_dataframe.to_excel(performance_writer, index = False)
close_performance_writer(performance_writer)