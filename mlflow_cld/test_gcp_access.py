import os
from google.cloud import storage
from google.cloud.storage import Bucket
from google.api_core import exceptions
from google.oauth2 import service_account
import json

class GCSPermissionChecker:
    def __init__(self, bucket_name, service_account_path):
        self.bucket_name = bucket_name
        self.service_account_path = service_account_path
        self.client = None
        self.bucket = None
        self.service_account_email = None
        
    def setup_client(self):
        """Initialize storage client with service account"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_path)
            self.client = storage.Client(credentials=credentials)
            
            # Get service account email
            with open(self.service_account_path) as f:
                sa_info = json.load(f)
            self.service_account_email = sa_info.get('client_email')
            
            return True
        except Exception as e:
            print(f"❌ Failed to setup storage client: {str(e)}")
            return False

    def check_permissions(self):
        """Check all required permissions for MLflow artifact logging"""
        print(f"\n=== Checking permissions for {self.service_account_email} ===\n")
        
        results = {
            "bucket_access": self._check_bucket_access(),
            "object_operations": self._check_object_operations(),
            "metadata_operations": self._check_metadata_operations()
        }
        
        print("\n=== Permission Check Summary ===")
        all_passed = True
        for category, checks in results.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for permission, status in checks.items():
                status_symbol = "✅" if status else "❌"
                print(f"{status_symbol} {permission}")
                if not status:
                    all_passed = False
        
        if not all_passed:
            print("\n🔧 Required IAM Roles:")
            print("1. storage.objects.create")
            print("2. storage.objects.get")
            print("3. storage.objects.list")
            print("4. storage.objects.delete")
            print("5. storage.buckets.get")
            
            print("\n📝 You can grant these permissions by adding these roles:")
            print("- roles/storage.objectViewer")
            print("- roles/storage.objectCreator")
            
            print("\nRun this command to add roles:")
            print(f"gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \\\n"
                  f"    --member=serviceAccount:{self.service_account_email} \\\n"
                  f"    --role=roles/storage.objectViewer")
            print(f"gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \\\n"
                  f"    --member=serviceAccount:{self.service_account_email} \\\n"
                  f"    --role=roles/storage.objectCreator")
        
        return all_passed

    def _check_bucket_access(self):
        """Check basic bucket access permissions"""
        try:
            self.bucket = self.client.bucket(self.bucket_name)
            return {
                "storage.buckets.get": self._try_operation(
                    lambda: self.bucket.exists()
                )
            }
        except Exception as e:
            return {"storage.buckets.get": False}

    def _check_object_operations(self):
        """Check object-level operations"""
        results = {}
        test_blob_name = "mlflow_permission_test_file"
        
        # Test create
        results["storage.objects.create"] = self._try_operation(
            lambda: self.bucket.blob(test_blob_name).upload_from_string("test")
        )
        
        # Test list
        results["storage.objects.list"] = self._try_operation(
            lambda: next(self.bucket.list_blobs(max_results=1), None)
        )
        
        # Test get
        results["storage.objects.get"] = self._try_operation(
            lambda: self.bucket.get_blob(test_blob_name)
        )
        
        # Test delete
        results["storage.objects.delete"] = self._try_operation(
            lambda: self.bucket.blob(test_blob_name).delete()
        )
        
        return results

    def _check_metadata_operations(self):
        """Check metadata-related permissions"""
        return {
            "storage.buckets.get": self._try_operation(
                lambda: self.bucket.get_iam_policy()
            )
        }

    def _try_operation(self, operation):
        """Helper to execute an operation and return boolean success"""
        try:
            operation()
            return True
        except (exceptions.Forbidden, exceptions.PermissionDenied):
            return False
        except Exception as e:
            print(f"Unexpected error during operation: {str(e)}")
            return False

if __name__ == "__main__":
    BUCKET_NAME = "mlflow-backend-storage-models"
    SA_KEY_PATH = "/home/MERHAWI/arrival_time/Arrival_time_estimation/mlflow_cld/my_gcp_k.json"
    
    checker = GCSPermissionChecker(BUCKET_NAME, SA_KEY_PATH)
    if checker.setup_client():
        checker.check_permissions()