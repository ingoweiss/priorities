import pytest
import pdb
import numpy as np

from data import Data

Data._data_dir = 'test/data'

def test_priorities():
    priorities = Data.priorities()

    assert np.array_equal(priorities.columns, ['Epic', 'Date', 'Priority'])
    assert priorities.set_index(['Date', 'Epic']).loc['2020-05-01', 'Gran Torino'].at['Priority'] == 3
