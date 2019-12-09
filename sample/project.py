"""
    This module contains the definition of a machine learning project
"""

from typing import Callable, List, Dict
import random
import numpy as np

PredictionFunction = Callable[[np.ndarray], np.ndarray]
PreProcessingFunction = Callable[[np.ndarray, str], np.ndarray]
PostProcessingFunction = Callable[[np.ndarray], np.ndarray]
SelectionFunction = Callable[[List[PredictionFunction], np.ndarray], PredictionFunction]

class Project():
    """
        A project denotes a set of machine learning algorithms.
    """
    def __init__(
            self,
            project_id: str,
            prediction_functions: List[PredictionFunction],
            selection_function: SelectionFunction = None,
            preprocessing: PreProcessingFunction = lambda x, f: x,
            postprocessing: PostProcessingFunction = lambda y: y,
        ):
        self.project_id = project_id
        self.prediction_functions = prediction_functions

        if selection_function is None:
            selection_function = lambda x, f: random.choice(prediction_functions)
        self.selection_function = selection_function
        self.preprocessing = preprocessing
        self.postprocessing = postprocessing
        self.pre_hooks = []
        self.post_hooks = []

    def predict(self, features, feature_type: str, metadata: Dict) -> np.ndarray:
        """
            The prediction function will execute an algorithm on the data that is provided.
            It will execute the hooks that have been registered.

            Keyword arguments:
            features -- An array of data that will be preprocessed by the preprocessing function.
            metadata -- A list of tuples (key and value) to associate to this prediction.
        """
        preprocessed_features = self.preprocessing(features, feature_type)

        if preprocessed_features is None:
            return None

        for hook in self.pre_hooks:
            hook(features, metadata)

        labels = self.postprocessing(
            self.selection_function(self.prediction_functions, features)(
                preprocessed_features
            )
        )
        print(labels)
        for hook in self.post_hooks:
            hook(features, labels, metadata)

        return labels

    def register_pre_hook(self, hook: Callable[[np.ndarray, Dict], None]):
        """
            Register a hook executed before the computation of the prediction.

            Keyword arguments:
            hook --
            The function to execute when a prediction is executed.
            It takes the raw features as input (not preprocessed).
        """
        self.pre_hooks.append(hook)

    def register_post_hook(self, hook: Callable[[np.ndarray, np.ndarray, Dict], None]):
        """
            Register a hook executed after the computation of the prediction.

            Keyword arguments:
            hook --
            The function to execute when the prediction has been created.
            It takes the features (not preprocessed) and the labels (not processed) as input.
        """
        self.post_hooks.append(hook)
