from django.urls import path
from .views import DataFileUploadAPIView, hello_world

urlpatterns = [
    path('hello_world/', hello_world, name='hello-world'),
    path('upload-file/', DataFileUploadAPIView.as_view(), name='upload-file')
]