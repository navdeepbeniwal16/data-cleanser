import pandas as pd
import numpy as np
import re

MAX_INTEGER_CHECKABLE_FLOAT = 2.0 ** 53 # Max integer value that can be checked appropriately via is_integer()
INFERENCE_THRESHOLD_PERCENTAGE = 0.5 # Threshold percentage of valid values in a data column to accurately infer the type

"""
Method to return the data-type of the dataframe column passed, returns Object if not able to determine
"""
class InferedDataType:
    OBJECT = 'object'
    INTEGER = 'int64'
    INT64 = 'int64'
    INT32 = 'int32'
    INT16 = 'int16'
    INT8 = 'int8'
    FLOAT = 'float64'
    FLOAT64 = 'float64'
    FLOAT32 = 'float32'
    DATETIME64 = 'datetime64[ns]'
    TIMEDELTA64 = 'timedelta64[ns]'
    BOOLEAN = 'bool'
    CATEGORY = 'category'
    COMPLEX = 'complex'

"""
Calculates non-na values percentage in a dataframe

Args:
data_column (series): Data column from a pandas dataframe

Returns: 
float: Percentage of non-na values in the series (0.0 - 1.0)
"""
def get_non_na_values_percentage(data_column):
    total_values_count = len(data_column)
    non_na_values_count =  total_values_count - data_column.isna().sum()
    return non_na_values_count / total_values_count

"""
Infer numeric type from strings

Args:
data_column (series): Data column from a pandas dataframe

Returns:
InferedDataType.FLOAT64 or InferedDataType.INT64 or InferedDataType.OBJECT
"""
def infer_formatted_numeric_type(data_column):
    # Matching for comma ',' or currency symbol '$' separated integers or floats values
    comma_and_decimal_pattern = r'^(\$?\d{1,3}(,\d{3})*(\.\d+)?$)|(\d{1,3}(,\d{3})*(\.\d+)?$)'
    matches = data_column.astype(str).str.match(comma_and_decimal_pattern, na=False).sum()
    
    # If more than the threshold number of the column data is inferred as numeric, return a numeric type i.e. integer or float
    if matches / len(data_column) > INFERENCE_THRESHOLD_PERCENTAGE:
        contains_float = any('.' in str(x) for x in data_column)
        return InferedDataType.FLOAT64 if contains_float else InferedDataType.INT64
    
    # Default if no numeric type could be inferred
    return InferedDataType.OBJECT

def is_timedelta_type(data_column):
    timedelta_patterns = [
        r'^\d{1,2}:\d{2}:\d{2}$',                    # HH:MM:SS
        r'^\d{1,2}:\d{2}:\d{2}\.\d{1,3}$',           # HH:MM:SS.SSS
        r'^\d{1,2}:\d{2}:\d{2},\d{1,3}$',            # HH:MM:SS,SSS
        r'^\d+ days \d{1,2}:\d{2}:\d{2}$',           # DD days HH:MM:SS
        r'^\d+ days \d{1,2}:\d{2}:\d{2}\.\d{1,3}$',  # DD days HH:MM:SS.SSS
        r'^\d+:\d{2}:\d{2}:\d{2}$',                  # DD:HH:MM:SS
        r'^\d+:\d{2}:\d{2}:\d{2}\.\d{1,3}$',         # DD:HH:MM:SS.SSS
        r'^\d+:\d{2}:\d{2}:\d{2},\d{1,3}$',          # DD:HH:MM:SS,SSS
    ]

    for pattern in timedelta_patterns:
        if data_column.str.contains(pattern).sum() / len(data_column) > INFERENCE_THRESHOLD_PERCENTAGE:
            return True
    return False

def is_datetime_type(data_column):
    try:
        dc_converted = pd.to_datetime(data_column, errors='raise')
        if get_non_na_values_percentage(dc_converted) > INFERENCE_THRESHOLD_PERCENTAGE:
            return True
        return False
            
    except (ValueError, TypeError):
        return False

