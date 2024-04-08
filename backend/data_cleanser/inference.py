import pandas as pd
import numpy as np
import re

from .data_types import DataTypes, get_numeric_types

class Inference:

    MAX_INTEGER_CHECKABLE_FLOAT = 2.0 ** 53 # Max integer value that can be checked appropriately via is_integer()
    INFERENCE_THRESHOLD_PERCENTAGE = 0.5 # Default percentage of valid values in a data column to accurately infer the type

    def __init__(self, inference_threshold_perc):
        self.INFERENCE_THRESHOLD_PERCENTAGE = inference_threshold_perc

    
    def get_non_na_values_percentage(self, data_column):
        """
        Calculates non-na values percentage in a dataframe.

        Args:
        data_column (series): Data column from a pandas dataframe.

        Returns: 
        float: Percentage of non-na values in the series (0.0 - 1.0).
        """

        total_values_count = len(data_column)
        non_na_values_count =  total_values_count - data_column.isna().sum()
        return non_na_values_count / total_values_count

    
    def infer_formatted_numeric_type(self, data_column):
        """
        Infer numeric type from strings.

        Args:
        - data_column (pd.Series): Data column from a pandas DataFrame.

        Returns:
        - DataTypes.FLOAT64 or DataTypes.INT64 or DataTypes.OBJECT: The inferred numeric type based on the data column.
        """
         
        # Matching for comma ',' or currency symbol '$' separated integers or floats values
        comma_and_decimal_pattern = r'^(\$?\d{1,3}(,\d{3})*(\.\d+)?$)|(\d{1,3}(,\d{3})*(\.\d+)?$)'
        matches = data_column.astype(str).str.match(comma_and_decimal_pattern, na=False).sum()
        
        # If more than the threshold number of the column data is inferred as numeric, return a numeric type i.e. integer or float
        if matches / len(data_column) > self.INFERENCE_THRESHOLD_PERCENTAGE:
            contains_float = any('.' in str(x) for x in data_column)
            return DataTypes.FLOAT64 if contains_float else DataTypes.INT64
        
        # Default if no numeric type could be inferred
        return DataTypes.OBJECT
    

    def is_timedelta_type(self, data_column):
        """
        Check if the data column contains timedelta values.

        Args:
        - data_column (pd.Series): Data column from a pandas DataFrame.

        Returns:
        - bool: True if the data column contains timedelta values, False otherwise.
        """

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
            if data_column.str.contains(pattern).sum() / len(data_column) > self.INFERENCE_THRESHOLD_PERCENTAGE:
                return True
        return False
    

    def is_datetime_type(self, data_column):
        """
        Check if the data column contains datetime values.

        Args:
        - data_column (pd.Series): Data column from a pandas DataFrame.

        Returns:
        - bool: True if the data column contains datetime values, False otherwise.
        """

        try:
            dc_converted = pd.to_datetime(data_column, errors='raise')
            if self.get_non_na_values_percentage(dc_converted) > self.INFERENCE_THRESHOLD_PERCENTAGE:
                return True
            return False
                
        except (ValueError, TypeError):
            return False
        
    
    def is_categorical_type(self, data_column):
        return len(data_column.astype(str).unique()) / len(data_column) < 0.5 # only returning true if unique values are less than 50%


    def infer_numeric_type(self, data_column):
        """
        Infer the numeric type (int64, int32, int16, int8, float64, float32) of the data column. If not numeric, return 'object' as default

        Args:
        - data_column (pd.Series): Data column from a pandas DataFrame.

        Returns:
        - str: The inferred numeric type.
        """

        infered_data_type = DataTypes.OBJECT # Default value if numeric data not inferred
        dc_converted = pd.to_numeric(data_column, errors='coerce') # Data column converted to numeric type using pandas
        
        # Inferring the high level numeric type i.e. Integer or Float
        if pd.api.types.is_integer_dtype(dc_converted):
            infered_data_type = DataTypes.INTEGER
        elif pd.api.types.is_float_dtype(dc_converted):
            infered_data_type = DataTypes.INTEGER # Setting to INTEGER unless a float value is found

            for value in dc_converted:
                if not np.isnan(value):
                    if value > self.MAX_INTEGER_CHECKABLE_FLOAT or not float(value).is_integer():
                        infered_data_type = DataTypes.FLOAT
                        break
        else:
            pass

        if self.get_non_na_values_percentage(dc_converted) > self.INFERENCE_THRESHOLD_PERCENTAGE: # More than threshold percentage of the values are numeric
            if infered_data_type == DataTypes.INTEGER: # Check if converted dataframe is of integer type
                try:
                    col_min = dc_converted.min()
                    col_max = dc_converted.max()

                    if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                        return DataTypes.INT8
                    elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                        return DataTypes.INT16
                    elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                        return DataTypes.INT32
                    else:
                        return DataTypes.INT64
                except (TypeError):
                        # Returning default 'int64' when the min, max are not numeric values
                        return DataTypes.INT64

            else: # Check if converted dataframe is of floating type
                try:
                    col_min = dc_converted.min()
                    col_max = dc_converted.max()

                    if col_max <= np.finfo(np.float32).max:
                        return DataTypes.FLOAT32
                    else:
                        return DataTypes.FLOAT64

                except (TypeError):
                    # Returning default 'float64' when the min, max are not numeric values
                    return DataTypes.FLOAT64
        
        else:
            # Checking for formatted numeric strings
            inferred_formatted_numeric_type = self.infer_formatted_numeric_type(data_column)
            if inferred_formatted_numeric_type == DataTypes.FLOAT64 or inferred_formatted_numeric_type == DataTypes.INT64:
                return inferred_formatted_numeric_type
            
        return DataTypes.OBJECT
    
    
    def is_boolean_type(self, data_column):
        """
        Infer if the data column contains boolean values.

        Args:
        - data_column (pd.Series): Data column from a pandas DataFrame.

        Returns:
        - bool: True if the column contains boolean values, False otherwise.
        """
        boolean_formats = ['1', '0', 'true', 'false', 't', 'f']
        boolean_count = 0
        for val in data_column:
            if str(val).strip().lower() in boolean_formats:
                boolean_count += 1

        return boolean_count / len(data_column) > self.INFERENCE_THRESHOLD_PERCENTAGE
    

    def is_complex_type(self, data_column):
        """
        Infer if the data column contains complex values.

        Args:
        - data_column (pd.Series): Data column from a pandas DataFrame.

        Returns:
        - bool: True if the column contains complex values, False otherwise.
        """
        
        complex_data_formats = [
            r'([-+]?\d*\.?\d+)\s*([-+])\s*(\d*\.?\d+)j', # a + bj
            r'\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)', # (a, b)
            r'([-+]?\d*\.?\d*)\s*([-+])\s*(\d*\.?\d*)\s*\*\s*j', # a +/- bi
            r'\d+\*(cos\(\d+(\.\d+)?\)\+j\*sin\(\d+(\.\d+)?\))', # r*(cos(theta) + j*sin(theta))
            r'\(\s*([-+]?\d*\.?\d+)\s*\+\s*([-+]?\d*\.?\d+)j\s*\)' # (a + bj)
        ]

        complex_values_count = 0
        for value in data_column:
            for format in complex_data_formats:
                if re.compile(format).match(str(value).strip()):
                    complex_values_count += 1
                    break
        
        return complex_values_count / len(data_column) > self.INFERENCE_THRESHOLD_PERCENTAGE


    def infer_data_type(self, data_column):
        """
        Infer the data type of a column based on its content.

        Args:
        - data_column (pd.Series): The column of data to infer the type from.

        Returns:
        - str: One of the following data types:
            - 'object': If the column is empty or the majority of values in the column can't be confidently inferred
            - 'int64', 'int32', 'int16', 'int8', 'float64', 'float32': If the column contains numeric data.
            - 'boolean': If the column contains boolean values.
            - 'timedelta64[ns]': If the column contains timedelta data.
            - 'datetime64[ns]': If the column contains datetime data.
            - 'boolean': If the column contains boolean values.
            - 'category': If the column contains categorical values.
            - 'complex': If the column contains complex numbers.

        Note:
        - This method uses various internal methods (infer_numeric_type, is_boolean_type, is_categorical_type, is_timedelta_type, is_datetime_type, is_boolean_type, is_categorical_type, is_complex_type) to infer the data type based on the content of the column.
        """

        # Return 'object' type if passed dataframe column is empty or majority ( > 50% ) values are NA
        if len(data_column) == 0 or self.get_non_na_values_percentage(data_column) <= self.INFERENCE_THRESHOLD_PERCENTAGE:
            return DataTypes.OBJECT

        # Infer numeric data type
        inferred_data_type = self.infer_numeric_type(data_column)
        if inferred_data_type in get_numeric_types():
            # Check boolean and categorical data in numerical format
            if self.is_boolean_type(data_column):
                return DataTypes.BOOLEAN
            return inferred_data_type

        # Infer timedelta data type
        if self.is_timedelta_type(data_column):
            return DataTypes.TIMEDELTA64

        # Infer datetime data type
        if self.is_datetime_type(data_column):
            return DataTypes.DATETIME64

        # Infer boolean data type
        if self.is_boolean_type(data_column):
            return DataTypes.BOOLEAN

        # Infer categorical data type
        if self.is_categorical_type(data_column):
            return DataTypes.CATEGORY

        # Infer complex data type
        if self.is_complex_type(data_column):
            return DataTypes.COMPLEX

        return DataTypes.OBJECT
    

    def infer_data_types(self, dataframe):
        """
        Infer the data types of all columns in the given dataframe.

        Args:
        - dataframe (pd.DataFrame): The input dataframe.

        Returns:
        - dict: A dictionary mapping column names to inferred data types.
        """
        
        inferred_data_types = dict()
        for col in list(dataframe.columns):
            inferred_data_types[col] = self.infer_data_type(dataframe[col])

        return inferred_data_types