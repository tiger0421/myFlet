import pandas as pd
from datetime import timedelta

def read_slog(file_dir):
#    return pd.read_csv(file_dir, sep='\t', lineterminator='\r\n')
    return pd.read_csv(file_dir, sep='\t', lineterminator='\n')


def preprocess_slog_date(slog, DATE_COLUMNS_NAME):
    # Date
    slog[DATE_COLUMNS_NAME] = pd.to_datetime(
            slog[DATE_COLUMNS_NAME],
            format="%Y/%m/%d　%H:%M:%S"
        )
    slog[DATE_COLUMNS_NAME] -= slog[DATE_COLUMNS_NAME][0]
    slog[DATE_COLUMNS_NAME] = my_hhmmss(slog[DATE_COLUMNS_NAME].dt)

    # String Data
    slog = slog.replace("OFF", 0)
    slog = slog.replace("ON", 1)

    # % -> numeric
    slog = slog.apply(pd.to_numeric, errors='ignore').astype("str")
    slog = slog.apply(lambda x: x.str.rstrip('%').astype('float') / 100
              if x.dtype == 'object' and x.str.endswith('%').any()
              else x)


    return slog


def my_hhmmss(td):
    ss = td.total_seconds().astype(int)
    mm, ss = ss.divmod(60, fill_value = 0)
    hh, mm = mm.divmod(60, fill_value = 0)

    # Change format from float to str
    hh = hh.map('{:03.0f}'.format).astype(str)
    mm = mm.map('{:02.0f}'.format).astype(str)
    ss = ss.map('{:02.0f}'.format).astype(str)


    # Concatenate
    r = hh + ":" + mm + ":" + ss
    return r

