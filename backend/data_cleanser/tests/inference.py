import unittest
import pandas as pd
import numpy as np

from data_cleanser.inference import Inference
from data_cleanser.data_types import DataTypes


inference_engine = Inference(0.5) # Initialising Inference object with inference threshold percentage of 50%

class TestNumericDataTypeInference(unittest.TestCase):
    """
    Unit tests for numeric data type inference.
    """

    def test_int64_inference(self):
        # Integers that fit within int64 but not int32
        df = pd.DataFrame({'col': [2**31, -2**31 - 1]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.INT64)

    def test_int32_inference(self):
        # Integers that fit within int32 but not int16
        df = pd.DataFrame({'col': [2**31 - 1, -2**31]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.INT32)

    def test_int16_inference(self):
        # Integers that fit within int16 but not int8
        df = pd.DataFrame({'col': [2**15 - 1, -2**15]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.INT16)

    def test_int8_inference(self):
        # Integers that fit within int8
        df = pd.DataFrame({'col': [2**7 - 1, -2**7]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.INT8)

    def test_int32_inference_with_nan_and_invalid_value(self):
        # Integers that fit within int64 but not int32, with NaN and invalid values included
        df = pd.DataFrame({'col': [2**31 - 1, -2**31, 3, None, 'not a number']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.INT32)

    def test_float64_inference(self):
        # Float values that require float64 precision
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT64)

    def test_float32_inference(self):
        # Float values that fit within float32
        df = pd.DataFrame({'col': [3.402823e+30, -3.402823e+30]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT32)

    def test_float64_with_nan_and_invalid_values(self):
        # Float values that require float64 precision, with NaN and invalid values included
        df = pd.DataFrame({'col': [1.7976931348623157e+308, -1.7976931348623157e+308, 12.5, None, 'not a number']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT64)

    def test_mixed_numeric_inference(self):
        # Integers, Floats and NaN all mixed in the data with more than 50% numeric values share
        mixed_data = [100, 200.5, -500, 350.0, 400, 1.5e2, -2.5e2, 0, 230, np.nan, 'not a number', None]
        df = pd.DataFrame({'col': mixed_data})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT32)

    def test_numeric_string_inference(self):
        # Numeric values stored as strings
        df = pd.DataFrame({'col': ['1.7976931348623157e+308', '-1.7976931348623157e+308']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT64)

    def test_numeric_commas_inference(self):
        # Numeric values with commas as thousands separators
        df = pd.DataFrame({'col': ['1,000', '2,500', '10,000', '100,000', '1,000,000']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.INT64)

    def test_numeric_commas_mixed_with_floats_inference(self):
        # Mixed data with numbers containing commas and floats
        df = pd.DataFrame({'col': ['1,000', '2,500', '10,000', '100,000', '1,000,000', '3.14', '6,543.21']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT64)

    def test_numeric_commas_mixed_with_non_numeric_inference(self):
        # Mixed data with numbers containing commas, floats, and non-numeric values with majority share of numeric values (> 50%)
        df = pd.DataFrame({'col': ['1,000', '2,500', '10,000', '100,000', '1,000,000', '3.14', '6,543.21', 'not a number']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT64)

    def test_numeric_commas_with_decimal_places_inference(self):
        # Numeric values with commas as thousands separators and decimal places
        df = pd.DataFrame({'col': ['1,000.50', '2,500.75', '10,000.25', '100,000.60', '1,000,000.99']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.FLOAT64)
        
class TestDateTimeDataTypeInference(unittest.TestCase):
    """
    Unit tests for datetime data type inference.
    """

    def test_date_format_YMD(self):
        # Date string with format "%Y-%m-%d"
        df = pd.DataFrame({'col': ['2022-03-28']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_date_format_MDY(self):
        # Date string with format "%m/%d/%Y"
        df = pd.DataFrame({'col': ['03/28/2022']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_date_format_MDY_2(self):
        # Date string with format "%m/%d/%Y"
        df = pd.DataFrame({'col': ['3/28/2022']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_date_format_DMY(self):
        # Date string with format "%d/%m/%Y"
        df = pd.DataFrame({'col': ['28/03/2022']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_YMD_HMS(self):
        # Date string with format "%Y-%m-%d %H:%M:%S"
        df = pd.DataFrame({'col': ['2022-03-28 13:45:30']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_MDY_HMS(self):
        # Date string with format "%m/%d/%Y %H:%M:%S"
        df = pd.DataFrame({'col': ['03/28/2022 13:45:30']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_DMY_HMS(self):
        # Date string with format "%d/%m/%Y %H:%M:%S"
        df = pd.DataFrame({'col': ['28/03/2022 13:45:30']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_YMD_HMS_f(self):
        # Date string with format "%Y-%m-%d %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['2022-03-28 13:45:30.123456']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_MDY_HMS_f(self):
        # Date string with format "%m/%d/%Y %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['03/28/2022 13:45:30.123456']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_DMY_HMS_f(self):
        # Date string with format "%d/%m/%Y %H:%M:%S.%f"
        df = pd.DataFrame({'col': ['28/03/2022 13:45:30.123456']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_YMD_HM(self):
        # Date string with format "%Y-%m-%d %H:%M"
        df = pd.DataFrame({'col': ['2022-03-28 13:45']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_MDY_HM(self):
        # Date string with format "%m/%d/%Y %H:%M"
        df = pd.DataFrame({'col': ['03/28/2022 13:45']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_DMY_HM(self):
        # Date string with format "%d/%m/%Y %H:%M"
        df = pd.DataFrame({'col': ['28/03/2022 13:45']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_YMDTHMS(self):
        # Date string with format "%Y-%m-%dT%H:%M:%S"
        df = pd.DataFrame({'col': ['2022-03-28T13:45:00']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_MDYTHMS(self):
        # Date string with format "%m/%d/%YT%H:%M:%S"
        df = pd.DataFrame({'col': ['03/28/2022T13:45:00']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_DMYTHMS(self):
        # Date string with format "%d/%m/%YT%H:%M:%S"
        df = pd.DataFrame({'col': ['28/03/2022T13:45:00']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_YMDTHMSf(self):
        # Date string with format "%Y-%m-%dT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['2022-03-28T13:45:00.123456']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_MDYTHMSf(self):
        # Date string with format "%m/%d/%YT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['03/28/2022T13:45:00.123456']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_DMYTHMSf(self):
        # Date string with format "%d/%m/%YT%H:%M:%S.%f"
        df = pd.DataFrame({'col': ['28/03/2022T13:45:00.123456']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_YMDIMS(self):
        # Date string with format "%Y-%m-%d %I:%M:%S %p"
        df = pd.DataFrame({'col': ['2022-03-28 01:45:00 PM']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_MDYIMS(self):
        # Date string with format "%m/%d/%Y %I:%M:%S %p"
        df = pd.DataFrame({'col': ['03/28/2022 01:45:00 PM']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_DMYIMS(self):
        # Date string with format "%d/%m/%Y %I:%M:%S %p"
        df = pd.DataFrame({'col': ['28/03/2022 01:45:00 PM']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    # Primarily needs to be inferred as timedelta
    # def test_datetime_format_HMS(self):
    #     # Test format "%H:%M:%S"
    #     df = pd.DataFrame({'col': ['13:45:30']})
    #     inferred_type = inference_engine.infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, DataTypes.DATETIME64)

    # def test_datetime_format_HMSf(self):
    #     # Test format "%H:%M:%S.%f"
    #     df = pd.DataFrame({'col': ['13:45:30.123456']})
    #     inferred_type = inference_engine.infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, DataTypes.DATETIME64)

    # def test_datetime_format_HM(self):
    #     # Test format "%H:%M"
    #     df = pd.DataFrame({'col': ['13:45']})
    #     inferred_type = inference_engine.infer_data_type(df['col'])
    #     self.assertEqual(inferred_type, DataTypes.DATETIME64)

    def test_datetime_format_BdY(self):
        # Date string with format "%B %d, %Y"
        df = pd.DataFrame({'col': ['December 25, 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_bdY(self):
        # Date string with format "%b %d, %Y"
        df = pd.DataFrame({'col': ['Dec 25, 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_BY(self):
        # Date string with format "%B %d %Y"
        df = pd.DataFrame({'col': ['December 25 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_by(self):
        # Date string with format "%b %d %Y"
        df = pd.DataFrame({'col': ['Dec 25 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_dBY(self):
        # Date string with format "%d %B, %Y"
        df = pd.DataFrame({'col': ['25 December, 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_dby(self):
        # Date string with format "%d %b, %Y"
        df = pd.DataFrame({'col': ['25 Dec, 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_dBY(self):
        # Date string with format "%d %B %Y"
        df = pd.DataFrame({'col': ['25 December 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_dby(self):
        # Date string with format "%d %b %Y"
        df = pd.DataFrame({'col': ['25 Dec 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_BY(self):
        # Date string with format "%B %Y"
        df = pd.DataFrame({'col': ['December 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

    def test_datetime_format_by(self):
        # Date string with format "%b %Y"
        df = pd.DataFrame({'col': ['Dec 2023']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.DATETIME64)

class TestTimeDeltaDataTypeInference(unittest.TestCase):
    """
    Unit tests for timedelta data type inference.
    """ 

    def test_timedelta_format_HH_MM_SS(self):
        # Timedelta string with format HH:MM:SS
        df = pd.DataFrame({'col': ['12:34:56']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)

    def test_timedelta_format_HH_MM_SS_SSS(self):
        # Timedelta string with format HH:MM:SS.SSS
        df = pd.DataFrame({'col': ['12:34:56.789']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)

    def test_timedelta_format_DD_days_HH_MM_SS(self):
        # Timedelta string with format DD days HH:MM:SS
        df = pd.DataFrame({'col': ['5 days 12:34:56']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)

    def test_timedelta_format_DD_days_HH_MM_SS_SSS(self):
        # Timedelta string with format DD days HH:MM:SS.SSS
        df = pd.DataFrame({'col': ['5 days 12:34:56.789']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)

    def test_timedelta_format_DD_HH_MM_SS(self):
        # Timedelta string with format DD:HH:MM:SS
        df = pd.DataFrame({'col': ['5:12:34:56']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)

    def test_timedelta_format_DD_HH_MM_SS_SSS(self):
        # Timedelta string with format DD:HH:MM:SS.SSS
        df = pd.DataFrame({'col': ['5:12:34:56.789']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)

    def test_timedelta_format_DD_HH_MM_SS_comma_SSS(self):
        # Timedelta string with format DD:HH:MM:SS,SSS
        df = pd.DataFrame({'col': ['5:12:34:56,789']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.TIMEDELTA64)


class TestBooleanDataTypeInference(unittest.TestCase):
    """
    Unit tests for boolean data type inference.
    """ 
    def test_numeric_1_0(self):
        # Boolean string with format '1' and '0'
        df = pd.DataFrame({'col': ['1', '0']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.BOOLEAN)

    def test_boolean_True_False(self):
        # Boolean string with format 'True' and 'False'
        df = pd.DataFrame({'col': ['True', 'False']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.BOOLEAN)

    def test_boolean_TRUE_FALSE(self):
        # Boolean string with format 'TRUE' and 'FALSE'
        df = pd.DataFrame({'col': ['TRUE', 'FALSE']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.BOOLEAN)

    def test_boolean_true_false(self):
        # Boolean string with format 'true' and 'false'
        df = pd.DataFrame({'col': ['true', 'false']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.BOOLEAN)

    def test_boolean_T_F(self):
        # Boolean string with format 'T' and 'F'
        df = pd.DataFrame({'col': ['T', 'F']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.BOOLEAN)

    def test_boolean_True_False_mixed_case(self):
        # Boolean string with format mixed case such as 'True', 'False', 'true', 'false'
        df = pd.DataFrame({'col': ['True', 'False', 'true', 'false']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.BOOLEAN)

   
class TestCategoricalDataTypeInference(unittest.TestCase):
    """
    Unit tests for categorical data type inference.
    """ 
   
    def test_single_category(self):
        # Single category
        df = pd.DataFrame({'col': ['A'] * 8})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_multiple_categories(self):
        # Multiple categories
        df = pd.DataFrame({'col': ['A'] * 5 + ['B'] * 5 + ['C']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_mixed_categories_and_strings(self):
        # Mixed categories and strings with majority share of unique categories (> 50%)
        df = pd.DataFrame({'col': ['A'] * 6 + ['B'] * 3 + ['C'] * 2 + ['other category']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_categories_with_spaces(self):
        # Categories with leading/trailing spaces
        df = pd.DataFrame({'col': [' A'] * 5 + ['B '] * 5 + [' C ']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_categories_with_different_cases(self):
        # Categories with different cases
        df = pd.DataFrame({'col': ['A'] * 4 + ['B'] * 3 + ['b'] * 3 + ['C'] + ['D']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_categories_with_numeric_values(self):
        # Categories with numeric values
        df = pd.DataFrame({'col': [1] * 5 + [2] * 4 + [3]})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_categories_with_numeric_values_mixed(self):
        # Categories with numeric values mixed with string values
        df = pd.DataFrame({'col': ['1'] * 5 + [2] * 4 + ['A'] * 2})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_categories_with_nan_values(self):
        # Categories with NaN values
        df = pd.DataFrame({'col': ['A'] * 4 + ['B'] * 3 + ['C'] + [float('nan')] * 2})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

    def test_categories_with_duplicates(self):
        # Categories with duplicate values
        df = pd.DataFrame({'col': ['A'] * 3 + ['B'] * 2 + ['A']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.CATEGORY)

class TestComplexDataTypeInference(unittest.TestCase):
    """
    Unit tests for complex data type inference.
    """ 

    def test_standard_form(self):
        # Complex data of standard form: a + bj
        df = pd.DataFrame({'col': ['1+2j', '3+4j', '5+6j']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.COMPLEX)

    def test_parentheses_form(self):
        # Complex data of parentheses form: (a + bj) or (a, b)
        df = pd.DataFrame({'col': ['(1+2j)', '(3+4j)', '(5+6j)']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.COMPLEX)

    def test_exponential_form(self):
        # Complex data of exponential form: a + b*j or a + bj
        df = pd.DataFrame({'col': ['1+2*j', '3+4*j', '5+6*j']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.COMPLEX)

    # TODO: Handle the following format
    # def test_polar_form(self):
    #     # Complex data of polar form: r * (cos(theta) + j*sin(theta))
    #     df = pd.DataFrame({'col': ['1*(cos(0)+j*sin(0))', '2*(cos(1)+j*sin(1))', '3*(cos(2)+j*sin(2))']})
    #     self.assertEqual(infer_data_type(df['col']), DataTypes.COMPLEX)

    def test_tuple_form(self):
        # Complex data of tuple form: (a, b)
        df = pd.DataFrame({'col': ['(1, 2)', '(3, 4)', '(5, 6)']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.COMPLEX)

    def test_mixed_formats(self):
        # Complex data of mixed formats
        df = pd.DataFrame({'col': ['1+2j', '(3, 4)', '5+6*j']})
        self.assertEqual(inference_engine.infer_data_type(df['col']), DataTypes.COMPLEX)

    def test_invalid_formats(self):
        # Complex data of invalid formats
        df = pd.DataFrame({'col': ['1+2', '3+j', '5*6j']})
        self.assertNotEqual(inference_engine.infer_data_type(df['col']), DataTypes.COMPLEX)

class TestDataFrameInference(unittest.TestCase):
    """
    Unit tests for complete dataframes
    """

    def test_infer_data_types():
        # Basic DataFrame columns data type inference

        data = {
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Birthdate': ['1/01/1990', '2/02/1991', '3/03/1992', '4/04/1993', '5/05/1994'],
            'Score': [90, 75, 85, 70, 'Not Available'],
            'Grade': ['A', 'B', 'A', 'B', 'A'],
            'Is_Citizen': [True, False, True, False, True],
            'Blood_Group': ['A', 'B', 'B', 'B', 'A'],
            'Complex': ['1 + 2j', '3 + 4j', '5 + 6j', '7 + 8j', '9 + 10j'],
            'Object': [object(), object(), object(), object(), object()],
        }
        df = pd.DataFrame(data)

        inferred_types = inference_engine.infer_data_types(df)

        assert inferred_types['Name'] == DataTypes.OBJECT
        assert inferred_types['Birthdate'] == DataTypes.DATETIME64
        assert inferred_types['Score'] == DataTypes.INT8
        assert inferred_types['Grade'] == DataTypes.CATEGORY
        assert inferred_types['Is_Citizen'] == DataTypes.BOOLEAN
        assert inferred_types['Blood_Group'] == DataTypes.CATEGORY
        assert inferred_types['Complex'] == DataTypes.COMPLEX
        assert inferred_types['Object'] == DataTypes.OBJECT

if __name__ == '__main__':
    unittest.main()