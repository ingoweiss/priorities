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

    @classmethod
    def changes(cls):

        top = 5

        # Current priority:
        current_priority = Data.priorities().pivot_table(index='Date', columns='Epic', values='Priority')

        # Previous date:
        dates = np.insert(current_priority.index.values, 0, None)[0:-1]
        width, height = current_priority.shape
        previous_date = pd.DataFrame([dates]*height).transpose().set_index(current_priority.index)
        previous_date.columns = current_priority.columns

        # Previous priority:
        previous_priority = current_priority[:-1]\
            .set_index(current_priority[1:].index)\
            .reindex(index=current_priority.index)

        # Category:
        category = current_priority.copy()
        category.loc[:,:] = None
        category[current_priority == previous_priority] = 'Unchanged'
        category[current_priority != previous_priority] = 'Changed'
        category[previous_priority.isna()] = 'Added'
        category[current_priority.isna()] = 'Removed'
        category[current_priority.isna()] = 'Removed'
        category.loc[category.index.min()] = 'Initial'
        category[current_priority.isna() & previous_priority.isna()] = 'Absent'

        # Change:
        change = current_priority - previous_priority

        # Size of change:
        change_size = change.abs()

        # Does the change change the top priorities?
        changes_top_priorities = current_priority.copy()
        changes_top_priorities.loc[:,:] = False
        changes_top_priorities[category.isin(['Changed', 'Added', 'Removed']) & ((previous_priority <= top) ^ (current_priority <= top))] = True

        # Highest priority changed:
        highest_priority_changed = current_priority.copy()
        highest_priority_changed.loc[:,:] = np.nan
        highest_priority_changed[changes_top_priorities & ((current_priority < previous_priority) | previous_priority.isna())] = current_priority
        highest_priority_changed[changes_top_priorities & ((previous_priority < current_priority) | current_priority.isna())] = previous_priority

        # Impact Score
        impact_score = current_priority.copy()
        impact_score.loc[:,:] = 0
        impact_score[changes_top_priorities] = (top + 1 - highest_priority_changed)*10

        fields_map = {
            'Previous Date': previous_date,
            'Current Priority': current_priority,
            'Previous Priority': previous_priority,
            'Category': category,
            'Change': change,
            'Change Size': change_size,
            'Changes Top Priorities?': changes_top_priorities,
            'Highest Priority Changed': highest_priority_changed,
            'Impact Score': impact_score
        }
        changes = pd.concat(fields_map.values(), keys=fields_map.keys())\
            .unstack()\
            .transpose()\
            .reset_index()

        return changes
