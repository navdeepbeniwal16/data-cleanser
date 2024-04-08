import unittest
import pandas as pd
import numpy as np
import pytest
from data_cleanser.conversion import Convertor
from data_cleanser.data_types import DataTypes

conversion_engine = Convertor()

class TestConverionToDatetimeType(unittest.TestCase):
    """
    Unit tests to test conversion to datetime data type
    """
    def test_convert_column_to_datetime_existing_column(self):
        # Test converting an existing object type column to datetime
        df = pd.DataFrame({'dates_valid': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']})
        column_name = 'dates_valid'
        assert df[column_name].dtype == 'object'
        result = conversion_engine.convert_column_to_datetime(df, column_name)
        assert str(result[column_name].dtype) == 'datetime64[ns]'

    def test_convert_column_to_datetime_non_existing_column(self):
        # Test converting a non-existing column
        df = pd.DataFrame({'dates_valid': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']})
        with pytest.raises(KeyError):
            conversion_engine.convert_column_to_datetime(df, 'non_existing_column')

    def test_convert_column_to_datetime_raise_exception_with_invalid_values(self):
        # Test converting a column with invalid values
        df = pd.DataFrame({'dates_invalid': ['2022-01-01', 'invalid', '2022-03-01', '2022-04-01']})
        column_name = 'dates_invalid'
        with pytest.raises(ValueError):
            conversion_engine.convert_column_to_datetime(df, column_name)

    def test_convert_column_to_datetime_coerce_errors_with_invalid_values(self):
        # Test converting a column with invalid values and 'coerce' errors
        df = pd.DataFrame({'dates_invalid': ['2022-01-01', 'invalid', '2022-03-01', '2022-04-01']})
        column_name = 'dates_invalid'
        result = conversion_engine.convert_column_to_datetime(df, column_name, errors='coerce')
        assert pd.isna(result[column_name]).sum() == 1

    def test_convert_column_to_datetime_no_changes_in_original_df(self):
        # Test that the original DataFrame is not modified
        df = pd.DataFrame({'dates_valid': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']})
        column_name = 'dates_valid'
        conversion_engine.convert_column_to_datetime(df, column_name)
        assert 'dates_valid' in df.columns  # Check that the column still exists in the original DataFrame

    def test_convert_column_to_datetime_missing_values_ignore(self):
        # Test converting a column with missing values and 'ignore' missing_values option
        column_name = 'dates_missing'
        df = pd.DataFrame({'dates_missing': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', np.nan ]})
        result = conversion_engine.convert_column_to_datetime(df, column_name, missing_values='ignore')
        assert pd.isna(result[column_name]).sum() == 1  # One missing value should remain as NaN

    def test_convert_column_to_datetime_missing_values_default(self):
        # Test converting a column with missing values and 'default' missing_values option
        column_name = 'dates_missing'
        df = pd.DataFrame({'dates_missing': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', np.nan ]})
        default_value = pd.Timestamp.now()
        result = conversion_engine.convert_column_to_datetime(df, column_name, missing_values='default', default_value=default_value)
        assert result[column_name].dtype == 'datetime64[ns]'
        assert pd.isna(result[column_name]).sum() == 0  # Missing value should be replaced with default_value

    def test_convert_column_to_datetime_missing_values_delete(self):
        # Test converting a column with missing values and 'delete' missing_values option
        column_name = 'dates_missing'
        df = pd.DataFrame({'dates_missing': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', np.nan ]})
        result = conversion_engine.convert_column_to_datetime(df, column_name, missing_values='delete')
        assert result[column_name].dtype == 'datetime64[ns]'
        assert pd.isna(result[column_name]).sum() == 0  # Missing value should be deleted

class TestConverionToCategoryType(unittest.TestCase):
    """
    Unit tests to test conversion to categorical data type
    """

    def test_convert_column_to_category_existing_column(self):
        # Test converting an existing column to category
        df = pd.DataFrame({'category_column': ['A', 'B', 'C', 'A', 'B', 'C']})
        column_name = 'category_column'
        assert df[column_name].dtype == 'object'
        result = conversion_engine.convert_column_to_category(df, column_name)
        assert result[column_name].dtype == 'category'

    def test_convert_column_to_category_non_existing_column(self):
        # Test converting a non-existing column
        df = pd.DataFrame({'category_column': ['A', 'B', 'C', 'A', 'B', 'C']})
        column_name = 'non_existing_column'
        with pytest.raises(KeyError):
            conversion_engine.convert_column_to_category(df, column_name)

    def test_convert_column_to_category_empty_dataframe(self):
        # Test converting a column in an empty DataFrame
        df = pd.DataFrame()
        column_name = 'category_column'
        with pytest.raises(KeyError):
            conversion_engine.convert_column_to_category(df, column_name)

    def test_convert_column_to_category_ignore_missing_values(self):
        # Test converting a column with missing values and 'ignore' option
        df = pd.DataFrame({'category_column': ['A', 'B', None, 'A', 'B', 'C']})
        column_name = 'category_column'
        result = conversion_engine.convert_column_to_category(df, column_name, missing_values='ignore')
        assert result[column_name].dtype == 'category'

    def test_convert_column_to_category_default_missing_values(self):
        # Test converting a column with missing values and 'default' option
        df = pd.DataFrame({'category_column': ['A', 'B', None, 'A', 'B', 'C']})
        column_name = 'category_column'
        result = conversion_engine.convert_column_to_category(df, column_name, missing_values='default', default_value='default value')
        assert result[column_name].dtype == 'category'
        assert result[column_name].isna().sum() == 0

    def test_convert_column_to_category_delete_missing_values(self):
        # Test converting a column with missing values and 'delete' option
        df = pd.DataFrame({'category_column': ['A', 'B', None, 'A', 'B', 'C']})
        column_name = 'category_column'
        result = conversion_engine.convert_column_to_category(df, column_name, missing_values='delete')
        assert result[column_name].dtype == 'category'
        assert result[column_name].isna().sum() == 0

class TestConverionToBooleanType(unittest.TestCase):
    """
    Unit tests to test conversion to boolean data type
    """

    def test_convert_column_to_boolean_values(self):
        # Test converting an existing column to boolean
        column_name = 'col'
        df = pd.DataFrame({column_name: [True, False, True, False]})
        assert df[column_name].dtype == 'bool'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert str(result[column_name].dtype) == 'bool'

    def test_convert_column_to_boolean_values_strings(self):
        # Test converting an existing column to boolean
        column_name = 'col'
        df = pd.DataFrame({column_name: ['True', 'False', 'True', 'False']})
        assert df[column_name].dtype == 'object'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == DataTypes.BOOLEAN

    def test_convert_column_to_boolean_non_existing_column(self):
        # Test converting a non-existing column
        df = pd.DataFrame({'col': ['True', 'False', 'True', 'False']})
        column_name = 'non_existing_col'
        with pytest.raises(KeyError):
            conversion_engine.convert_column_to_boolean(df, column_name)

    def test_convert_column_to_boolean_empty_dataframe(self):
        # Test converting a column in an empty DataFrame
        df = pd.DataFrame()
        column_name = 'boolean_column'
        with pytest.raises(KeyError):
            conversion_engine.convert_column_to_boolean(df, column_name)

    def test_convert_column_to_boolean_invalid_values_raise(self):
        # Test converting a column with invalid values, with errors='raise'
        df = pd.DataFrame({'bool_column': ['True', 'False', 'invalid', 'True', '']})
        column_name = 'bool_column'
        with pytest.raises(ValueError):
            conversion_engine.convert_column_to_boolean(df, column_name, errors='raise')

    def test_convert_column_to_boolean_invalid_values_ignore(self):
        # Test converting a column with invalid values, with errors='ignore'
        df = pd.DataFrame({'bool_column': ['True', 'False', 'invalid', 'True', '']})
        column_name = 'bool_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name, errors='ignore')
        assert len(result) == 5

    def test_convert_column_to_boolean_invalid_values_coerce(self):
        # Test converting a column with invalid values, with errors='coerce'
        df = pd.DataFrame({'bool_column': ['True', 'False', 'invalid', 'True', '']})
        column_name = 'bool_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name, errors='coerce')
        assert len(result) == 5
        assert pd.isna(result['bool_column'][2])
        assert pd.isna(result['bool_column'][4])

    def test_convert_column_to_boolean_missing_values_ignore(self):
        # Test converting a column with missing values, with missing_values='ignore'
        df = pd.DataFrame({'bool_column': ['True', 'False', np.nan, 'True', None]})
        column_name = 'bool_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name, errors='ignore', missing_values='ignore')
        assert len(result) == 5
        assert pd.isna(result['bool_column'][2])
        assert pd.isna(result['bool_column'][4])

    def test_convert_column_to_boolean_missing_values_default(self):
        # Test converting a column with missing values, with missing_values='default'
        df = pd.DataFrame({'bool_column': ['True', 'False', np.nan, 'True', None]})
        column_name = 'bool_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name, errors='ignore', missing_values='default', default_value=True)
        assert len(result) == 5
        assert result['bool_column'][2] == True
        assert result['bool_column'][4] == True

    def test_convert_column_to_boolean_missing_values_delete(self):
        # Test converting a column with missing values, with missing_values='delete'
        df = pd.DataFrame({'bool_column': ['True', 'False', np.nan, 'True', None]})
        column_name = 'bool_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name, errors='ignore', missing_values='delete')
        assert len(result) == 3

    def test_convert_column_to_boolean_lowercase_true_false(self):
        # Test converting a column with 'True' and 'False' values
        df = pd.DataFrame({'boolean_column': ['true', 'false', 'true', 'false']})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False]

    def test_convert_column_to_boolean_uppercase_true_false(self):
        # Test converting a column with 'TRUE' and 'False' values
        df = pd.DataFrame({'boolean_column': ['TRUE', 'FALSE', 'TRUE', 'FALSE']})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False]

    def test_convert_column_to_boolean_1_0_strings(self):
        # Test converting a column with '1' and '0' values
        df = pd.DataFrame({'boolean_column': ['1', '0', '1', '0']})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False]

    def test_convert_column_to_boolean_1_0_numeric(self):
        # Test converting a column with '1' and '0' values
        df = pd.DataFrame({'boolean_column': [1, 0, 1, 0]})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False]

    def test_convert_column_to_boolean_uppercase_t_f(self):
        # Test converting a column with 'T' and 'F' values
        df = pd.DataFrame({'boolean_column': ['T', 'F', 'T', 'F']})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False]

    def test_convert_column_to_boolean_lowercase_t_f(self):
        # Test converting a column with 't' and 'f' values
        df = pd.DataFrame({'boolean_column': ['t', 'f', 't', 'f']})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False]

    def test_convert_column_to_boolean_mixed(self):
        # Test converting a column with 't' and 'f' values
        df = pd.DataFrame({'boolean_column': ['True', 'FALSE', '1', 'f', 'T']})
        column_name = 'boolean_column'
        result = conversion_engine.convert_column_to_boolean(df, column_name)
        assert result[column_name].dtype == 'bool'
        assert result[column_name].tolist() == [True, False, True, False, True]


class TestConvertColumnToNumeric(unittest.TestCase):
    """
    Unit tests to test conversion to Numeric Data type
    """

    def test_convert_column_to_numeric_int8(self):
        # Tests conversion to int8
        column_name = 'col'
        data = {column_name: [-100, 0, 100, 127, -128]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='int8')
        self.assertTrue(result[column_name].dtype == DataTypes.INT8)

    def test_convert_column_to_numeric_int16(self):
        # Tests conversion to int16
        column_name = 'col'
        data = {column_name: [-10000, 0, 10000, 32767, -32768]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='int16')
        self.assertTrue(result[column_name].dtype == DataTypes.INT16)

    def test_convert_column_to_numeric_int32(self):
        # Tests conversion to int32
        column_name = 'col'
        data = {column_name: [-2147483648, 0, 2147483647]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='int32')
        self.assertTrue(result[column_name].dtype == DataTypes.INT32)

    def test_convert_column_to_numeric_int64(self):
        # Tests conversion to int64
        column_name = 'col'
        data = {column_name: [-9223372036854775808, 0, 9223372036854775807]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='int64')
        self.assertTrue(result[column_name].dtype == DataTypes.INT64)

    def test_convert_column_to_numeric_float32(self):
        # Tests conversion to float32
        column_name = 'col'
        data = {column_name: [3.402823466e+38, 0, -3.402823466e+38]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float32')
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT32)

    def test_convert_column_to_numeric_float64(self):
        #  Tests conversion to float64
        column_name = 'col'
        data = {column_name: [1.7976931348623157e+308, 0, -1.7976931348623157e+308]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64')
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)

    def test_convert_column_to_numeric_valid_mixed_data_types(self):
        # Tests handling of valid mixed data types
        column_name = 'col'
        data = {column_name: [1, 2.5, '3', True]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64')
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)

    # Handling invalid numeric values
    def test_convert_column_to_numeric_mixed_data_types_raise_errors(self):
        # Tests raising errors for invalid values
        column_name = 'col'
        data = {column_name: [1, 2.5, '3', 'abc', True]}
        df = pd.DataFrame(data)
        with pytest.raises(ValueError):
            conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64', errors='raise', missing_values='ignore') 

    def test_convert_column_to_numeric_mixed_data_types_coerce_errors(self):
        # Tests coercing errors for invalid values
        column_name = 'col'
        data = {column_name: [1, 2.5, '3', 'abc', True]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64', errors='coerce', missing_values='ignore')
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)
        self.assertTrue(result[column_name].isna().sum() == 1)

    # Handling missing values
    def test_convert_column_to_numeric_mixed_data_types_raise_errors_ignore_missing_values(self):
        # Tests raising errors for invalid values and ignoring missing values
        column_name = 'col'
        data = {column_name: [1, 2.5, 3.9, np.nan, None]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64', errors='raise', missing_values='ignore')
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)
        print("Data:", result[column_name])
        self.assertTrue(pd.isna(result[column_name][3])) 
        self.assertTrue(pd.isna(result[column_name][4]))

    def test_convert_column_to_numeric_mixed_data_types_raise_errors_default_missing_values(self):
        # Tests raising errors for invalid values and using a default value for missing values
        column_name = 'col'
        data = {column_name: [1, 2.5, 3.9, np.nan, None]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64', errors='raise', missing_values='default', default_value=-1)
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)
        self.assertTrue(result[column_name][3] == -1) 
        self.assertTrue(result[column_name][4] == -1) 

    def test_convert_column_to_numeric_mixed_data_types_raise_errors_delete_missing_values(self):
        # Tests raising errors for invalid values and deleting missing values
        column_name = 'col'
        data = {column_name: [1, 2.5, 3.9, np.nan, None]}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64', errors='raise', missing_values='delete')
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)
        self.assertTrue(len(result[column_name]) == 3) # missing values should be deleted

    def test_convert_column_to_numeric_non_standard_numeric_formats(self):
        # Tests conversion of non-standard numeric formats ie comma separated integers, decimals, currency symbols, percentage signs, exponential and scienctific notations 
        column_name = 'col'
        data = {column_name: ['1,000', '$100,00',  '2,050.5', '$2,050.502', '50.5%', '1.23 x 10^5', '1.23e+05'] }
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_numeric(df, column_name, numeric_type='float64')
        print(result)
        self.assertTrue(result[column_name].dtype == DataTypes.FLOAT64)

class TestConvertColumnToTimedelta(unittest.TestCase):
    """
    Unit tests to test conversion to Timedelta type
    """
    column_name = 'col'

    def test_convert_column_to_timedelta_default(self):
        data = {self.column_name: ['1 days', '2 days', '3 days', '4 days', '5 days']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, self.column_name)
        self.assertTrue(result[self.column_name].dtype == DataTypes.TIMEDELTA64)
        self.assertTrue(result[self.column_name][0] == pd.Timedelta(days=1))

    def test_convert_column_to_timedelta_hh_mm_ss(self):
        data = {self.column_name: ['01:02:03']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, self.column_name)
        self.assertTrue(result[self.column_name].dtype == DataTypes.TIMEDELTA64)
        self.assertTrue(result[self.column_name][0] == pd.Timedelta(hours=1, minutes=2, seconds=3))

    def test_convert_column_to_timedelta_hh_mm_ss_sss(self):
        data = {self.column_name: ['01:02:03.456']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, self.column_name)
        self.assertTrue(result[self.column_name].dtype == DataTypes.TIMEDELTA64)
        self.assertTrue(result[self.column_name][0] == pd.Timedelta(hours=1, minutes=2, seconds=3, milliseconds=456))

    def test_convert_column_to_timedelta_dd_days_hh_mm_ss(self):
        data = {self.column_name: ['5 days 01:02:03']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, self.column_name)
        self.assertTrue(result[self.column_name].dtype == DataTypes.TIMEDELTA64)
        self.assertTrue(result[self.column_name][0] == pd.Timedelta(days=5, hours=1, minutes=2, seconds=3))

    def test_convert_column_to_timedelta_dd_days_hh_mm_ss_sss(self):
        data = {'col': ['5 days 01:02:03.456']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, 'col')
        self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
        self.assertTrue(result['col'].iloc[0] == pd.Timedelta(days=5, hours=1, minutes=2, seconds=3, milliseconds=456))

    def test_convert_column_to_timedelta_dd_hh_mm_ss(self):
        data = {'col': ['5:01:02:03']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, 'col')
        self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
        print("Data", result)
        self.assertTrue(result['col'][0] == pd.Timedelta(days=5, hours=1, minutes=2, seconds=3))

    def test_convert_column_to_timedelta_dd_hh_mm_ss_sss(self):
        data = {'col': ['5:01:02:03.456']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, 'col')
        self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
        self.assertTrue(result['col'].iloc[0] == pd.Timedelta(days=5, hours=1, minutes=2, seconds=3, milliseconds=456))

    def test_convert_column_to_timedelta_dd_hh_mm_ss_comma_sss(self):
        data = {'col': ['5:01:02:03,456']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, 'col')
        self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
        self.assertTrue(result['col'].iloc[0] == pd.Timedelta(days=5, hours=1, minutes=2, seconds=3, milliseconds=456))

    def test_convert_column_to_timedelta_DD_days(self):
        column_name = 'col'
        data = {column_name: ['5 days', '10 days', '15 days']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_HH_MM(self):
        column_name = 'col'
        data = {column_name: ['01:02', '10:12', '15:23']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_HH_MM_SS_AM_PM(self):
        column_name = 'col'
        data = {column_name: ['01:02:03 AM', '10:12:23 PM', '12:59:59 AM']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_HH_MM_AM_PM(self):
        column_name = 'col'
        data = {column_name: ['01:02 AM', '10:12 PM', '12:59 AM']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_HH_hours_MM_minutes_SS_seconds(self):
        column_name = 'col'
        data = {column_name: ['1 hours 2 minutes 3 seconds', '5 hours 10 minutes 15 seconds', '10 hours 30 minutes 45 seconds']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_HH_hours_MM_minutes_SS_SSS_seconds(self):
        column_name = 'col'
        data = {column_name: ['1 hours 2 minutes 3.456 seconds', '5 hours 10 minutes 15.789 seconds', '10 hours 30 minutes 45.123 seconds']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_MM_minutes_SS_seconds(self):
        column_name = 'col'
        data = {column_name: ['2 minutes 3 seconds', '10 minutes 15 seconds', '30 minutes 45 seconds']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_MM_minutes_SS_SSS_seconds(self):
        column_name = 'col'
        data = {column_name: ['2 minutes 3.456 seconds', '10 minutes 15.789 seconds', '30 minutes 45.123 seconds']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_SS_seconds(self):
        column_name = 'col'
        data = {column_name: ['3 seconds', '15 seconds', '45 seconds']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_SS_SSS_seconds(self):
        column_name = 'col'
        data = {column_name: ['3.456 seconds', '15.789 seconds', '45.123 seconds']}
        df = pd.DataFrame(data)
        result = conversion_engine.convert_column_to_timedelta(df, column_name)
        self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    def test_convert_column_to_timedelta_with_invalid_values_raise_errors(self):
        column_name = 'col'
        data = {column_name: ['1 days', '2 days', '3 days', '4 days', '5 days', 'invalid']}
        df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            conversion_engine.convert_column_to_timedelta(df, 'col', errors='raise')

    # TODO
    # def test_convert_column_to_timedelta_with_invalid_values_coerce_errors(self):
    #     column_name = 'col'
    #     data = {column_name: ['1 days', '2 days', '3 days', '4 days', '5 days', 'invalid']}
    #     df = pd.DataFrame(data)
    #     result = conversion_engine.convert_column_to_timedelta(df, 'col', errors='coerce')
    #     self.assertTrue(result[column_name].dtype == DataTypes.TIMEDELTA64)

    # def test_convert_column_to_timedelta_coerce_errors(self):
    #     result = conversion_engine.convert_column_to_timedelta(self.df, 'col', errors='coerce')
    #     self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
    #     self.assertTrue(pd.isna(result['col'].iloc[0]))

    # def test_convert_column_to_timedelta_default_missing_values(self):
    #     result = conversion_engine.convert_column_to_timedelta(self.df, 'col', missing_values='default')
    #     self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
    #     self.assertTrue(result['col'].iloc[0] == pd.Timedelta(0))

    # def test_convert_column_to_timedelta_delete_missing_values(self):
    #     result = conversion_engine.convert_column_to_timedelta(self.df, 'col', missing_values='delete')
    #     self.assertTrue(result['col'].dtype == 'timedelta64[ns]')
    #     self.assertTrue(len(result['col']) == 5)

class TestConvertColumnToComplex(unittest.TestCase):
    """
    Unit tests to test conversion to Complex type
    """

    def test_standard_form(self):
        df = pd.DataFrame({'column': ['3+4j', '5+6j', '7+8j']})
        result_df = conversion_engine.convert_column_to_complex(df, 'column')
        expected_dtype = 'complex'
        expected_length = 3
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)

    def test_parentheses_form_with_plus(self):
        df = pd.DataFrame({'column': ['(3+4j)', '(5+6j)']})
        result_df = conversion_engine.convert_column_to_complex(df, 'column')
        expected_dtype = 'complex'
        expected_length = 2
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)

    def test_parentheses_form_with_comma(self):
        df = pd.DataFrame({'column': ['(3, 4)', '(5, 6)']})
        result_df = conversion_engine.convert_column_to_complex(df, 'column')
        expected_dtype = 'complex'
        expected_length = 2
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)

    def test_tuple_form(self):
        df = pd.DataFrame({'column': [(3, 4), (5, 6)]})
        result_df = conversion_engine.convert_column_to_complex(df, 'column')
        expected_dtype = 'complex'
        expected_length = 2
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)

    def test_error_handling_raise(self):
        df = pd.DataFrame({'column': ['invalid', '5+6j']})
        with self.assertRaises(ValueError):
            result_df = conversion_engine.convert_column_to_complex(df, 'column', errors='raise')

    def test_error_handling_coerce(self):
        df = pd.DataFrame({'column': ['invalid', '5+6j']})
        result_df = conversion_engine.convert_column_to_complex(df, 'column', errors='coerce')
        expected_dtype = 'complex'
        expected_length = 2
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)

    def test_missing_values_default(self):
        df = pd.DataFrame({'column': [None, '5+6j']})
        result_df = conversion_engine.convert_column_to_complex(df, 'column', missing_values='default', default_value=complex(1, 1))
        expected_dtype = 'complex'
        expected_length = 2
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)

    def test_missing_values_delete(self):
        df = pd.DataFrame({'column': [None, '5+6j']})
        result_df = conversion_engine.convert_column_to_complex(df, 'column', missing_values='delete')
        expected_dtype = 'complex'
        expected_length = 1
        self.assertTrue(result_df['column'].dtype == expected_dtype)
        self.assertTrue(len(result_df['column']) == expected_length)
        
class TestConvertDataTypes(unittest.TestCase):
    """
    Unit tests to test conversion of complete dataframe
    """

    def test_convert_data_types(self):
        data = {
            'int_col': [1, 2, 3],
            'float_col': [1.0, 2.0, 3.0],
            'bool_col': ['TRUE', 'FALSE', 'TRUE'],
            'datetime_col': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'timedelta_col': ['1 days', '2 days', '3 days'],
            'category_col': ['A', 'B', 'C']
        }
        df = pd.DataFrame(data)

        # Define the dtype_mapping
        dtype_mapping = {
            'int_col': DataTypes.INT8,
            'float_col': DataTypes.FLOAT32,
            'bool_col': DataTypes.BOOLEAN,
            'datetime_col': DataTypes.DATETIME64,
            'timedelta_col': DataTypes.TIMEDELTA64,
            'category_col': DataTypes.CATEGORY
        }

        result = conversion_engine.convert_data_types(df, dtype_mapping)

        # Check if the returned DataFrame is correctly converted
        self.assertTrue(str(result['int_col'].dtype) == dtype_mapping['int_col'])
        self.assertTrue(str(result['float_col'].dtype) == dtype_mapping['float_col'])
        self.assertTrue(str(result['bool_col'].dtype) == dtype_mapping['bool_col'])
        self.assertTrue(str(result['datetime_col'].dtype) == dtype_mapping['datetime_col'])
        self.assertTrue(str(result['timedelta_col'].dtype) == dtype_mapping['timedelta_col'])
        self.assertTrue(str(result['category_col'].dtype) == dtype_mapping['category_col'])

if __name__ == '__main__':
    unittest.main()
