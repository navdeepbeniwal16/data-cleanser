import unittest
import pandas as pd
import numpy as np

from data_cleanser.inference import infer_data_type, infer_data_types

class TestInference(unittest.TestCase):
    def test_int64_inference(self):
        # Integers that fit within int64 but not int32
        df = pd.DataFrame({'col': [2**31, -2**31 - 1]})
        self.assertEqual(infer_data_type(df, 'col'), 'int64')

    def test_int32_inference(self):
        # Integers that fit within int32 but not int16
        df = pd.DataFrame({'col': [2**31 - 1, -2**31]})
        self.assertEqual(infer_data_type(df, 'col'), 'int32')

    def test_int16_inference(self):
        # Integers that fit within int16 but not int8
        df = pd.DataFrame({'col': [2**15 - 1, -2**15]})
        self.assertEqual(infer_data_type(df, 'col'), 'int16')

    def test_int8_inference(self):
        # Integers that fit within int8
        df = pd.DataFrame({'col': [2**7 - 1, -2**7]})
        self.assertEqual(infer_data_type(df, 'col'), 'int8')

    def test_int64_inference_with_nan(self):
        # Integers that fit within int64 but not int32, with NaN values included
        df = pd.DataFrame({'col': [2**31, -2**31 - 1, 3, None, 'not a number']})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_float64_inference(self):
        # Float values that require float64 precision
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308]})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_float32_inference(self):
        # Float values that fit within float32
        df = pd.DataFrame({'col': [3.402823e+30, -3.402823e+30]})
        self.assertEqual(infer_data_type(df, 'col'), 'float32')

if __name__ == '__main__':
    unittest.main(verbosity=2)