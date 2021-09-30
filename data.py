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

        for df in data_files:
            match = date_pattern.match(df)
            if match:
                date = pd.to_datetime(match.group(1))
                data = pd.read_csv(df)
                data['Date'] = date
                data['Priority'] = data.index + 1
                frames.append(data)

        return pd.concat(frames)
