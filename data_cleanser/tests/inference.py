import unittest
import pandas as pd
import numpy as np
import datetime

from data_cleanser.inference import infer_data_type, infer_data_types

class TestInference(unittest.TestCase):

    def test_int64_inference(self):
        # Integers that fit within int64 but not int32
        df = pd.DataFrame({'col': [2**31, -2**31 - 1]})
        self.assertEqual(infer_data_type(df['col']), 'int64')

    def test_int32_inference(self):
        # Integers that fit within int32 but not int16
        df = pd.DataFrame({'col': [2**31 - 1, -2**31]})
        self.assertEqual(infer_data_type(df['col']), 'int32')

    def test_int16_inference(self):
        # Integers that fit within int16 but not int8
        df = pd.DataFrame({'col': [2**15 - 1, -2**15]})
        self.assertEqual(infer_data_type(df['col']), 'int16')

    def test_int8_inference(self):
        # Integers that fit within int8
        df = pd.DataFrame({'col': [2**7 - 1, -2**7]})
        self.assertEqual(infer_data_type(df['col']), 'int8')

    def test_int64_inference_with_nan(self):
        # Integers that fit within int64 but not int32, with NaN values included
        df = pd.DataFrame({'col': [2**31, -2**31 - 1, 3, None]})
        self.assertEqual(infer_data_type(df['col']), 'int64')

    def test_float64_inference(self):
        # Float values that require float64 precision
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308]})
        self.assertEqual(infer_data_type(df['col']), 'float64')

    def test_float32_inference(self):
        # Float values that fit within float32
        df = pd.DataFrame({'col': [3.402823e+30, -3.402823e+30]})
        self.assertEqual(infer_data_type(df['col']), 'float32')

    def test_float64_with_nan(self):
        # Float values that require float64 precision
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308, 12.5, None, 'not a number']})
        self.assertEqual(infer_data_type(df['col']), 'float64')

    def test_mixed_numeric_inference(self):
        # Integers, Floats and NaN all mixed in the data
        mixed_data = [100, 200.5, np.nan, -500, 350.0, 400, 1.5e2, -2.5e2, 0, 'not a number', None, 230]
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df['col']), 'float32')

    def test_numeric_string_inference(self):
        # Numeric values stored as strings
        numbers_as_string = ['1.7976931348623157e+308', '-1.7976931348623157e+308']
        df = pd.DataFrame({'col': numbers_as_string})
        self.assertEqual(infer_data_type(df['col']), 'float64')

    def test_numeric_commas_inference(self):
        # Numeric values with commas as thousands separators
        mixed_data = ['1,000', '2,500', '10,000', '100,000', '1,000,000']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df['col']), 'int64')

    def test_numeric_commas_mixed_with_floats_inference(self):
        # Mixed data with numbers containing commas and floats
        mixed_data = ['1,000', '2,500', '10,000', '100,000', '1,000,000', '3.14', '6,543.21']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df['col']), 'float64')

    def test_numeric_commas_mixed_with_non_numeric_inference(self):
        # Mixed data with numbers containing commas, floats, and non-numeric values
        mixed_data = ['1,000', '2,500', '10,000', '100,000', '1,000,000', '3.14', '6,543.21', 'not a number']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df['col']), 'float64')

    def test_numeric_commas_with_decimal_places_inference(self):
        # Numeric values with commas as thousands separators and decimal places
        mixed_data = ['1,000.50', '2,500.75', '10,000.25', '100,000.60', '1,000,000.99']
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(infer_data_type(df['col']), 'float64')
        
    def test_date_format_YMD(self):
        # Test format "%Y-%m-%d"
        df = pd.DataFrame({'col': ['2022-03-28']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_date_format_MDY(self):
        # Test format "%m/%d/%Y"
        df = pd.DataFrame({'col': ['03/28/2022']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_date_format_MDY_2(self):
        # Test format "%m/%d/%Y"
        df = pd.DataFrame({'col': ['3/28/2022']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_date_format_DMY(self):
        # Test format "%d/%m/%Y"
        df = pd.DataFrame({'col': ['28/03/2022']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMD_HMS(self):
        # Test format "%Y-%m-%d %H:%M:%S"
        df = pd.DataFrame({'col': ['2022-03-28 13:45:30']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDY_HMS(self):
        # Test format "%m/%d/%Y %H:%M:%S"
        df = pd.DataFrame({'col': ['03/28/2022 13:45:30']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMY_HMS(self):
        # Test format "%d/%m/%Y %H:%M:%S"
        df = pd.DataFrame({'col': ['28/03/2022 13:45:30']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMD_HMS_f(self):
        # Test format "%Y-%m-%d %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['2022-03-28 13:45:30.123456']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDY_HMS_f(self):
        # Test format "%m/%d/%Y %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['03/28/2022 13:45:30.123456']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMY_HMS_f(self):
        # Test format "%d/%m/%Y %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['28/03/2022 13:45:30.123456']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMD_HM(self):
        # Test format "%Y-%m-%d %H:%M"
        df = pd.DataFrame({'col': ['2022-03-28 13:45']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDY_HM(self):
        # Test format "%m/%d/%Y %H:%M"
        df = pd.DataFrame({'col': ['03/28/2022 13:45']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMY_HM(self):
        # Test format "%d/%m/%Y %H:%M"
        df = pd.DataFrame({'col': ['28/03/2022 13:45']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMDTHMS(self):
        # Test format "%Y-%m-%dT%H:%M:%S"
        df = pd.DataFrame({'col': ['2022-03-28T13:45:00']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDYTHMS(self):
        # Test format "%m/%d/%YT%H:%M:%S"
        df = pd.DataFrame({'col': ['03/28/2022T13:45:00']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMYTHMS(self):
        # Test format "%d/%m/%YT%H:%M:%S"
        df = pd.DataFrame({'col': ['28/03/2022T13:45:00']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMDTHMSf(self):
        # Test format "%Y-%m-%dT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['2022-03-28T13:45:00.123456']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDYTHMSf(self):
        # Test format "%m/%d/%YT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['03/28/2022T13:45:00.123456']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMYTHMSf(self):
        # Test format "%d/%m/%YT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['28/03/2022T13:45:00.123456']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_YMDIMS(self):
        # Test format "%Y-%m-%d %I:%M:%S %p"
        df = pd.DataFrame({'col': ['2022-03-28 01:45:00 PM']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_MDYIMS(self):
        # Test format "%m/%d/%Y %I:%M:%S %p"
        df = pd.DataFrame({'col': ['03/28/2022 01:45:00 PM']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_DMYIMS(self):
        # Test format "%d/%m/%Y %I:%M:%S %p"
        df = pd.DataFrame({'col': ['28/03/2022 01:45:00 PM']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    # Primarily needs to be inferred as timedelta
    # def test_datetime_format_HMS(self):
    #     # Test format "%H:%M:%S"
    #     df = pd.DataFrame({'col': ['13:45:30']})
    #     inferred_type = infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, 'datetime64')

    # def test_datetime_format_HMSf(self):
    #     # Test format "%H:%M:%S.%f"
    #     df = pd.DataFrame({'col': ['13:45:30.123456']})
    #     inferred_type = infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, 'datetime64')

    # def test_datetime_format_HM(self):
    #     # Test format "%H:%M"
    #     df = pd.DataFrame({'col': ['13:45']})
    #     inferred_type = infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_BdY(self):
        # Test format "%B %d, %Y"
        df = pd.DataFrame({'col': ['December 25, 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_bdY(self):
        # Test format "%b %d, %Y"
        df = pd.DataFrame({'col': ['Dec 25, 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_BY(self):
        # Test format "%B %d %Y"
        df = pd.DataFrame({'col': ['December 25 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_by(self):
        # Test format "%b %d %Y"
        df = pd.DataFrame({'col': ['Dec 25 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dBY(self):
        # Test format "%d %B, %Y"
        df = pd.DataFrame({'col': ['25 December, 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dby(self):
        # Test format "%d %b, %Y"
        df = pd.DataFrame({'col': ['25 Dec, 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dBY(self):
        # Test format "%d %B %Y"
        df = pd.DataFrame({'col': ['25 December 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_dby(self):
        # Test format "%d %b %Y"
        df = pd.DataFrame({'col': ['25 Dec 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_BY(self):
        # Test format "%B %Y"
        df = pd.DataFrame({'col': ['December 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    def test_datetime_format_by(self):
        # Test format "%b %Y"
        df = pd.DataFrame({'col': ['Dec 2023']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'datetime64')

    # TODO: Need to tackle the confusion with integers
    # def test_datetime_format_Y(self):
    #     # Test format "%Y"
    #     df = pd.DataFrame({'col': ['2023']})
    #     inferred_type = infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, 'datetime64')
        
    def test_timedelta_format_HH_MM_SS(self):
        # Test format HH:MM:SS
        df = pd.DataFrame({'col': ['12:34:56']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    def test_timedelta_format_HH_MM_SS_SSS(self):
        # Test format HH:MM:SS.SSS
        df = pd.DataFrame({'col': ['12:34:56.789']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    def test_timedelta_format_DD_days_HH_MM_SS(self):
        # Test format DD days HH:MM:SS
        df = pd.DataFrame({'col': ['5 days 12:34:56']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    def test_timedelta_format_DD_days_HH_MM_SS_SSS(self):
        # Test format DD days HH:MM:SS.SSS
        df = pd.DataFrame({'col': ['5 days 12:34:56.789']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    def test_timedelta_format_DD_HH_MM_SS(self):
        # Test format DD:HH:MM:SS
        df = pd.DataFrame({'col': ['5:12:34:56']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    def test_timedelta_format_DD_HH_MM_SS_SSS(self):
        # Test format DD:HH:MM:SS.SSS
        df = pd.DataFrame({'col': ['5:12:34:56.789']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    def test_timedelta_format_DD_HH_MM_SS_comma_SSS(self):
        # Test format DD:HH:MM:SS,SSS
        df = pd.DataFrame({'col': ['5:12:34:56,789']})
        inferred_type = infer_data_type(df['col'])
        self.assertEqual(inferred_type, 'timedelta64[ns]')

    """
    Testing boolean data
    """
    def test_numeric_1_0(self):
        # Test '1' and '0'
        df = pd.DataFrame({'col': ['1', '0']})
        self.assertEqual(infer_data_type(df['col']), 'bool')

    def test_boolean_True_False(self):
        # Test 'True' and 'False'
        df = pd.DataFrame({'col': ['True', 'False']})
        self.assertEqual(infer_data_type(df['col']), 'bool')

    def test_boolean_TRUE_FALSE(self):
        # Test 'TRUE' and 'FALSE'
        df = pd.DataFrame({'col': ['TRUE', 'FALSE']})
        self.assertEqual(infer_data_type(df['col']), 'bool')

    def test_boolean_true_false(self):
        # Test 'true' and 'false'
        df = pd.DataFrame({'col': ['true', 'false']})
        self.assertEqual(infer_data_type(df['col']), 'bool')

    def test_boolean_T_F(self):
        # Test 'T' and 'F'
        df = pd.DataFrame({'col': ['T', 'F']})
        self.assertEqual(infer_data_type(df['col']), 'bool')

    def test_boolean_True_False_mixed_case(self):
        # Test 'True', 'False', 'true', 'false' in mixed case
        df = pd.DataFrame({'col': ['True', 'False', 'true', 'false']})
        self.assertEqual(infer_data_type(df['col']), 'bool')

    """
    Testing categorical data
    """
    def test_single_category(self):
        # Test a single category
        df = pd.DataFrame({'col': ['A'] * 8 + ['B']})
        self.assertEqual(infer_data_type(df['col']), 'category')

    def test_multiple_categories(self):
        # Test multiple categories
        df = pd.DataFrame({'col': ['A'] * 5 + ['B'] * 5 + ['C']})
        self.assertEqual(infer_data_type(df['col']), 'category')

    def test_mixed_categories_and_strings(self):
        # Test mixed categories and strings
        df = pd.DataFrame({'col': ['A'] * 6 + ['B'] * 3 + ['C'] * 2 + ['other category']})
        self.assertEqual(infer_data_type(df['col']), 'category')

    # def test_categories_with_spaces(self):
    #     # Test categories with leading/trailing spaces
    #     df = pd.DataFrame({'col': [' A'] * 5 + ['B '] * 5 + [' C ']})
    #     self.assertEqual(infer_data_type(df['col']), 'category')

    def test_categories_with_different_cases(self):
        # Test categories with different cases
        df = pd.DataFrame({'col': ['A'] * 4 + ['B'] * 3 + ['b'] * 3 + ['C'] + ['D']})
        self.assertEqual(infer_data_type(df['col']), 'category')

    # def test_categories_with_numeric_values(self):
    #     # Test categories with numeric values
    #     df = pd.DataFrame({'col': [1] * 5 + [2] * 4 + [3]})
    #     self.assertEqual(infer_data_type(df['col']), 'category')

    # def test_categories_with_numeric_values_mixed(self):
    #     # Test categories with numeric values mixed with string values
    #     df = pd.DataFrame({'col': ['1'] * 5 + [2] * 4 + ['A'] * 2})
    #     self.assertEqual(infer_data_type(df['col']), 'category')

    def test_categories_with_nan_values(self):
        # Test categories with NaN values
        df = pd.DataFrame({'col': ['A'] * 4 + ['B'] * 3 + ['C'] + [float('nan')] * 2})
        self.assertEqual(infer_data_type(df['col']), 'category')

    def test_categories_with_duplicates(self):
        # Test categories with duplicate values
        df = pd.DataFrame({'col': ['A'] * 3 + ['B'] * 2 + ['A']})
        self.assertEqual(infer_data_type(df['col']), 'category')

    # def test_empty_dataframe(self):
    #     # Test an empty dataframe
    #     df = pd.DataFrame({'col': []})
    #     self.assertEqual(infer_data_type(df['col']), 'category')

if __name__ == '__main__':
    unittest.main(verbosity=2)