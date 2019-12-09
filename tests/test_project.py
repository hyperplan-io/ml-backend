# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock
from sklearn.ensemble import RandomForestClassifier

from mlbackend.project import Project

def clf1(features):
    return [(10, 0.1), (20, 0.2)]

def clf2(features):
    return [(10, 0.2), (20, 0.5)]

class ProjectTestSuite(unittest.TestCase):
    """Project test cases."""

    def test_register_pre_hook(self):
        project = Project(
            'id',
            [clf1],
            None
        )
        mock = Mock()
        project.register_pre_hook(mock)

        project.predict([[1,2,3]], 'numpy', {})

        mock.assert_called_once_with([[1,2,3]], {})

    def test_register_post_hook(self):
        project = Project(
            'id',
            [clf1],
            None
        )
        mock = Mock()
        project.register_post_hook(mock)

        project.predict([[1,2,3]], 'numpy', {})

        mock.assert_called_once_with([[1,2,3]], [(10, 0.1), (20, 0.2)], {})

    def test_predict(self):
        pass

    def test_predict_scikit_learn(self):
        # taken from the scikit learn documentation
        clf = RandomForestClassifier(random_state=0)
        X = [[ 1,  2,  3], [11, 12, 13]]
        y = [0, 1]
        clf.fit(X, y)

        project = Project(
            'id',
            [clf.predict],
            None
        )

        n = 100
        for i in range(0, n):
            project.predict([[1,2,3]], 'numpy', {})

    def test_constructor_without_selection_func(self):
        project = Project(
            'id',
            [clf1, clf2],
            None
        )


        # execute the selection method n times and see how many different values we get
        n = 100
        functions_clf1 = 0
        functions_clf2 = 0

        for i in range(0, n):
            function = project.selection_function(project.prediction_functions, [[0, 1, 2, 3]])
            if function == clf1:
                functions_clf1+=1
            elif function == clf2:
                functions_clf2+=1

        assert(
            functions_clf1 > 0
        )
        assert(
            functions_clf2 > 0
        )

    def test_constructor_with_selection_func(self):
        project = Project(
            'id',
            [clf1, clf2],
            lambda functions, features: functions[0]
        )

        # execute the selection method n times and see how many different values we get
        n = 100
        functions_clf1 = 0
        functions_clf2 = 0

        for i in range(0, n):
            function = project.selection_function(project.prediction_functions, [[0, 1, 2, 3]])
            if function == clf1:
                functions_clf1+=1
            elif function == clf2:
                functions_clf2+=1

        assert(
            functions_clf1 > 0
        )
        assert(
            functions_clf2 == 0
        )

if __name__ == '__main__':
    unittest.main()
