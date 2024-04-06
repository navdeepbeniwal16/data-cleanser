class DataTypes:
    """
    Constants representing different data types.
    """
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

def get_numeric_types():
    """
    Gets a list of numeric data types

    Returns:
    - list: List of numeric data types
    """
    return [
        DataTypes.INT8,
        DataTypes.INT16,
        DataTypes.INT32,
        DataTypes.INT64,
        DataTypes.FLOAT32,
        DataTypes.FLOAT64,
    ]