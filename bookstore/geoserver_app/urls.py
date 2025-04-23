from django.urls import path
from .views import GeoserverManager  # یا از هرجا که اون کلاس اومده

urlpatterns = [
    path('upload-tiff/', GeoserverManager.as_view(), name='upload_tiff'),
]
