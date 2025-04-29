import io
from minio import Minio
from minio.error import S3Error
import os

# MioIO config
minio_endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
minio_access_key = os.getenv("MINIO_ACCESS_KEY", "cILmKujcwn5DVB7HzU0z")
minio_secret_key= os.getenv("MINIO_SECRET_KEY", "tBp0EYhnhXT1IlN3vwfLLOp5ZNbcjgjnZJmkJX8r")
bucket_name = os.getenv("MINIO_BUCKET_NAME_BOOKSTORE", "bookstore")

class MinioManager:

    def __init__(self):
        # استفاده از متغیرهای محیطی برای تنظیم کلیدهای دسترسی
        self.client = Minio(
            "minio:9000",  # برای اتصال به MinIO
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False  # اگر از HTTPS استفاده می‌کنید این را به True تغییر دهید
        )

    def upload(self, bucket_name, file_name, file, minio_endpoint="minio:9000"):
        try:
            # بررسی وجود bucket
            found = self.client.bucket_exists(bucket_name)
            if not found:
                self.client.make_bucket(bucket_name)
                print(f"Created bucket: {bucket_name}")
            else:
                print(f"Bucket '{bucket_name}' already exists")

            # تبدیل فایل به داده‌های باینری
            data_stream = io.BytesIO(file)

            # آپلود فایل به MinIO
            self.client.put_object(
                bucket_name,
                file_name,
                data_stream,
                length=len(file),
                content_type="application/octet-stream"
            )
            print(f"Successfully uploaded {file_name} to bucket {bucket_name}")

            # ساخت URL برای فایل آپلود شده
            minio_url = f"http://{minio_endpoint}/{bucket_name}/{file_name}"
            return minio_url
        except S3Error as exc:
            print(f"Error uploading file: {exc}")
            return None
