import pandas as pd
import numpy as np
from .inference import InferedDataType
from . import inference as inference_engine

class MISSING_VALUE_OPTIONS:
    IGNORE = 'ignore'
    DEFAULT = 'default'
    DELETE = 'delete'

def dataframe_has_column(df, column):
    # Check if the column exists in the passed in dataframe
    if column not in df:
        raise KeyError(f'Column "{column}" does not exist in the DataFrame')

def convert_column_to_numeric(df, column):
    """
    Convert a column in the DataFrame to a numeric data type.

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - column (str): Column name to convert.

    Returns:
    - pd.DataFrame: DataFrame with specified column converted to numeric data type.
    """
    # Your implementation here
    pass

def convert_column_to_datetime(df, column, errors='raise', missing_values='ignore', default_value=pd.Timestamp.now()):
    """
    Convert a column in the DataFrame to a datetime data type.

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - column (str): Column name to convert.
    - errors (str): To handle errors in conversion. Default is 'raise', but can be set to 'coerce' or 'ignore'.
    - missing_values (str): To handle missing values. Default is 'ignore'.

    Returns:
    - pd.DataFrame: DataFrame with specified column converted to datetime data type.
    """

    dataframe_has_column(df, column)

    # Convert the column to a datetime type
    try:
        df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
        if missing_values == MISSING_VALUE_OPTIONS.IGNORE:
            df_copy[column] = pd.to_datetime(df_copy[column], errors=errors)
        elif missing_values == MISSING_VALUE_OPTIONS.DEFAULT:          
            df_copy[column] = pd.to_datetime(df_copy[column], errors=errors).fillna(default_value)
        elif missing_values == MISSING_VALUE_OPTIONS.DELETE:
            df_copy.dropna(subset=[column], inplace=True)
            df_copy[column] = pd.to_datetime(df_copy[column], errors=errors)
        else:
            raise ValueError('Invalid value for missing_values. Use one of "ignore", "default", or "delete".')
        return df_copy
    except ValueError as e:
        raise ValueError(f'Error converting column "{column}" to {InferedDataType.DATETIME64}: {str(e)}')
    

def convert_column_to_category(df, column, missing_values='ignore', default_value='other'):
    """
    Convert a column in the DataFrame to a categorical data type.

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - column (str): Column name to convert.
    - missing_values (str): How to handle missing values. Default is 'ignore', but can be set to 'coerce' or 'ignore'.
    - default_value (str): Default value to use for missing values. Default is 'other'.

    Returns:
    - pd.DataFrame: DataFrame with specified column converted to categorical data type.
    """
    
    dataframe_has_column(df, column)

    # Convert the column to a categorical type
    try:
        df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
        if missing_values == MISSING_VALUE_OPTIONS.IGNORE:
            df_copy[column] = pd.Categorical(df_copy[column])
        elif missing_values == MISSING_VALUE_OPTIONS.DEFAULT:
            df_copy[column] = pd.Categorical(df_copy[column].fillna(default_value))
        elif missing_values == MISSING_VALUE_OPTIONS.DELETE:
            df_copy.dropna(subset=[column], inplace=True)
            df_copy[column] = pd.Categorical(df_copy[column])
        return df_copy
    except ValueError as e:
        raise ValueError(f'Error converting column "{column}" to {InferedDataType.CATEGORY}: {str(e)}')

boolean_map = { True: True, False: False, 'True': True, 'TRUE': True, 'true': True, '1': True, 'T': True, 't': True, 'False': False, 'FALSE': False, 'false': False, '0': False, 'F': False, 'f': False }

def map_boolean(value):
    if value in boolean_map:
        return boolean_map[value]
    else:
        raise ValueError(f'Invalid boolean value: {value}')

def convert_column_to_boolean(df, column, errors='raise', missing_values='ignore', default_value=False):
    """
    Convert a column in the DataFrame to a boolean data type

    Args:
    - df (pd.DataFrame): Input DataFrame
    - column (str): Column name to convert
    - errors (str): To handle errors in conversion. Default is 'raise'. Options are 'ignore', 'coerce', 'raise'.
    - missing_values (str): To handle missing values. Default is 'ignore'. Options are 'ignore', 'default', 'delete'.
    - default_value: Default value to use for missing values. Default is False

    Returns:
    - pd.DataFrame: DataFrame with specified column converted to boolean data type
    """

    dataframe_has_column(df, column)

    # Return dataframe if the dataframe column already is of boolean type
    if df[column].dtype == InferedDataType.BOOLEAN:
        return df

    # Convert the column to a boolean type
    try:
        df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original

        # Handle invalid values based on set option for errors
        if errors == 'ignore':
            pass
        elif errors == 'coerce':
            df_copy[column] = df_copy[column].map(boolean_map)
        elif errors == 'raise':
            df_copy[column] = df_copy[column].map(map_boolean)

        # Handle missing values based on set option for missing_values
        if missing_values == MISSING_VALUE_OPTIONS.IGNORE:
            pass
        elif missing_values == MISSING_VALUE_OPTIONS.DEFAULT:
            df_copy[column] = df_copy[column].fillna(default_value).map(map_boolean)
        elif missing_values == MISSING_VALUE_OPTIONS.DELETE:
            df_copy = df_copy.dropna(subset=[column])
            df_copy[column] = df_copy[column].map(map_boolean)
        
        return df_copy
    except ValueError as e:
        raise ValueError(f'Error converting column "{column}" to {InferedDataType.BOOLEAN}: {str(e)}')



def convert_data_types(df, dtype_mapping):
    """
    Convert specified columns in the DataFrame to the specified data types.

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - dtype_mapping (dict): Dictionary mapping columns to desired data types.

    Returns:
    - pd.DataFrame: DataFrame with specified columns converted to specified data types.
    """
    # Your implementation here
    pass

def infer_and_convert_data_types(df):
    """
    Infer and convert data types of columns in the DataFrame.

    Args:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    - pd.DataFrame: DataFrame with columns converted to inferred data types.
    """
    # Your implementation here
    pass