"""
Function to infer numeric types i.e (int64, int32,int16, int8, float64, float32)
"""
def infer_numeric_type(data_column):
    infered_data_type = InferedDataType.OBJECT # Default value if numeric data not inferred
    dc_converted = pd.to_numeric(data_column, errors='coerce') # Data column converted to numeric type using pandas
    
    # Inferring the high level numeric type i.e. Integer or Float
    if pd.api.types.is_integer_dtype(dc_converted):
        infered_data_type = InferedDataType.INTEGER
    elif pd.api.types.is_float_dtype(dc_converted):
        infered_data_type = InferedDataType.INTEGER # Setting to INTEGER unless a float value is found

        for value in dc_converted:
            if not np.isnan(value):
                if value > MAX_INTEGER_CHECKABLE_FLOAT or not float(value).is_integer():
                    infered_data_type = InferedDataType.FLOAT
                    break
    else:
        pass

    if get_non_na_values_percentage(dc_converted) > INFERENCE_THRESHOLD_PERCENTAGE: # More than threshold percentage of the values are numeric
        if infered_data_type == InferedDataType.INTEGER: # Check if converted dataframe is of integer type
            try:
                col_min = dc_converted.min()
                col_max = dc_converted.max()

                if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                    return InferedDataType.INT8
                elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                    return InferedDataType.INT16
                elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                    return InferedDataType.INT32
                else:
                    return InferedDataType.INT64
            except (TypeError):
                    # Returning default 'int64' when the min, max are not numeric values
                    return InferedDataType.INT64

        else: # Check if converted dataframe is of floating type
            try:
                col_min = dc_converted.min()
                col_max = dc_converted.max()

                if col_max <= np.finfo(np.float32).max:
                    return InferedDataType.FLOAT32
                else:
                    return InferedDataType.FLOAT64

            except (TypeError):
                # Returning default 'float64' when the min, max are not numeric values
                return InferedDataType.FLOAT64
    
    else:
        # Checking for formatted numeric strings
        inferred_formatted_numeric_type = infer_formatted_numeric_type(data_column)
        if inferred_formatted_numeric_type == InferedDataType.FLOAT64 or inferred_formatted_numeric_type == InferedDataType.INT64:
            return inferred_formatted_numeric_type
        
    return InferedDataType.OBJECT
    
def is_boolean_type(data_column):
    boolean_formats = ['1', '0', 'true', 'false', 't', 'f']
    boolean_count = 0
    for val in data_column:
        if str(val).strip().lower() in boolean_formats:
            boolean_count += 1

    return boolean_count / len(data_column) > INFERENCE_THRESHOLD_PERCENTAGE

def is_categorical_type(data_column):
    return len(data_column.unique()) / len(data_column) < 0.5

def is_complex_type(data_column):
    complex_data_formats = [
        r'([-+]?\d*\.?\d+)\s*([-+])\s*(\d*\.?\d+)j',
        r'\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)',
        r'([-+]?\d*\.?\d*)\s*([-+])\s*(\d*\.?\d*)\s*\*\s*j',
        r'\d+\*(cos\(\d+(\.\d+)?\)\+j\*sin\(\d+(\.\d+)?\))',
        r'\(\s*([-+]?\d*\.?\d+)\s*\+\s*([-+]?\d*\.?\d+)j\s*\)'
    ]

    complex_values_count = 0
    for value in data_column:
        for format in complex_data_formats:
            if re.compile(format).match(str(value).strip()):
                complex_values_count += 1
                break
    
    return complex_values_count / len(data_column) > INFERENCE_THRESHOLD_PERCENTAGE


def infer_data_type(data_column):
    # Returning 'object' type if passed dataframe column in empty or more than a threshold values are na
    if len(data_column) == 0 or get_non_na_values_percentage(data_column) <= INFERENCE_THRESHOLD_PERCENTAGE:
        return InferedDataType.OBJECT

    # Inferring numeric data type
    inferred_data_type = infer_numeric_type(data_column)
    if inferred_data_type in [InferedDataType.FLOAT32, InferedDataType.FLOAT64, InferedDataType.INT8, InferedDataType.INT16, InferedDataType.INT32, InferedDataType.INT64]:
        # Checking for boolean (0, 1) numerics
        if is_boolean_type(data_column):
            return InferedDataType.BOOLEAN
        
        return inferred_data_type
    
    # Inferring timedelta[na] data type 
    if is_timedelta_type(data_column):
            return InferedDataType.TIMEDELTA64
    
    # Inferring datetime data type
    if is_datetime_type(data_column):
        return InferedDataType.DATETIME64

    # Inferring boolean data type
    if is_boolean_type(data_column):
        return InferedDataType.BOOLEAN
    
    # Inferring categorical data
    if is_categorical_type(data_column): 
            return InferedDataType.CATEGORY

    # Inferring complex data
    if is_complex_type(data_column):
        return InferedDataType.COMPLEX

    return InferedDataType.OBJECT

"""
Method to return the data-types of all of the columns in the dataframe passed
"""    
def infer_data_types(dataframe):
    inferred_data_types = dict()
    for col in list(dataframe.columns):
        inferred_data_types[col] = infer_data_type(dataframe[col])

    print("Inferred data types")
    return inferred_data_types