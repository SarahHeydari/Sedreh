import os

import requests
from requests.auth import HTTPBasicAuth

# GeoServer config
geoserver_username = os.getenv("GEOSERVER_ADMIN_USER" , "sedreh")
geoserver_password = os.getenv("GEOSERVER_ADMIN_PASSWORD", "ABcd1234!@")
geoserver_rest_url = os.getenv("GEOSERVER_URL" ,"http://geoserver:8080/geoserver/rest/")

# MioIO config
# minio_endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
# minio_username = os.getenv("MINIO_ROOT_USER", "admin")
# minio_password = os.getenv("MINIO_ROOT_PASSWORD", "sedreh313")
# bucket_name = os.getenv("MINIO_BUCKET_NAME_BOOKSTORE", "bookstore")


class Geoserver:

    def __init__(self):
        self.auth = HTTPBasicAuth(geoserver_username, geoserver_password)

    def create_workspace(self, workspace):
        request_url = f"{geoserver_rest_url}/workspaces"
        headers = {"content-type": "application/xml"}
        workspace_xml = f"""<workspace><name>{workspace}</name></workspace>"""

        response = requests.post(request_url, headers=headers, data=workspace_xml, auth=self.auth)
        if response.status_code == 409:  # 409 = Already exists
            print(f" Workspace '{workspace}' already exists.")
        elif not response.ok:
            raise Exception(f"Failed to create workspace: {response.status_code}, {response.text}")
        # print(workspace,"123456************")
    def check_store_exists(self, workspace, store_name):
        request_url = f"{geoserver_rest_url}/workspaces/{workspace}/coveragestores/{store_name}.xml"
        response = requests.get(request_url, auth=self.auth)
        # print(store_name)
        return response.status_code == 200  # If store exists, status code will be 200

    def create_layer_with_store(self, workspace, store_name, minio_url):  #geotiff_url-> minio_url
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
                            <url>{minio_url}</url>
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
        if response.status_code == 500:
            raise Exception(f"Failed to publish layer: {response.status_code}, {response.text}")
        elif response.status_code == 409:
            print(f"Layer '{store_name}' already exists in workspace '{workspace}'.")
        else:
            print(f"Layer '{store_name}' successfully published.")

