#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Main function
"""

import numpy as np

from project import Project
from hooks.sqlite_hook import sqlite_hook
from mlrestapp import MlRestApp

if __name__ == "__main__":
    print('hello world')
    PROJECT_A = Project(
        "id",
        prediction_functions=[
            lambda x: np.array([[2]])
        ],
    )

    PROJECT_A.register_post_hook(sqlite_hook('example.db'))
    print(
        PROJECT_A.predict([[1]], [('my_entity', 'my_value')])
    )

    MlRestApp([PROJECT_A]).start()
