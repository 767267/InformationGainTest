# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 23:06:14 2019

@author: vaibhav gaikwad
"""

import pandas as pd

BASE_PATH = "F:\\BITS Pilani\\SEM 2\\2. DataMining - ISZC415"
READ_FOLDER = ("%s\\data\\" % BASE_PATH)
WRITE_FOLDER = ("%s\\results\\" % BASE_PATH)
BITS_ID = "2018HT12597"


def read_csv_data(file_index):
    file_name = '%s%d.csv' % (READ_FOLDER, file_index)
    file_data = pd.read_csv(file_name, sep=',',header=None, names = ["A1", "A2", "A3", "A4" , "A5", "A6", "A7" , "A8", "A9", "A10", "A11", "A12", "A13", "A14" , "A15" , "A16", "A17", "A18", "A19" , "A20" , "Class"])
    return file_data;