import logging
from django.shortcuts import render
from django.views.generic import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import DataFileSerializer, DataTypesChangeRequestSerializer
import pandas as pd
from pandas.errors import ParserError
import os
import pickle
import redis

import sys
sys.path.append('../') 
from data_cleanser.inference import Inference
from data_cleanser.conversion import Convertor

# Initialising logger, cache, inference (for type inference) and convertor (for type/data conversion) instance
logger = logging.getLogger("django")
cache = redis.Redis()
inference_engine = Inference(0.5)
conversion_engine = Convertor()

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# Create your views here.
@api_view(['GET'])
def hello_data_cleanser(request):
    return Response({"message": "Hello! Welcome to data cleanser."})

class DataFileUploadAPIView(APIView):
    """
    API view for uploading data files.

    Handles the uploading of data files (e.g., CSV, Excel) and processes
    them for further analysis or manipulation. It uses the `MultiPartParser` and
    `FormParser` to parse the incoming request data and serializes the data using the `DataFileSerializer`.
    """
    
    parser_classes = (MultiPartParser, FormParser) # for parsing request data
    serializer_class = DataFileSerializer

    def post(self, request):
    
        logger.debug('DataFileUploadAPIView: Starting POST method')
        
        file_data_serializer = self.serializer_class(data=request.data)
        
        if file_data_serializer.is_valid():
            # Access the uploaded file
            uploaded_file = file_data_serializer.validated_data["file"]
            file_name = uploaded_file.name
            file_extension = os.path.splitext(file_name)[1]

            logger.debug(f'DataFileUploadAPIView: Processing file "{file_name}" with extension "{file_extension}"')

            df = pd.DataFrame() # Define an empty dataframe to be replaced with parsed one

            if file_extension == '.csv':
                try:
                    df = pd.read_csv(uploaded_file)
                    logger.debug('DataFileUploadAPIView: Successfully parsed CSV file')
                except ParserError as e:
                    logger.error(f"DataFileUploadAPIView: Error occurred while parsing CSV file: {file_name}, error: {str(e)}")
                    return Response({"message": f"Error occurred while parsing file: {file_name}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            elif file_extension in ['.xls', '.xlsx', '.xlsm', '.xlsb']:
                try:
                    df = pd.read_excel(uploaded_file)
                    logger.debug('DataFileUploadAPIView: Successfully parsed Excel file')
                except ParserError as e:
                    logger.error(f"DataFileUploadAPIView: Error occurred while parsing Excel file: {file_name}, error: {str(e)}")
                    return Response({"message": f"Error occurred while parsing file: {file_name}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            else:
                logger.error(f"DataFileUploadAPIView: Unsupported file type: {file_extension}")
                return Response({"message": "Received unsupported data file type"}, status=status.HTTP_400_BAD_REQUEST )
            
            try:
                df_cleaning_result = self.clean_dataframe(df)
                logger.debug('DataFileUploadAPIView: Dataframe cleaned successfully')
            except ValueError as e:
                logger.error(f"DataFileUploadAPIView: Error cleaning dataframe: {str(e)}")
                return Response({ "message" : "Error cleaning dataframe", "error" : str(e) }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"DataFileUploadAPIView: Unexpected error cleaning dataframe: {str(e)}")
                return Response({ "message" : "Error cleaning dataframe", "error" : str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            df_cleaned = df_cleaning_result["data"]
            
            df_original_bytes = pickle.dumps(df)
            df_cleaned_bytes = pickle.dumps(df_cleaned)

            # Setting original and cleaned dataframe in cache
            original_df_key = 'df_' + os.path.splitext(file_name)[0] + '_original'
            cleaned_df_key = 'df_' + os.path.splitext(file_name)[0] + '_cleaned'
            cache.set(original_df_key, df_original_bytes)
            cache.set(cleaned_df_key, df_cleaned_bytes)
            logger.debug('DataFileUploadAPIView: Dataframes cached successfully')

            for col_name in df_cleaned:
                if df_cleaned[col_name].dtype == 'complex':
                    df_cleaned[col_name] = df_cleaned[col_name].astype(str)
            
            # Instantiate paginator for supporting paginated data
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(df_cleaned.to_dict(orient='records'), request)
            logger.debug('DataFileUploadAPIView: Data paginated successfully')
            
            return Response(
                {
                    "message": "Data uploaded and processed successfully", 
                    "dtypes": df_cleaning_result["dtypes"], 
                    "data": paginated_data, 
                    "original_data_key" : original_df_key,
                    "cleaned_data_key" : cleaned_df_key
                },  status=status.HTTP_200_OK)
        else:
            logger.error(f"DataFileUploadAPIView: Invalid file data serializer: {file_data_serializer.errors}")
            return Response(file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def clean_dataframe(self, df):
        logger.debug("DataFileUploadAPIView : clean_dataframe : Data types received for cleaning")
        logger.debug(df.dtypes)

        # Inferring data types of received data
        logger.debug("DataFileUploadAPIView : clean_dataframe : Inferring received data types")
        df_inferred_types = inference_engine.infer_data_types(df)

        logger.debug("DataFileUploadAPIView : clean_dataframe : Inferred types")
        logger.debug(df_inferred_types)

        # Converting data to inferrred data types
        logger.debug("DataFileUploadAPIView : clean_dataframe : Converting received data to inferred types")
        df_cleaned = conversion_engine.convert_data_types(df, df_inferred_types)
        logger.debug("DataFileUploadAPIView : clean_dataframe : Converted received data to inferred types")
        logger.debug(df_cleaned)

        # Create updated dtypes dict to be sent to the clinet
        df_cleaned_dtypes = {} 
        for col_name in df_cleaned:
            df_cleaned_dtypes[col_name] = str(df_cleaned[col_name].dtype)
        
        logger.debug(str([(df_cleaned[col_name].name, str(df_cleaned[col_name].dtype)) for col_name in df_cleaned]))

        return {
            "dtypes" : df_cleaned_dtypes,
            "data" : df_cleaned
        }
    
class PaginatedDataView(APIView):
    """
    This view returns a page of data from the cleaned dataset.

    The view takes a key for the cleaned data stored in the cache and a page number
    from the request. It then returns the corresponding page of data from the dataset.
    """

    def get(self, request, cleaned_data_key):
        
        logger.debug(f'PaginatedDataView : get : Requesting paginated data for key: {cleaned_data_key}')
        
        # Retrieve the cleaned data from the cache
        df_cleaned_bytes = cache.get(cleaned_data_key)
        if df_cleaned_bytes is None:
            logger.error(f'PaginatedDataView : get : Data not found for key: {cleaned_data_key}')
            return Response({"message": "Data not found. Please check your data key"}, status=status.HTTP_404_NOT_FOUND)

        df_cleaned = pickle.loads(df_cleaned_bytes)
        logger.debug(f'PaginatedDataView : get : Successfully retrieved cleaned data from cache for key: {cleaned_data_key}')

        # Create updated dtypes dict to be sent to the client
        df_cleaned_dtypes = {} 
        for col_name in df_cleaned:
            df_cleaned_dtypes[col_name] = str(df_cleaned[col_name].dtype)

        # Converting complex dtypes columns to strings to allow json serialization
        for col_name in df_cleaned:
            if df_cleaned[col_name].dtype == 'complex':
                df_cleaned[col_name] = df_cleaned[col_name].astype(str)

        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(df_cleaned.to_dict(orient='records'), request)
        logger.debug(f'PaginatedDataView : get : Returning paginated cleaned data for key: {cleaned_data_key}')

        return Response({
            "message": "Successfully retrieved paginated data.", 
            "data": paginated_data, 
            "cleaned_data_key" : cleaned_data_key}, 
            status=status.HTTP_200_OK)

class UpdateColumnsDataTypesAPIView(APIView):
    """
    This view updates the data types of specified columns along with the data formats in the dataset.

    It receives a request containing the changes to be made to the data types
    of certain columns and applies these changes to the cleaned dataset.
    """

    serializer_class = DataTypesChangeRequestSerializer

    def post(self, request):
        logger.debug('UpdateColumnsDataTypesAPIView : post : Beginning of method')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            logger.debug('UpdateColumnsDataTypesAPIView : post : Request data is validated')

            # Fetching the original and cleaned dataframe cache keys
            original_df_key = data["original_data_key"]
            cleaned_df_key = data["cleaned_data_key"]

            # Loading original and cleaned dataframes from cache
            original_df_bytes = cache.get(original_df_key)
            original_df = pickle.loads(original_df_bytes)

            cleaned_df_bytes = cache.get(cleaned_df_key)
            df_cleaned = pickle.loads(cleaned_df_bytes)

            col_dtypes_updates = data["dtypes"] # Fetch dtypes to update for the columns

            for col_dtype_update in col_dtypes_updates:
                col_name = col_dtype_update["col_name"]
                type_to_cast = col_dtype_update["dtype"]
                missing_values_handling_option = col_dtype_update["missing_values"]
                default_value = col_dtype_update["default"]
                invalid_values_handling_option = data["invalid_values"]

                # Cast original dataframe column data to received type
                try:
                    original_df = conversion_engine.convert_col_date_type(original_df, col_name, type_to_cast, invalid_values_handling_option, missing_values_handling_option, default_value)
                    logger.debug(f'UpdateColumnsDataTypesAPIView : post : Converted column "{col_name}" to type "{type_to_cast}"')
                except ValueError as e:
                    logger.error(f'UpdateColumnsDataTypesAPIView : post : Error converting column "{col_name}" to type "{type_to_cast}": {str(e)}')
                    return Response({ "message" : "Error cleaning dataframe", "error" : str(e) }, status=status.HTTP_400_BAD_REQUEST)
                except TypeError as e:
                    logger.error(f'UpdateColumnsDataTypesAPIView : post : Invalid data passed for column "{col_name}": {str(e)}')
                    return Response({ "message" : "Invalid data passed", "error" : str(e) }, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error(f'UpdateColumnsDataTypesAPIView : post : Error cleaning dataframe for column "{col_name}": {str(e)}')
                    return Response({ "message" : "Error cleaning dataframe", "error" : str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Replace updated column in the cleaned dataframe
                df_cleaned[col_name] = original_df[col_name]

            # Caching the updated cleaned dataframe
            df_cleaned_bytes = pickle.dumps(df_cleaned)
            cache.set(cleaned_df_key, df_cleaned_bytes)
            logger.debug('UpdateColumnsDataTypesAPIView : post : Updated cleaned dataframe cached')

            # Create updated dtypes dict to be sent to the client
            df_cleaned_dtypes = {} 
            for col_name in df_cleaned:
                df_cleaned_dtypes[col_name] = str(df_cleaned[col_name].dtype)

            # Converting complex dtypes columns to strings to allow json serialization
            for col_name in df_cleaned:
                if df_cleaned[col_name].dtype == 'complex':
                    df_cleaned[col_name] = df_cleaned[col_name].astype(str)

            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(df_cleaned.to_dict(orient='records'), request)
            logger.debug('UpdateColumnsDataTypesAPIView : post : Paginated the cleaned data')

            return Response({
                "message": "Request is successful.", 
                "data": paginated_data, 
                "dtypes" : df_cleaned_dtypes, 
                "original_data_key" : original_df_key, 
                "cleaned_data_key" : cleaned_df_key}, 
                status=status.HTTP_200_OK)
        
        logger.error(f'UpdateColumnsDataTypesAPIView : post : Validation failed for request data: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
