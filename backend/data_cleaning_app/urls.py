from django.urls import path
from .views import hello_data_cleanser, DataFileUploadAPIView, UpdateColumnsDataTypesAPIView

urlpatterns = [
    path('hello/', hello_data_cleanser, name='hello'),
    path('upload-file/', DataFileUploadAPIView.as_view(), name='upload-file'),
    path('update-columns-dtypes/', UpdateColumnsDataTypesAPIView.as_view(), name='update-columns-dtypes'),
]