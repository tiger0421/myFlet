import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import myFunc
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib
import random
import numpy as np
import yaml


DATE_COLUMNS_NAME = "Date"
JSON_FILE_DIR  = "./"
JSON_FILE_NAME = "continuousGenGraphConfig.json"
slog_file_dir = "./"
slog_file_name = "test.slog"

# Read json
try:
    with open(JSON_FILE_DIR + JSON_FILE_NAME) as file:
        config = yaml.safe_load(file.read())
except Exception as e:
    print(e)


# Read slog
try:
    slog = myFunc.read_slog(slog_file_dir + slog_file_name)
    slog = myFunc.preprocess_slog(slog, DATE_COLUMNS_NAME)
except Exception as e:
    print(e)

# Drow graph
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.get_cmap("tab10").colors)
color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
for config_key, config_value in config.items():
    ax1_columns = config_value[0]["ax1"]
    try:
        ax2_columns = config_value[0]["ax2"]
    except:
        ax2_columns = []

    try:
        ax1.clear()
        ax2.clear()
        ax1.plot(slog[DATE_COLUMNS_NAME], slog[ax1_columns].astype(np.float64), label = ax1_columns)
        ax1.xaxis.set_tick_params(rotation=45, labelsize=5)
        step = (60 // 30) * 30
        ax1.set_xticks(slog[DATE_COLUMNS_NAME][::step])
        if(ax2_columns):
            for i, column in enumerate(ax2_columns):
                ax2.plot(slog[DATE_COLUMNS_NAME], slog[column].astype(np.float64),
                         label = column, color = color_cycle[len(ax1_columns) + i])
            ax2.set_xticks(slog[DATE_COLUMNS_NAME][::step])
            ax2.xaxis.set_tick_params(rotation=45, labelsize=5)
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(.5, -.15), ncol=4)
        plt.tight_layout()
        fig.savefig(JSON_FILE_DIR + "result_" + config_key + ".png")
    except Exception as e:
        print(e)


