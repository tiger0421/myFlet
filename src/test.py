import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import myFunc
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib
import random
import numpy as np
import pprint


DATE_COLUMNS_NAME = "Date"
slog_file_dir = "./"
slog_input_name = "test.slog"
criteria_num = 0
use_mode = False
target_column_name_list = ["hyaku"]

# Read .slog and preprocess
try:
    slog = myFunc.read_slog(slog_file_dir + slog_input_name)
    slog = myFunc.preprocess_slog(slog, DATE_COLUMNS_NAME)

    # Data is listed from the second row of Excel, so the index starts at 2
    slog.index = np.arange(2, len(slog) + 2)
    columns_name = slog.drop(DATE_COLUMNS_NAME, axis=1).columns.values
except Exception as e:
    print(e)

for target_column_name in target_column_name_list:
# Get number of mode
    if(use_mode):
        try:
            mode_num = slog[target_column_name].mode().astype('float').values[0]
        except:
            # if \r exists
            target_column_name += "\r"
            mode_num = slog[target_column_name].mode().astype('float').values[0]
        criteria_num = mode_num

# Confirm whether change exists
    print("#####")
    try:
        temp = slog[target_column_name].astype('float') - criteria_num
        temp = np.ediff1d(temp, to_begin = 0)
        calc_result = slog[temp != 0]
        calc_result = calc_result[calc_result[target_column_name].astype('float') != criteria_num]
        if(len(calc_result)):
            output_file_dir = slog_file_dir + "result_" + target_column_name + ".xlsx"
#            calc_result.to_excel(output_file_dir)
            print("complete " + target_column_name)
        else:
            print("Change is nothing in " + target_column_name)
            print("Not output xlsx")
    except Exception as e:
        print(e)

