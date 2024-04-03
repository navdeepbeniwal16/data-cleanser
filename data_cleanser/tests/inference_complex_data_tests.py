import unittest
import pandas as pd
from data_cleanser.inference import infer_data_type

class TestInferDataType(unittest.TestCase):

    def test_standard_form(self):
        # Test standard form: a + bj
        df = pd.DataFrame({'col': ['1+2j', '3+4j', '5+6j']})
        self.assertEqual(infer_data_type(df, 'col'), 'complex')

    def test_parentheses_form(self):
        # Test parentheses form: (a + bj) or (a, b)
        df = pd.DataFrame({'col': ['(1+2j)', '(3+4j)', '(5+6j)']})
        self.assertEqual(infer_data_type(df, 'col'), 'complex')

    def test_exponential_form(self):
        # Test exponential form: a + b*j or a + bj
        df = pd.DataFrame({'col': ['1+2*j', '3+4*j', '5+6*j']})
        self.assertEqual(infer_data_type(df, 'col'), 'complex')

    def test_polar_form(self):
        # Test polar form: r * (cos(theta) + j*sin(theta))
        df = pd.DataFrame({'col': ['1*(cos(0)+j*sin(0))', '2*(cos(1)+j*sin(1))', '3*(cos(2)+j*sin(2))']})
        self.assertEqual(infer_data_type(df, 'col'), 'complex')

    def test_tuple_form(self):
        # Test tuple form: (a, b)
        df = pd.DataFrame({'col': ['(1, 2)', '(3, 4)', '(5, 6)']})
        self.assertEqual(infer_data_type(df, 'col'), 'complex')

    def test_mixed_formats(self):
        # Test mixed formats
        df = pd.DataFrame({'col': ['1+2j', '(3, 4)', '5+6*j']})
        self.assertEqual(infer_data_type(df, 'col'), 'complex')

    def test_invalid_formats(self):
        # Test invalid formats
        df = pd.DataFrame({'col': ['1+2', '3+j', '5*6j']})
        self.assertNotEqual(infer_data_type(df, 'col'), 'complex')

if __name__ == '__main__':
    unittest.main()