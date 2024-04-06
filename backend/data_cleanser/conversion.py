import pandas as pd
import numpy as np
import re
from .data_types import DataTypes, get_numeric_types

class _ERROR_HANDLING_OPTIONS:
    IGNORE = 'ignore'
    COERCE = 'coerce'
    RAISE = 'raise'    
class _MISSING_VALUE_OPTIONS:
    IGNORE = 'ignore'
    DEFAULT = 'default'
    DELETE = 'delete'

class Convertor:

    _boolean_map = { True: True, False: False, 'True': True, 'TRUE': True, 'true': True, '1': True, 'T': True, 't': True, 'False': False, 'FALSE': False, 'false': False, '0': False, 'F': False, 'f': False }

    def __init__(self):
        pass

    
    """  Private helper functions to support conversion apis """
    
    def _dataframe_has_column(self, df, column):
        """
        (Private) Check if a column exists in a DataFrame.

        Args:
        - df (pd.DataFrame): The DataFrame to check.
        - column (str): The column name to check for.

        Raises:
        - KeyError: If the column does not exist in the DataFrame.
        """

        if column not in df:
            raise KeyError(f'Column "{column}" does not exist in the DataFrame')
        
    
    def _is_valid_data_type(self, type):
        """
        (Private) Check if a provided data type is valid.

        Args:
        - type (str): The data type to check.

        Raises:
        - KeyError: If the data type is not valid.
        """

        type_options = DataTypes.__dict__.values()
        if type not in type_options:
            raise KeyError(f'Invalid data type provided i.e. {type}. Please provide one of {type_options}')


    def _is_valid_error_handling_option(self, option):
        """
        (Private) Check if the provided error handling option is valid.

        Args:
        - option (str): The error handling option to check.

        Raises:
        - KeyError: If the option is not valid.
        """

        error_options = [_ERROR_HANDLING_OPTIONS.IGNORE, _ERROR_HANDLING_OPTIONS.RAISE, _ERROR_HANDLING_OPTIONS.COERCE]
        if option not in error_options:
            raise KeyError(f'Invalid argument \'{option}\' for \'errors\'. Please provide one of {error_options}')
    

    def _is_valid_missing_value_option(self, option):
        """
        (Private) Check if the provided missing value option is valid.

        Args:
        - option (str): The missing value option to check.

        Raises:
        - KeyError: If the option is not valid.
        """
        
        missing_value_options = [_MISSING_VALUE_OPTIONS.IGNORE, _MISSING_VALUE_OPTIONS.DEFAULT, _MISSING_VALUE_OPTIONS.DELETE]
        if option not in missing_value_options:
            raise KeyError(f'Invalid argument for \'missing_values\'. Please provide one of {missing_value_options}')


    def _map_boolean(self, value):
        """
        (Private) Map a boolean string value to its boolean equivalent based on the boolean map.

        Args:
        - value: The value to map.

        Returns:
        - bool: The boolean equivalent of the boolean string.

        Raises:
        - ValueError: If the value cannot be mapped to a boolean.
        """

        if value in self._boolean_map:
            return self._boolean_map[value]
        else:
            raise ValueError(f'Invalid boolean value: {value}')
        

    def _parse_formatted_numeric_string(self, numeric_string):
        """
        (Private) Parse a string with various numeric formats to a float.

        Args:
        - numeric_string (str): String containing various numeric formats.

        Returns:
        - float: Float value parsed from the string.
        """
        # Handle percentage values
        if re.match(r'^\d{1,3}(,\d{3})*$', numeric_string):
            return pd.to_numeric(numeric_string.replace(',', ''))

        # Handle currency values
        elif re.match(r'^\$?\d{1,3}(,\d{3})*(,\d{2})?$', numeric_string):
            return pd.to_numeric(numeric_string.replace('$', '').replace(',', ''))

        # Handle decimal values
        elif re.match(r'^\d{1,3}(,\d{3})*\.\d+$', numeric_string):
            return pd.to_numeric(numeric_string.replace(',', ''))

        # Handle decimal values with currency symbol
        elif re.match(r'^\$?\d{1,3}(,\d{3})*\.\d+$', numeric_string):
            return pd.to_numeric(numeric_string.replace('$', '').replace(',', ''))

        # Handle percentage values
        elif re.match(r'^-?\d+(\.\d+)?%$', numeric_string):
            return float(numeric_string[:-1]) / 100

        # Handle exponential notation
        elif re.match(r'^-?\d+(\.\d+)?[eE][+-]?\d+$', numeric_string):
            return float(numeric_string)

        # Handle scientific notation
        elif re.match(r'^-?\d+(\.\d+)?[eE]\d+$', numeric_string):
            return float(numeric_string)

        # Handle 'exponential' edge case format
        elif re.match(r'^-?\d+(\.\d+)? x 10\^\d+$', numeric_string):
            parts = numeric_string.split(' x ')
            base, exponent = parts[0], parts[1].replace('^', '')
            return float(base) * 10**float(exponent)

        else:
            raise ValueError(f"Invalid format: '{numeric_string}' is not a formatted numeric string")


    """ Public apis to support conversion """

    def convert_column_to_numeric(self, df, column, numeric_type='float64', errors='raise', missing_values='ignore', default_value=None):
        """
        Convert a column in the DataFrame to a numeric data type.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - column (str): Column name to convert.
        - numeric_type (str): Numeric data type to convert the column to. Options are 'int8', 'int16', 'int32', 'int64', 'float32', 'float64'. Default is 'float64'.
        - errors (str): How to handle errors in conversion. Options are 'coerce' and 'raise'. Default is 'raise'.
        - missing_values (str): How to handle missing values. Options are 'ignore', 'default', 'delete'. Default is 'ignore'.
        - default_value: Default value to use for missing values. Default is None.

        Returns:
        - pd.DataFrame: DataFrame with specified column converted to numeric data type.

        Raises:
        - KeyError: If the numeric_type is not a valid option.
        - KeyError: If the errors option is not 'coerce' or 'raise'.
        - KeyError: If the missing_values option is not 'ignore', 'default', or 'delete'.
        - KeyError: If the specified column does not exist in the DataFrame.
        - ValueError: If there is an error converting the column to the specified numeric type.
        """

        # Check if the numeric type passed is valid or supported
        supported_numeric_types = get_numeric_types()
        if numeric_type not in supported_numeric_types:
            raise KeyError(f'Numeric type "{numeric_type}" is not valid. Please provider one of "{[nt for nt in supported_numeric_types]}"')

        # Handling invalid errors and missing_values arguments
        error_options = [_ERROR_HANDLING_OPTIONS.RAISE, _ERROR_HANDLING_OPTIONS.COERCE]
        if errors not in error_options:
            raise KeyError(f'Invalid argument for \'errors\'. Please provide one of {error_options}')
        self._is_valid_missing_value_option(missing_values)

        self._dataframe_has_column(df, column)

        # Convert the column to a numeric type
        try:
            df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original

            # Pass the errors option directly to pandas to_numeric method - same arguments are supported by to_numeric
            df_copy[column] = pd.to_numeric(df_copy[column], errors=errors)

            # Handle missing values based on set option for missing_values
            if missing_values == _MISSING_VALUE_OPTIONS.IGNORE:
                pass
            elif missing_values == _MISSING_VALUE_OPTIONS.DEFAULT:
                df_copy[column] = df_copy[column].fillna(default_value)
            elif missing_values == _MISSING_VALUE_OPTIONS.DELETE:
                df_copy = df_copy.dropna(subset=[column])
            
            # casting it to the passed in numeric type
            df_copy[column] = df_copy[column].astype(numeric_type) 
            
            return df_copy
        except ValueError as e:
            # Check for formatted numeric type
            try:
                df_copy[column] = df_copy[column].map(str).map(self._parse_formatted_numeric_string)
                df_copy[column] = df_copy[column].astype(numeric_type)
                return df_copy
            except ValueError:
                raise ValueError(f'Error converting column "{column}" to {numeric_type}: {str(e)}')


    def convert_column_to_datetime(self, df, column, errors='raise', missing_values='ignore', default_value=pd.Timestamp.now()):
        """
        Convert a column in the DataFrame to a datetime data type.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - column (str): Column name to convert.
        - errors (str): How to handle errors in conversion. Options are 'coerce', 'raise', or 'ignore'. Default is 'raise'.
        - missing_values (str): How to handle missing values. Options are 'ignore', 'default', or 'delete'. Default is 'ignore'.
        - default_value: Default value to use for missing values. Default is the current timestamp.

        Returns:
        - pd.DataFrame: DataFrame with specified column converted to datetime data type.

        Raises:
        - KeyError: If the errors option is not 'coerce', 'raise', or 'ignore'.
        - KeyError: If the missing_values option is not 'ignore', 'default', or 'delete'.
        - KeyError: If the specified column does not exist in the DataFrame.
        - ValueError: If there is an error converting the column to the datetime type.
        """

        # Handling invalid errors and missing_values arguments
        self._is_valid_error_handling_option(errors)
        self._is_valid_missing_value_option(missing_values)

        self._dataframe_has_column(df, column)

        # Convert the column to a datetime type
        try:
            df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
            if missing_values == _MISSING_VALUE_OPTIONS.IGNORE:
                df_copy[column] = pd.to_datetime(df_copy[column], errors=errors)
            elif missing_values == _MISSING_VALUE_OPTIONS.DEFAULT:          
                df_copy[column] = pd.to_datetime(df_copy[column], errors=errors).fillna(default_value)
            elif missing_values == _MISSING_VALUE_OPTIONS.DELETE:
                df_copy.dropna(subset=[column], inplace=True)
                df_copy[column] = pd.to_datetime(df_copy[column], errors=errors)
            else:
                raise ValueError('Invalid value for missing_values. Use one of "ignore", "default", or "delete".')
            return df_copy
        except ValueError as e:
            raise ValueError(f'Error converting column "{column}" to {DataTypes.DATETIME64}: {str(e)}')
    

    def convert_column_to_category(self, df, column, missing_values='ignore', default_value='other'):
        """
        Convert a column in the DataFrame to a categorical data type.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - column (str): Column name to convert.
        - missing_values (str): How to handle missing values. Options are 'ignore', 'default', or 'delete'. Default is 'ignore'.
        - default_value (str): Default value to use for missing values. Default is 'other'.

        Returns:
        - pd.DataFrame: DataFrame with specified column converted to categorical data type.

        Raises:
        - KeyError: If the missing_values option is not 'ignore', 'default', or 'delete'.
        - KeyError: If the specified column does not exist in the DataFrame.
        - ValueError: If there is an error converting the column to the categorical type.
        """

        # Handling missing_values arguments
        self._is_valid_missing_value_option(missing_values)
        
        self._dataframe_has_column(df, column)

        # Convert the column to a categorical type
        try:
            df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
            if missing_values == _MISSING_VALUE_OPTIONS.IGNORE:
                df_copy[column] = pd.Categorical(df_copy[column])
            elif missing_values == _MISSING_VALUE_OPTIONS.DEFAULT:
                df_copy[column] = pd.Categorical(df_copy[column].fillna(default_value))
            elif missing_values == _MISSING_VALUE_OPTIONS.DELETE:
                df_copy.dropna(subset=[column], inplace=True)
                df_copy[column] = pd.Categorical(df_copy[column])
            return df_copy
        except ValueError as e:
            raise ValueError(f'Error converting column "{column}" to {DataTypes.CATEGORY}: {str(e)}')


    def convert_column_to_boolean(self, df, column, errors='raise', missing_values='ignore', default_value=False):
        """
        Convert a column in the DataFrame to a boolean data type.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - column (str): Column name to convert.
        - errors (str): How to handle errors in conversion. Options are 'raise', 'coerce', 'ignore'. Default is 'raise'.
        - missing_values (str): How to handle missing values. Options are 'ignore', 'default', 'delete'. Default is 'ignore'.
        - default_value: Default value to use for missing values. Default is False.

        Returns:
        - pd.DataFrame: DataFrame with specified column converted to boolean data type.

        Raises:
        - KeyError: If the errors option is not 'raise', 'coerce', or 'ignore'.
        - KeyError: If the missing_values option is not 'ignore', 'default', or 'delete'.
        - KeyError: If the specified column does not exist in the DataFrame.
        - ValueError: If there is an error converting the column to the boolean type.
        """

        # Handling invalid errors and missing_values arguments
        self._is_valid_error_handling_option(errors)
        self._is_valid_missing_value_option(missing_values)

        self._dataframe_has_column(df, column)

        # Return dataframe if the dataframe column already is of boolean type
        if df[column].dtype == DataTypes.BOOLEAN:
            return df

        # Convert the column to a boolean type
        try:
            df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original

            # Handle invalid values based on set option for errors
            if errors == 'ignore':
                pass
            elif errors == 'coerce':
                df_copy[column] = df_copy[column].map(self._boolean_map)
            elif errors == 'raise':
                df_copy[column] = df_copy[column].map(self._map_boolean)

            # Handle missing values based on set option for missing_values
            if missing_values == _MISSING_VALUE_OPTIONS.IGNORE:
                pass
            elif missing_values == _MISSING_VALUE_OPTIONS.DEFAULT:
                df_copy[column] = df_copy[column].fillna(default_value).map(self._map_boolean)
            elif missing_values == _MISSING_VALUE_OPTIONS.DELETE:
                df_copy = df_copy.dropna(subset=[column])
                df_copy[column] = df_copy[column].map(self._map_boolean)
            
            return df_copy
        except ValueError as e:
            raise ValueError(f'Error converting column "{column}" to {DataTypes.BOOLEAN}: {str(e)}')
        

    def _parse_pandas_unsupported_timedelta_format(self, timedelta_string):
        """
        Parse timedelta strings in pandas unsupported format to Timedelta object

        Args:
        - timedelta_string (str): String representing timedelta in unsupported format

        Returns:
        - pd.Timedelta: Timedelta object parsed from the input string

        Raises:
        - ValueError: If the input string does not match any of the supported timedelta formats
        """
        
        # Handling dd_hh_mm_ss (eg '5:01:02:03')
        if re.match(r'^(\d+):(\d{2}):(\d{2}):(\d{2})$', timedelta_string):
            parts = timedelta_string.split(':')
            days, hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            return pd.Timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

        # Handling dd_hh_mm_ss_sss: (eg '5:01:02:03.456')
        elif re.match(r'^(\d+):\d{2}:\d{2}:\d{2}\.\d{3}$', timedelta_string):
            parts = timedelta_string.split(':')
            days, hours, minutes, seconds, milliseconds = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3].split('.')[0]), int(parts[3].split('.')[1])
            return pd.Timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

        # Handling dd_hh_mm_ss_comma_sss: (eg '5:01:02:03,456')
        elif re.match(r'^\d+:\d{2}:\d{2}:\d{2},\d{3}$', timedelta_string):
            parts = timedelta_string.split(':')
            days, hours, minutes, seconds, milliseconds = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3].split(',')[0]), int(parts[3].split(',')[1])
            return pd.Timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

        # Handling hh_mm: (eg '5:01')
        elif re.match(r'^\d+:\d{2}$', timedelta_string):
            parts = timedelta_string.split(':')
            hours, minutes, seconds = int(parts[0]), int(parts[1]), 0 
            return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)

        # Handling HH:MM AM/PM (eg '12:34 PM')
        elif re.match(r'^(\d{1,2}):(\d{2}) (AM|PM)$', timedelta_string):
            parts = re.match(r'^(\d{1,2}):(\d{2}) (AM|PM)$', timedelta_string).groups()
            hours = int(parts[0])
            if parts[2] == 'PM' and hours != 12:
                hours += 12
            elif parts[2] == 'AM' and hours == 12:
                hours = 0
            return pd.Timedelta(hours=hours, minutes=int(parts[1]))

        else:
            raise ValueError(f"Invalid timedelta format: {timedelta_string}")
    

    def convert_column_to_timedelta(self, df, column, errors='raise', missing_values='ignore', default_value=pd.Timedelta(0)):
        """
        Convert a column in the DataFrame to a timedelta data type.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - column (str): Column name to convert.
        - errors (str): How to handle errors in conversion. Default is 'raise'. Options are 'ignore', 'coerce', 'raise'.
        - missing_values (str): How to handle missing values. Default is 'ignore'. Options are 'ignore', 'default', 'delete'.
        - default_value: Default value to use for missing values. Default is pd.Timedelta(0).

        Returns:
        - pd.DataFrame: DataFrame with the specified column converted to timedelta data type.

        Raises:
        - KeyError: If an invalid argument is provided for 'errors'.
        - ValueError: If an invalid value is provided for 'missing_values' or if an error occurs during conversion.
        """
        
        # Handling invalid errors and missing_values arguments
        error_options = [_ERROR_HANDLING_OPTIONS.RAISE, _ERROR_HANDLING_OPTIONS.COERCE]
        if errors not in error_options:
            raise KeyError(f'Invalid argument for \'errors\'. Please provide one of {error_options}')
        self._is_valid_missing_value_option(missing_values)

        self._dataframe_has_column(df, column)

        # Convert the column to a timedelta type
        try:
            df_copy = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
            if missing_values == _MISSING_VALUE_OPTIONS.IGNORE:
                df_copy[column] = pd.to_timedelta(df_copy[column], errors=errors)
            elif missing_values == _MISSING_VALUE_OPTIONS.DEFAULT:          
                df_copy[column] = pd.to_timedelta(df_copy[column], errors=errors).fillna(default_value)
            elif missing_values == _MISSING_VALUE_OPTIONS.DELETE:
                df_copy.dropna(subset=[column], inplace=True)
                df_copy[column] = pd.to_timedelta(df_copy[column], errors=errors)
            else:
                raise ValueError('Invalid value for missing_values. Use one of "ignore", "default", or "delete".')
            
            return df_copy
        except ValueError as e:
            # Check for pandas to_timedelta() unsupported timedelta formats
            try:
                df_copy[column] = df_copy[column].map(str).map(self._parse_pandas_unsupported_timedelta_format)
                return df_copy
            except ValueError:
                raise ValueError(f'Error converting column "{column}" to {DataTypes.TIMEDELTA64}: {str(e)}')
        

    def convert_col_date_type(self, df, column, type_to_cast, errors='coerce', missing_values='ignore', default_value=None):
        """
        Convert a column in a DataFrame to the specified data type.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - column (str): Name of the column to convert.
        - type_to_cast (str): Data type to cast the column to. Should be one of the values from DataTypes.
        - errors (str): How to handle errors during conversion. Default is 'coerce'.
        - missing_values (str): How to handle missing values during conversion. Default is 'ignore'.
        - default_value: Default value to use for missing or erroneous values. Default is None.

        Returns:
        - pd.DataFrame: DataFrame with the specified column converted to the specified data type.

        Raises:
        - KeyError: If an invalid argument is provided for 'type_to_cast', 'errors' and 'missing_values'.
        - ValueError: If an invalid value is provided for 'missing_values' or if an error occurs during conversion.
        """
        
        if type_to_cast == DataTypes.OBJECT:
            pass
        if type_to_cast in get_numeric_types():
            df = self.convert_column_to_numeric(df, column, type_to_cast, errors, missing_values, default_value)
        elif type_to_cast == DataTypes.BOOLEAN:
            df = self.convert_column_to_boolean(df, column, errors, missing_values, default_value)
        elif type_to_cast == DataTypes.DATETIME64:
            df = self.convert_column_to_datetime(df, column, errors, missing_values, default_value)
        elif type_to_cast == DataTypes.TIMEDELTA64:
            df = self.convert_column_to_timedelta(df, column, errors, missing_values, default_value)
        elif type_to_cast == DataTypes.CATEGORY:
            df = self.convert_column_to_category(df, column, missing_values, default_value)
        else:
            pass

        return df


    def convert_data_types(self, df, dtype_mapping, errors='coerce', missing_values='ignore', default_value=None):
        """
        Convert specified columns in the DataFrame to the specified data types.

        Args:
        - df (pd.DataFrame): Input DataFrame.
        - dtype_mapping (dict): Dictionary mapping columns to desired data types.
        - errors (str): How to handle errors during conversion. Default is 'coerce'.
        - missing_values (str): How to handle missing values during conversion. Default is 'ignore'.
        - default_value: Default value to use for missing or erroneous values. Default is None.

        Returns:
        - pd.DataFrame: DataFrame with specified columns converted to specified data types.

        Raises:
        - KeyError: If an invalid argument is provided for 'type_to_cast', 'errors' and 'missing_values'.
        - ValueError: If an error occurs during conversion.
        """

        df_copy = df.copy() # Create a copy of the DataFrame to avoid modifying the original
        
        for col_name in dtype_mapping.keys():
            print("Col name to convert:", col_name)   
            type_to_cast = dtype_mapping[col_name]
            print("Tyoe to cast to:", type_to_cast) 
            df_copy = self.convert_col_date_type(df_copy, col_name, type_to_cast, errors, missing_values, default_value)
        
        return df_copy