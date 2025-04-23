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

# GeoServer config
geoserver_username = settings.GEOSERVER_USERNAME
geoserver_password = settings.GEOSERVER_PASSWORD
geoserver_rest_url = settings.GEOSERVER_REST_URL

class GeoserverManager(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = HTTPBasicAuth(geoserver_username, geoserver_password)

    def create_workspace(self, workspace):
        request_url = f"{geoserver_rest_url}/workspaces"
        headers = {"content-type": "application/xml"}
        workspace_xml = f"""<workspace><name>{workspace}</name></workspace>"""

        response = requests.post(request_url, headers=headers, data=workspace_xml, auth=self.auth)
        if response.status_code == 409:  # 409 = Already exists
            print(f"⚠ Workspace '{workspace}' already exists.")
        elif not response.ok:
            raise Exception(f"Failed to create workspace: {response.status_code}, {response.text}")

    def check_store_exists(self, workspace, store_name):
        request_url = f"{geoserver_rest_url}/workspaces/{workspace}/coveragestores/{store_name}.xml"
        response = requests.get(request_url, auth=self.auth)
        return response.status_code == 200  # If store exists, status code will be 200

    def create_layer_with_store(self, workspace, store_name, geotiff_url):
        store_exists = self.check_store_exists(workspace, store_name)
        if store_exists:
            print(f"⚠ Store '{store_name}' already exists in workspace '{workspace}'.")
            return False  # Don't try to create if it exists

        request_url = f"{geoserver_rest_url}/workspaces/{workspace}/coveragestores"
        headers = {"content-type": "application/xml"}
        store_xml = f"""<coverageStore>
                            <name>{store_name}</name>
                            <type>GeoTIFF</type>
                            <enabled>true</enabled>
                            <workspace>{workspace}</workspace>
                            <url>{geotiff_url}</url>
                        </coverageStore>"""

        response = requests.post(request_url, headers=headers, data=store_xml, auth=self.auth)
        if not response.ok:
            raise Exception(f"Failed to create store: {response.status_code}, {response.text}")
        return True

    def publish_layer(self, workspace, store_name):
        request_url = f"{geoserver_rest_url}/workspaces/{workspace}/coveragestores/{store_name}/coverages/"
        headers = {"content-type": "application/xml"}
        layer_xml = f"""<coverage>
                            <name>{store_name}</name>
                            <title>{store_name}</title>
                            <nativeName>geotiff_coverage</nativeName>
                            <enabled>true</enabled>
                        </coverage>"""
        response = requests.post(request_url, headers=headers, data=layer_xml, auth=self.auth)
        if not response.ok:
            raise Exception(f"Failed to publish layer: {response.status_code}, {response.text}")

    def post(self, request):
        file = request.FILES.get("file")
        workspace = request.data.get("workspace")
        store_name = request.data.get("store_name")

        if not file or not workspace or not store_name:
            return Response({"error": "Missing file or parameters."}, status=400)

        file_name = f"{uuid.uuid4().hex}_{file.name}"
        shared_dir = settings.GEOSERVER_SHARED_DIR
        os.makedirs(shared_dir, exist_ok=True)

        full_path = os.path.join(shared_dir, file_name)
        with open(full_path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        os.chmod(full_path, 0o644)

        geotiff_url = f"file://{full_path}"

        # Check workspace and store creation
        self.create_workspace(workspace)
        store_created = self.create_layer_with_store(workspace, store_name, geotiff_url)
        if not store_created:
            return Response({"error": f"Store '{store_name}' already exists in workspace '{workspace}'. Please choose a different name."}, status=409)

        self.publish_layer(workspace, store_name)

        return Response({"message": "TIFF uploaded and layer published successfully."})
