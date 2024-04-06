from rest_framework import serializers
from .models import DataFile

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ('file', 'uploaded_on')

class DataTypeChangeSerializer(serializers.Serializer):
    dtype_choices = [
        ("object", "Object"),
        ("int64", "Int64"),
        ("int32", "Int32"),
        ("int16", "Int16"),
        ("int8", "Int8"),
        ("float64", "Float64"),
        ("float32", "Float32"),
        ("boolean", "Boolean"),
        ("category", "Category"),
        ("datetime64[ns]", "Datetime64"),
        ("timedelta64[ns]", "Timedelta64"),
        ("complex", "Complex")
    ]

    missing_values_choices = [
        ("ignore", "Ignore"),
        ("default", "Default"),
        ("delete", "Delete")
    ]

    col_name = serializers.CharField(max_length=250)
    dtype = serializers.ChoiceField(choices=dtype_choices)
    missing_values = serializers.ChoiceField(choices=missing_values_choices)
    default = serializers.CharField(max_length=20, allow_null=True)

class DataTypesChangeRequestSerializer(serializers.Serializer):
    invalid_values_choices = [
        ("coerce", "Coerce"),
        ("raise", "Raise")
    ]

    dtypes = DataTypeChangeSerializer(many=True)
    invalid_values = serializers.ChoiceField(choices=invalid_values_choices)
    original_data_key = serializers.CharField(max_length=100)
    cleaned_data_key = serializers.CharField(max_length=100)
