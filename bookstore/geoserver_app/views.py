import os
import uuid
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.miniotest import MinioManager
from utils.geoserver import Geoserver

# GeoServer config
# geoserver_username = os.getenv("GEOSERVER_ADMIN_USER" , "sedreh")
# geoserver_password = os.getenv("GEOSERVER_ADMIN_PASSWORD", "ABcd1234!@")
# geoserver_rest_url = os.getenv("GEOSERVER_URL" ,"http://geoserver:8080/geoserver/rest/")

# MioIO config
minio_endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
# minio_username = os.getenv("MINIO_ROOT_USER", "admin")
# minio_password = os.getenv("MINIO_ROOT_PASSWORD", "sedreh313")
bucket_name = os.getenv("MINIO_BUCKET_NAME_BOOKSTORE", "bookstore")

class GeoserverManager(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]


    def post(self, request):

        uploaded_file = request.FILES.get("file")
        file_data = uploaded_file.read()
        workspace = request.data.get("workspace")
        store_name = request.data.get("store_name")

        if not file_data or not workspace or not store_name:
            return Response({"error": "Missing file or parameters."}, status=400)
        if not bucket_name:
            return Response({"error": "Bucket name is required."}, status=400)


        file_name = f"{uuid.uuid4()}.tif"
        print(bucket_name)
        print(file_name)
        print("************///////////////******************")
        print(workspace,"123456************" ,store_name)
        minio = MinioManager()
        minio_url = minio.upload(bucket_name=bucket_name, file_name=file_name, file=file_data)
        print(minio_url , "minio_url")
        if not minio_url:
            return Response({"error": "Failed to upload file to MinIO."}, status=500)
        geoserver = Geoserver()
        # Check workspace and store creation
        geoserver.create_workspace(workspace)
        store_created = geoserver.create_layer_with_store(workspace, store_name, minio_url)  #geotiff_url-> minio_url
        if not store_created:
                return Response({"error": f"Store '{store_name}' already exists in workspace '{workspace}'. Please choose a different name."}, status=409)
        geoserver.publish_layer(workspace, store_name)
        return Response({"message": "TIFF uploaded and layer published successfully."})
