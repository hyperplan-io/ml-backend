"""
    This module contains the definition of a machine learning project
"""

from typing import Callable, List
import json
import random
import numpy as np
from feature_type import FeatureType

PREDICTION_FUNCTION = Callable[[np.ndarray], np.ndarray]
PREPROCESSING_FUNCTION = Callable[[np.ndarray, FeatureType], np.ndarray]
POSTPROCESSING_FUNCTION = Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]
SELECTION_FUNCTION = Callable[[List[PREDICTION_FUNCTION]], PREDICTION_FUNCTION]

class Project():
    """
        A project denotes a set of machine learning algorithms.
    """
    def __init__(
            self,
            project_id: str,
            prediction_functions: List[PREDICTION_FUNCTION],
            supported_feature_types: List[FeatureType],
            selection_function: SELECTION_FUNCTION = None,
            preprocessing: PREPROCESSING_FUNCTION = lambda x,f: x,
            postprocessing: POSTPROCESSING_FUNCTION = lambda y: y,
        ):
        self.project_id = project_id
        self.prediction_functions = prediction_functions
        self.supported_feature_types = supported_feature_types

        if selection_function is None:
            selection_function = lambda x: random.choice(prediction_functions)
        self.selection_function = selection_function
        self.preprocessing = preprocessing
        self.postprocessing = postprocessing
        self.pre_hooks = []
        self.post_hooks = []


    def supports_type(self, feature_type):
        return feature_type in self.supported_feature_types

    def predict(self, features, feature_type: FeatureType, metadata: List) -> np.ndarray:
        """
            The prediction function will execute an algorithm on the data that is provided.
            It will execute the hooks that have been registered.

            Keyword arguments:
            features -- An array of data that will be preprocessed by the preprocessing function.
            metadata -- A list of tuples (key and value) to associate to this prediction.
        """
        preprocessed_features = self.preprocessing(features, feature_type)

        if preprocessed_features == None:
            return None

        featuresWithData = zip(features, metadata)
        for hook in self.pre_hooks:
            hook(features, metadata)

        labels = self.postprocessing(
            self.selection_function(self.prediction_functions)(
               preprocessed_features 
            )
        )

        for hook in self.post_hooks:
            hook(features, metadata, labels)

        return labels 

    def register_pre_hook(self, hook: Callable[[np.ndarray], None]):
        """
            Register a hook executed before the computation of the prediction.

            Keyword arguments:
            hook -- The function to execute when a prediction is executed. It takes the raw features as input (not preprocessed).
        """
        self.pre_hooks.append(hook)

    def register_post_hook(self, hook: Callable[[np.ndarray, np.ndarray], None]):
        """
            Register a hook executed after the computation of the prediction.

            Keyword arguments:
            hook: The function to execute when the prediction has been created. It takes the features (not preprocessed) and the labels (not processed) as input.
        """
        self.post_hooks.append(hook)
