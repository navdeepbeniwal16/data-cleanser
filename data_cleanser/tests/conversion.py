import pandas as pd
import numpy as np
import pytest
from data_cleanser import conversion as conversion_engine
from data_cleanser.inference import InferedDataType


import pytest
import numpy as np
import pandas as pd

"""
Testing conversion to datetime data type
"""

def test_convert_column_to_datetime_existing_column():
    # Test converting an existing object type column to datetime
    df = pd.DataFrame({'dates_valid': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']})
    column_name = 'dates_valid'
    assert df[column_name].dtype == 'object'
    result = conversion_engine.convert_column_to_datetime(df, column_name)
    assert str(result[column_name].dtype) == 'datetime64[ns]'

def test_convert_column_to_datetime_non_existing_column():
    # Test converting a non-existing column
    df = pd.DataFrame({'dates_valid': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']})
    with pytest.raises(KeyError):
        conversion_engine.convert_column_to_datetime(df, 'non_existing_column')

def test_convert_column_to_datetime_raise_exception_with_invalid_values():
    # Test converting a column with invalid values
    df = pd.DataFrame({'dates_invalid': ['2022-01-01', 'invalid', '2022-03-01', '2022-04-01']})
    column_name = 'dates_invalid'
    with pytest.raises(ValueError):
        conversion_engine.convert_column_to_datetime(df, column_name)

def test_convert_column_to_datetime_coerce_errors_with_invalid_values():
    # Test converting a column with invalid values and 'coerce' errors
    df = pd.DataFrame({'dates_invalid': ['2022-01-01', 'invalid', '2022-03-01', '2022-04-01']})
    column_name = 'dates_invalid'
    result = conversion_engine.convert_column_to_datetime(df, column_name, errors='coerce')
    assert pd.isna(result[column_name]).sum() == 1

def test_convert_column_to_datetime_no_changes_in_original_df():
    # Test that the original DataFrame is not modified
    df = pd.DataFrame({'dates_valid': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']})
    column_name = 'dates_valid'
    conversion_engine.convert_column_to_datetime(df, column_name)
    assert 'dates_valid' in df.columns  # Check that the column still exists in the original DataFrame

def test_convert_column_to_datetime_missing_values_ignore():
    # Test converting a column with missing values and 'ignore' missing_values option
    column_name = 'dates_missing'
    df = pd.DataFrame({'dates_missing': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', np.nan ]})
    result = conversion_engine.convert_column_to_datetime(df, column_name, missing_values='ignore')
    assert pd.isna(result[column_name]).sum() == 1  # One missing value should remain as NaN

def test_convert_column_to_datetime_missing_values_default():
    # Test converting a column with missing values and 'default' missing_values option
    column_name = 'dates_missing'
    df = pd.DataFrame({'dates_missing': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', np.nan ]})
    default_value = pd.Timestamp.now()
    result = conversion_engine.convert_column_to_datetime(df, column_name, missing_values='default', default_value=default_value)
    assert result[column_name].dtype == 'datetime64[ns]'
    assert pd.isna(result[column_name]).sum() == 0  # Missing value should be replaced with default_value

def test_convert_column_to_datetime_missing_values_delete():
    # Test converting a column with missing values and 'delete' missing_values option
    column_name = 'dates_missing'
    df = pd.DataFrame({'dates_missing': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', np.nan ]})
    result = conversion_engine.convert_column_to_datetime(df, column_name, missing_values='delete')
    assert result[column_name].dtype == 'datetime64[ns]'
    assert pd.isna(result[column_name]).sum() == 0  # Missing value should be deleted


"""
Testing conversion to categorical data type
"""

def test_convert_column_to_category_existing_column():
    # Test converting an existing column to category
    df = pd.DataFrame({'category_column': ['A', 'B', 'C', 'A', 'B', 'C']})
    column_name = 'category_column'
    assert df[column_name].dtype == 'object'
    result = conversion_engine.convert_column_to_category(df, column_name)
    assert result[column_name].dtype == 'category'

def test_convert_column_to_category_non_existing_column():
    # Test converting a non-existing column
    df = pd.DataFrame({'category_column': ['A', 'B', 'C', 'A', 'B', 'C']})
    column_name = 'non_existing_column'
    with pytest.raises(KeyError):
        conversion_engine.convert_column_to_category(df, column_name)

def test_convert_column_to_category_empty_dataframe():
    # Test converting a column in an empty DataFrame
    df = pd.DataFrame()
    column_name = 'category_column'
    with pytest.raises(KeyError):
        conversion_engine.convert_column_to_category(df, column_name)

def test_convert_column_to_category_ignore_missing_values():
    # Test converting a column with missing values and 'ignore' option
    df = pd.DataFrame({'category_column': ['A', 'B', None, 'A', 'B', 'C']})
    column_name = 'category_column'
    result = conversion_engine.convert_column_to_category(df, column_name, missing_values='ignore')
    assert result[column_name].dtype == 'category'

def test_convert_column_to_category_default_missing_values():
    # Test converting a column with missing values and 'default' option
    df = pd.DataFrame({'category_column': ['A', 'B', None, 'A', 'B', 'C']})
    column_name = 'category_column'
    result = conversion_engine.convert_column_to_category(df, column_name, missing_values='default', default_value='default value')
    assert result[column_name].dtype == 'category'
    assert result[column_name].isna().sum() == 0

def test_convert_column_to_category_delete_missing_values():
    # Test converting a column with missing values and 'delete' option
    df = pd.DataFrame({'category_column': ['A', 'B', None, 'A', 'B', 'C']})
    column_name = 'category_column'
    result = conversion_engine.convert_column_to_category(df, column_name, missing_values='delete')
    assert result[column_name].dtype == 'category'
    assert result[column_name].isna().sum() == 0