import os
import json
import socket
import requests
import datetime
from google.cloud import storage
from google.oauth2 import service_account
from google.auth import default
from google.auth.transport.requests import Request

class GCSErrorDiagnostic:
    def __init__(self, bucket_name, service_account_path=None):
        self.bucket_name = bucket_name
        self.service_account_path = service_account_path
        self.results = {}
        
    def run_diagnostics(self):
        print("=== GCS Error Diagnostic Results ===\n")
        
        self._check_environment()
        self._check_credentials()
        self._check_network()
        self._check_bucket_existence()
        self._check_service_account_status()
        self._check_token_expiration()
        
        self._print_results()
        
    def _check_environment(self):
        """Check environment-related issues"""
        print("Checking environment variables...")
        
        # Check GOOGLE_APPLICATION_CREDENTIALS
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.results['env_vars'] = {
            'GOOGLE_APPLICATION_CREDENTIALS': {
                'status': creds_path is not None,
                'value': creds_path,
                'message': 'Environment variable not set' if not creds_path else 'Set to: ' + creds_path
            }
        }
        
        # Check if the credentials file exists
        if creds_path:
            file_exists = os.path.exists(creds_path)
            self.results['env_vars']['credentials_file_exists'] = {
                'status': file_exists,
                'message': 'Credentials file exists' if file_exists else 'Credentials file not found'
            }
    
    def _check_credentials(self):
        """Check credential-related issues"""
        print("Checking credentials...")
        
        try:
            if self.service_account_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.service_account_path
                )
            else:
                credentials, project = default()
            
            self.results['credentials'] = {
                'valid': {
                    'status': True,
                    'message': 'Credentials are valid'
                }
            }
            
            # Check if credentials are scoped
            scopes = credentials.scopes if hasattr(credentials, 'scopes') else None
            self.results['credentials']['scopes'] = {
                'status': scopes is not None,
                'value': scopes,
                'message': f'Scopes: {scopes}' if scopes else 'No scopes found'
            }
            
        except Exception as e:
            self.results['credentials'] = {
                'valid': {
                    'status': False,
                    'message': f'Invalid credentials: {str(e)}'
                }
            }
    
    def _check_network(self):
        """Check network-related issues"""
        print("Checking network connectivity...")
        
        # Check basic internet connectivity
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            internet_status = True
        except OSError:
            internet_status = False
            
        self.results['network'] = {
            'internet': {
                'status': internet_status,
                'message': 'Internet connection available' if internet_status else 'No internet connection'
            }
        }
        
        # Check GCS connectivity
        try:
            response = requests.get('https://storage.googleapis.com', timeout=5)
            gcs_status = response.status_code == 200
        except Exception:
            gcs_status = False
            
        self.results['network']['gcs_api'] = {
            'status': gcs_status,
            'message': 'Can reach GCS API' if gcs_status else 'Cannot reach GCS API'
        }
    
    def _check_bucket_existence(self):
        """Check if the bucket exists and is accessible"""
        print("Checking bucket status...")
        
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_name)
            exists = bucket.exists()
            
            self.results['bucket'] = {
                'exists': {
                    'status': exists,
                    'message': f'Bucket {self.bucket_name} exists' if exists else f'Bucket {self.bucket_name} does not exist'
                }
            }
            
            if exists:
                # Try to get bucket metadata
                bucket.reload()
                self.results['bucket']['metadata'] = {
                    'status': True,
                    'value': {
                        'location': bucket.location,
                        'storage_class': bucket.storage_class,
                        'created': bucket.time_created
                    }
                }
        except Exception as e:
            self.results['bucket'] = {
                'error': {
                    'status': False,
                    'message': f'Error checking bucket: {str(e)}'
                }
            }
    
    def _check_service_account_status(self):
        """Check if the service account is enabled and active"""
        print("Checking service account status...")
        
        try:
            if self.service_account_path:
                with open(self.service_account_path) as f:
                    sa_info = json.load(f)
                    
                self.results['service_account'] = {
                    'email': {
                        'status': True,
                        'value': sa_info.get('client_email'),
                        'message': f'Service account email: {sa_info.get("client_email")}'
                    },
                    'project': {
                        'status': True,
                        'value': sa_info.get('project_id'),
                        'message': f'Project ID: {sa_info.get("project_id")}'
                    }
                }
        except Exception as e:
            self.results['service_account'] = {
                'error': {
                    'status': False,
                    'message': f'Error checking service account: {str(e)}'
                }
            }
    
    def _check_token_expiration(self):
        """Check if the authentication token is expired"""
        print("Checking token status...")
        
        try:
            if self.service_account_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.service_account_path
                )
                
                if not credentials.valid:
                    credentials.refresh(Request())
                
                expiry = credentials.expiry
                if expiry:
                    now = datetime.datetime.now(datetime.timezone.utc)
                    is_expired = expiry < now
                    
                    self.results['token'] = {
                        'expired': {
                            'status': not is_expired,
                            'value': expiry,
                            'message': f'Token expires at: {expiry}'
                        }
                    }
        except Exception as e:
            self.results['token'] = {
                'error': {
                    'status': False,
                    'message': f'Error checking token: {str(e)}'
                }
            }
    
    def _print_results(self):
        """Print diagnostic results in a readable format"""
        print("\n=== Diagnostic Results ===\n")
        
        for category, checks in self.results.items():
            print(f"\n{category.upper()}:")
            for check_name, check_data in checks.items():
                status_symbol = "✅" if check_data.get('status', False) else "❌"
                print(f"{status_symbol} {check_name}: {check_data.get('message', '')}")
                if 'value' in check_data:
                    print(f"   Value: {check_data['value']}")

if __name__ == "__main__":
    diagnostic = GCSErrorDiagnostic(
        bucket_name="mlflow-backend-storage-models",
        service_account_path="/home/MERHAWI/arrival_time/Arrival_time_estimation/mlflow_cld/my_gcp_k.json"
    )
    diagnostic.run_diagnostics()