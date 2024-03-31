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

    # TODO: the method call needs to return an 'int64' given all of the values except NaN are integers - DD
    def test_int64_inference_with_nan(self):
        # Integers that fit within int64 but not int32, with NaN values included
        df = pd.DataFrame({'col': [2**31, -2**31 - 1, 3, None]})
        self.assertEqual(infer_data_type(df, 'col'), 'int64')

    def test_float64_inference(self):
        # Float values that require float64 precision
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308]})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_float32_inference(self):
        # Float values that fit within float32
        df = pd.DataFrame({'col': [3.402823e+30, -3.402823e+30]})
        self.assertEqual(infer_data_type(df, 'col'), 'float32')

    def test_float64_with_nan(self):
        # Float values that require float64 precision
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308, 12.5, None, 'not a number']})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_mixed_numeric_inference(self):
        # Integers, Floats and NaN all mixed in the data
        mixed_data = [100, 200.5, np.nan, -500, 350.0, 400, 1.5e2, -2.5e2, 0, 'not a number', None, 230]
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df, 'col'), 'float32')

    def test_numeric_string_inference(self):
        # Numeric values stored as strings
        numbers_as_string = ['1.7976931348623157e+308', '-1.7976931348623157e+308']
        df = pd.DataFrame({'col': numbers_as_string})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_numeric_commas_inference(self):
        # Numeric values with commas as thousands separators
        mixed_data = ['1,000', '2,500', '10,000', '100,000', '1,000,000']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df, 'col'), 'int64')

    def test_numeric_commas_mixed_with_floats_inference(self):
        # Mixed data with numbers containing commas and floats
        mixed_data = ['1,000', '2,500', '10,000', '100,000', '1,000,000', '3.14', '6,543.21']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_numeric_commas_mixed_with_non_numeric_inference(self):
        # Mixed data with numbers containing commas, floats, and non-numeric values
        mixed_data = ['1,000', '2,500', '10,000', '100,000', '1,000,000', '3.14', '6,543.21', 'not a number']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')

    def test_numeric_commas_with_decimal_places_inference(self):
        # Numeric values with commas as thousands separators and decimal places
        mixed_data = ['1,000.50', '2,500.75', '10,000.25', '100,000.60', '1,000,000.99']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df, 'col'), 'float64')


if __name__ == '__main__':
    unittest.main(verbosity=2)