import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import DataFileSerializer
import pandas as pd
from pandas.errors import ParserError
import os
import redis

import sys
sys.path.append('../') 
from data_cleanser import inference as inference_engine, conversion as conversion_engine

logger = logging.getLogger("django")
r = redis.Redis()


# Create your views here.
@api_view(['GET'])
def hello_data_cleanser(request):
    return Response({"message": "Hello! Welcome to data cleanser."})

class DataFileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser) # for parsing request data
    serializer_class = DataFileSerializer

    def post(self, request):
        
        logger.debug('DataFileUploadAPIView : post : Beginning of method')
        
        file_data_serializer = self.serializer_class(data=request.data)
        
        if file_data_serializer.is_valid():
            # Access the uploaded file
            uploaded_file = file_data_serializer.validated_data["file"]
            file_name = uploaded_file.name
            file_extension = os.path.splitext(file_name)[1]

            df = pd.DataFrame() # Define an empty dataframe to be replaced with parsed one

            if file_extension == '.csv':
                try:
                    df = pd.read_csv(uploaded_file)
                    logger.debug('DataFileUploadAPIView : post : Successfully parsed data from csv file.')
                except ParserError:
                    logger.error(f"Error occurred while parsing file: {file_name}")
                    return Response({"message": f"Error occurred while parsing file: {file_name}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            elif file_extension in ['.xls', '.xlsx', '.xlsm', '.xlsb']:
                try:
                    df = pd.read_excel(uploaded_file)
                    logger.debug('DataFileUploadAPIView : post : Successfully parsed data from excel file.')
                except ParserError:
                    logger.error(f"DataFileUploadAPIView : post : Error occurred while parsing file: {file_name}")
                    return Response({"message": f"Error occurred while parsing file: {file_name}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            else:
                logger.error(f"DataFileUploadAPIView : post : Received unsupported data file type: {file_name}")
                return Response({"message": "Received unsupported data file type"}, status=status.HTTP_400_BAD_REQUEST )
            
        
            cleaned_data = self.clean_dataframe(df)
            return Response({"message": "File cleaned successfully", "dtypes": cleaned_data["dtypes"], "data": cleaned_data["data"]}, status=status.HTTP_200_OK)

        else:
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
        df_converted = conversion_engine.convert_data_types(df, df_inferred_types)
        logger.debug("DataFileUploadAPIView : clean_dataframe : Converted received data to inferred types")
        logger.debug(df_converted)
        
        logger.debug(str([(df_converted[col_name].name, str(df_converted[col_name].dtype)) for col_name in df_converted]))

        return {
            "dtypes" : df_inferred_types,
            "data" : df_converted
        }