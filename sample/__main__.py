#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Main function
"""

import numpy as np

from project import Project
from hooks.sqlite_hook import sqlite_hook
from mlrestapp import MlRestApp
from feature_type import FeatureType


def preprocess(features, feature_type):
    if feature_type == FeatureType.JSON:
        pass
    elif feature_type == FeatureType.JPEG:
        return None
    print('feature type is {}'.format(feature_type))
    return features

if __name__ == "__main__":
    PROJECT_A = Project(
        "id",
        prediction_functions=[
            lambda x: np.array([[2]])
        ],
        supported_feature_types=[FeatureType.JSON],
        preprocessing=preprocess
    )

    PROJECT_A.register_post_hook(sqlite_hook('example.db'))
    print(
        'Test prediction: {}'.format(
            PROJECT_A.predict([[1]], FeatureType.NUMPY_ARRAY, [('my_entity', 'my_value')])
        )
    )

    MlRestApp([PROJECT_A]).start()
