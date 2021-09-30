import pandas as pd
import numpy as np
import glob
import re

class Data:

    _data_dir = 'data'

    @classmethod
    def priorities(cls):
        
        data_files = glob.glob(cls._data_dir + '/priorities-*.csv')
        date_pattern = re.compile(cls._data_dir + '/priorities-(\d{4}-\d{2}-\d{2})\.csv')
        frames = []

        for df_name in data_files:
            match = date_pattern.match(df_name)
            if match:
                date = pd.to_datetime(match.group(1))
                with open(df_name) as df:
                    epics_list = df.read().split("\n")
                epics = pd.DataFrame({'Epic': epics_list})\
                    .replace('', np.nan)\
                    .dropna()
                epics['Date'] = date
                epics['Priority'] = epics.index + 1
                frames.append(epics)

        return pd.concat(frames)
