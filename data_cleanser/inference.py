import pandas as pd
import numpy as np

"""
Method to return the data-type of the dataframe column passed, returns Object if not able to determine
"""

def infer_data_type(dataframe, col):
    default_type = 'object'
    
    """
    infering numeric types i.e (int64, int32,int16, int8)
    """ 
    print("Received data type:", dataframe[col].dtype)
    df_converted = pd.to_numeric(dataframe[col], errors='coerce')
    print("Converted data type:", df_converted.dtype)

    total_values_count = len(df_converted)
    numeric_values_count = total_values_count - df_converted.isna().sum()
    
    print("Numeric values count:", numeric_values_count)
    
    if pd.api.types.is_integer_dtype(df_converted):
        if numeric_values_count > total_values_count / 2:  # Major proportion of the values are numeric
            try:
                col_min = dataframe[col].min()
                col_max = dataframe[col].max()

                if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                    return 'int8'
                elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                    return 'int16'
                elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                    return 'int32'
                else:
                    return 'int64'
            except (TypeError):
                # handling when the min, max are not numeric values
                return 'int64'
            
    elif pd.api.types.is_float_dtype(df_converted):
        if numeric_values_count > total_values_count / 2:  # Major proportion of the values are numeric
            try:
                col_min = dataframe[col].min()
                col_max = dataframe[col].max()

                if col_max <= np.finfo(np.float32).max:
                    return 'float32'
                else:
                    return 'float64'
            
            except (TypeError):
                # handling when the min, max are not numeric values
                return 'float64'
    
    else: # Major proportion are not numeric
        pass

    
    return default_type

"""
Method to return the data-types of all of the columns in the dataframe passed
"""    
def infer_data_types(dataframe):
    return