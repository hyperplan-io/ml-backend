#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Main function
"""

from project import Project
from mlrestapp import MlRestApp

from .hooks.sqlite_hook import sqlite_hook

def preprocess(features, feature_type):
    """
        preprocess data before inference.
        Return None if you do not accept the feature type

        Keyword arguments:
        features -- the features data
        feature_type -- the type of feature (application/json, image/jpeg ...)
    """
    if feature_type == 'application/json':
        return map(features, lambda x: x*2)
    return None

if __name__ == "__main__":
    PROJECT_A = Project(
        "id",
        prediction_functions=[
            lambda features: [[x*2 for x in X] for X in features]
        ]
    )

    PROJECT_A.register_post_hook(sqlite_hook('example.db'))
    print(
        'Test prediction: {}'.format(
            PROJECT_A.predict([[1]], 'numpy', {'userId': '42'})
        )
    )

    MlRestApp(
        [
            (PROJECT_A, '/projecta', ['application/json'])
        ]
    ).start()
