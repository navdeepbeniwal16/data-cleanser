from django.urls import path
from .views import DataFileUploadAPIView, hello_data_cleanser

urlpatterns = [
    path('hello/', hello_data_cleanser, name='hello'),
    path('upload-file/', DataFileUploadAPIView.as_view(), name='upload-file')
]