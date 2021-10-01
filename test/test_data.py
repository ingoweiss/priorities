import pytest
import pdb
import numpy as np
import pandas as pd

from data import Data

Data._data_dir = 'test/data'

def test_priorities():
    priorities = Data.priorities()

    assert np.array_equal(priorities.columns, ['Epic', 'Date', 'Priority'])

    # Gran Torino
    # May:
    assert priorities.set_index(['Date', 'Epic']).loc['2020-05-01', 'Gran Torino'].at['Priority'] == 3

    # June:
    assert priorities.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Priority'] == 6

def test_changes():

    changes = Data.changes()

    assert np.array_equal(changes.columns, ['Epic', 'Date', 'Previous Date', 'Current Priority', 'Previous Priority', 'Category', 'Change', 'Change Size', 'Changes Top Priorities?', 'Highest Priority Changed', 'Impact Score'])

    # Gran Torino:
    # May:
    assert changes.set_index(['Date', 'Epic']).loc['2020-05-01', 'Gran Torino'].at['Current Priority'] == 3
    assert changes.set_index(['Date', 'Epic']).loc['2020-05-01', 'Gran Torino'].at['Category'] == 'Initial'

    # June:
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Previous Date'] == pd.to_datetime('2020-05-01')
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Current Priority'] == 6
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Previous Priority'] == 3
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Category'] == 'Changed'
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Change'] == 3
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Change Size'] == 3
    assert changes.set_index(['Date', 'Epic']).loc['2020-06-01', 'Gran Torino'].at['Changes Top Priorities?'] == True
