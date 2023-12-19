from django.urls import path

from .views import read_dataset_and_upload

app_name = 'huggingface'

urlpatterns = [
    path('/populate/s3', read_dataset_and_upload)
]
