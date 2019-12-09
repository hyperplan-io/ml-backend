# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock
from sklearn.ensemble import RandomForestClassifier
import subprocess
import random
import string
import sqlite3
import numpy as np

from mlbackend.hooks.sqlite_hook import sqlite_hook, read_predictions

N = 15

class SQliteHookTestSuite(unittest.TestCase):
    """SQlite hook test cases."""

    def test_create_table(self):
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        sqlite_hook(filename)
        subprocess.run(["rm", filename])

    def test_do_not_create_table_if_already_exists(self):
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        sqlite_hook(filename)
        sqlite_hook(filename)
        subprocess.run(["rm", filename])

    def test_run_hook_without_metadata(self):
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        hook = sqlite_hook(filename)
        hook([[0,1,2,3,4,5,6,7]], [(0, 0.5), (1, 0.5)], {})

        conn = sqlite3.connect(filename)
        prediction = read_predictions(conn)[0]
        
        assert(
            (prediction[1] == [[0, 1, 2, 3, 4, 5, 6, 7]]).all()
        )
        assert(
            (prediction[2] == [[0. , 0.5], [1. , 0.5]]).all()
        )

        assert(
            (prediction[3] == []).all()
        )
        assert(
            prediction[5] == None
        )

        assert(
            prediction[6] == {}
        )

        subprocess.run(["rm", filename])
    
    def test_run_hook_with_metadata(self):
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        hook = sqlite_hook(filename)
        hook([[0,1,2,3,4,5,6,7]], [(0, 0.5), (1, 0.5)], {'my_entity': 'my_value'})

        conn = sqlite3.connect(filename)
        prediction = read_predictions(conn)[0]

        assert(
            (prediction[1] == [[0, 1, 2, 3, 4, 5, 6, 7]]).all()
        )
        assert(
            (prediction[2] == [[0. , 0.5], [1. , 0.5]]).all()
        )

        assert(
            (prediction[3] == []).all()
        )
        assert(
            prediction[5] == None
        )
        prediction[6] == {'my_entity': 'my_value'}
        subprocess.run(["rm", filename])



if __name__ == '__main__':
    unittest.main()
