from django.urls import path
from .views import hello_data_cleanser, DataFileUploadAPIView, PaginatedDataView, UpdateColumnsDataTypesAPIView

urlpatterns = [
    path('hello/', hello_data_cleanser, name='hello'),
    path('upload-file/', DataFileUploadAPIView.as_view(), name='upload-file'),
    path('data/<str:cleaned_data_key>/', PaginatedDataView.as_view(), name='paginated_data'),
    path('update-columns-dtypes/', UpdateColumnsDataTypesAPIView.as_view(), name='update-columns-dtypes'),
]