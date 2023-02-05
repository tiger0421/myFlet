import pandas as pd
#import japanize_matplotlib
import matplotlib
import matplotlib.pyplot as plt
from datetime import timedelta

def read_slog(file_dir):
#    return pd.read_csv(file_dir, sep='\t', lineterminator='\r\n')
    return pd.read_csv(file_dir, sep='\t', lineterminator='\n')


def preprocess_slog_date(slog, Date_columns_name):
    slog[Date_columns_name] = pd.to_datetime(
            slog[Date_columns_name],
            format="%Y/%m/%d　%H:%M:%S"
        )
    slog[Date_columns_name] -= slog[Date_columns_name][0]
    return slog


def make_graph(data, element_name_list, Date_columns_name, title=None):
    fig, ax = plt.subplots()
    if(len(data) and len(element_name_list) and len(Date_columns_name)):
        x = data[Date_columns_name]
        for element in element_name_list:
            ax.plot(x, data[element], label = element)
            ax.legend()
        if(title):
            ax.set_title(title)
    return fig, ax


