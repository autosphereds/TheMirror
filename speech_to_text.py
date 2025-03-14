import json
import os
from google.cloud import secretmanager, speech

# -------------------------
# 1️⃣ Retrieve Google Credentials from Secret Manager
# -------------------------
def get_google_credentials():
    """Retrieve credentials from Google Cloud Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    
    # Replace YOUR_PROJECT_ID with your actual Google Cloud Project ID
    secret_name = "projects/YOUR_PROJECT_ID/secrets/SPEECH_TO_TEXT_CREDENTIALS/versions/latest"
    
    # Access the secret
    response = client.access_secret_version(name=secret_name)
    
    # Parse the secret (JSON format)
    credentials_json = response.payload.data.decode("UTF-8")
    return json.loads(credentials_json)

# -------------------------
# 2️⃣ Save Credentials to a Temporary File
# -------------------------
def save_temp_credentials(credentials_dict):
    """Save credentials to a temporary file for Google API authentication"""
    temp_credential_file = "temp_gcloud_key.json"
    with open(temp_credential_file, "w") as f:
        json.dump(credentials_dict, f)

    # Set the environment variable dynamically
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_credential_file

# -------------------------
# 3️⃣ Initialize Google Cloud Speech-to-Text API
# -------------------------
def initialize_speech_client():
    """Initialize Google Cloud Speech Client"""
    return speech.SpeechClient()

# -------------------------
# 4️⃣ Run the Setup
# -------------------------
if __name__ == "__main__":
    credentials_dict = get_google_credentials()  # Retrieve credentials
    save_temp_credentials(credentials_dict)  # Save credentials to file
    client = initialize_speech_client()  # Initialize Speech-to-Text API

    print("✅ Google Cloud Speech-to-Text API is set up and ready to use securely!")
