import unittest
import pandas as pd
import numpy as np
import datetime

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
        
    def test_date_format_YMD(self):
        # Test format "%Y-%m-%d"
        df = pd.DataFrame({'col': ['2022-03-28']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_date_format_MDY(self):
        # Test format "%m/%d/%Y"
        df = pd.DataFrame({'col': ['03/28/2022']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_date_format_DMY(self):
        # Test format "%d/%m/%Y"
        df = pd.DataFrame({'col': ['28/03/2022']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMD_HMS(self):
        # Test format "%Y-%m-%d %H:%M:%S"
        df = pd.DataFrame({'col': ['2022-03-28 13:45:30']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDY_HMS(self):
        # Test format "%m/%d/%Y %H:%M:%S"
        df = pd.DataFrame({'col': ['03/28/2022 13:45:30']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMY_HMS(self):
        # Test format "%d/%m/%Y %H:%M:%S"
        df = pd.DataFrame({'col': ['28/03/2022 13:45:30']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMD_HMS_f(self):
        # Test format "%Y-%m-%d %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['2022-03-28 13:45:30.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDY_HMS_f(self):
        # Test format "%m/%d/%Y %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['03/28/2022 13:45:30.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMY_HMS_f(self):
        # Test format "%d/%m/%Y %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['28/03/2022 13:45:30.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMD_HM(self):
        # Test format "%Y-%m-%d %H:%M"
        df = pd.DataFrame({'col': ['2022-03-28 13:45']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDY_HM(self):
        # Test format "%m/%d/%Y %H:%M"
        df = pd.DataFrame({'col': ['03/28/2022 13:45']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMY_HM(self):
        # Test format "%d/%m/%Y %H:%M"
        df = pd.DataFrame({'col': ['28/03/2022 13:45']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMDTHMS(self):
        # Test format "%Y-%m-%dT%H:%M:%S"
        df = pd.DataFrame({'col': ['2022-03-28T13:45:00']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDYTHMS(self):
        # Test format "%m/%d/%YT%H:%M:%S"
        df = pd.DataFrame({'col': ['03/28/2022T13:45:00']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMYTHMS(self):
        # Test format "%d/%m/%YT%H:%M:%S"
        df = pd.DataFrame({'col': ['28/03/2022T13:45:00']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMDTHMSf(self):
        # Test format "%Y-%m-%dT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['2022-03-28T13:45:00.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDYTHMSf(self):
        # Test format "%m/%d/%YT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['03/28/2022T13:45:00.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMYTHMSf(self):
        # Test format "%d/%m/%YT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['28/03/2022T13:45:00.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMDIMS(self):
        # Test format "%Y-%m-%d %I:%M:%S %p"
        df = pd.DataFrame({'col': ['2022-03-28 01:45:00 PM']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDYIMS(self):
        # Test format "%m/%d/%Y %I:%M:%S %p"
        df = pd.DataFrame({'col': ['03/28/2022 01:45:00 PM']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMYIMS(self):
        # Test format "%d/%m/%Y %I:%M:%S %p"
        df = pd.DataFrame({'col': ['28/03/2022 01:45:00 PM']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_HMS(self):
        # Test format "%H:%M:%S"
        df = pd.DataFrame({'col': ['13:45:30']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_HMSf(self):
        # Test format "%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['13:45:30.123456']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_HM(self):
        # Test format "%H:%M"
        df = pd.DataFrame({'col': ['13:45']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_BdY(self):
        # Test format "%B %d, %Y"
        df = pd.DataFrame({'col': ['December 25, 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_bdY(self):
        # Test format "%b %d, %Y"
        df = pd.DataFrame({'col': ['Dec 25, 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_BY(self):
        # Test format "%B %d %Y"
        df = pd.DataFrame({'col': ['December 25 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_by(self):
        # Test format "%b %d %Y"
        df = pd.DataFrame({'col': ['Dec 25 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dBY(self):
        # Test format "%d %B, %Y"
        df = pd.DataFrame({'col': ['25 December, 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dby(self):
        # Test format "%d %b, %Y"
        df = pd.DataFrame({'col': ['25 Dec, 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dBY(self):
        # Test format "%d %B %Y"
        df = pd.DataFrame({'col': ['25 December 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dby(self):
        # Test format "%d %b %Y"
        df = pd.DataFrame({'col': ['25 Dec 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_BY(self):
        # Test format "%B %Y"
        df = pd.DataFrame({'col': ['December 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_by(self):
        # Test format "%b %Y"
        df = pd.DataFrame({'col': ['Dec 2023']})
        inferred_type = infer_data_type(df, 'col')
        self.assertEqual(inferred_type, 'datetime64')

    # TODO: Need to tackle the confusion with integers
    # def test_datetime_format_Y(self):
    #     # Test format "%Y"
    #     df = pd.DataFrame({'col': ['2023']})
    #     inferred_type = infer_data_type(df, 'col')
    #     self.assertEqual(inferred_type, 'datetime64')

if __name__ == '__main__':
    unittest.main(verbosity=2)