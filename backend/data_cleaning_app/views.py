from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import DataFileSerializer
import pandas as pd

# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

class DataFileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DataFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]

            try:
                df = pd.read_csv(uploaded_file)
                print("Data types before inference:")
                print(df.dtypes)
            except:
                print("Error occured while parsing csv format.")

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)