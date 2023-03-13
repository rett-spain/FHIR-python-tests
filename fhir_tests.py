import requests
from fhir.resources.bundle import Bundle
import json
from datetime import datetime, date
from decimal import Decimal
from my_secrets import client_id, client_secret, fhirurl, tenant_id


# Define a custom JSON encoder to handle FHIR types
class FhirJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif hasattr(obj, 'as_json'):
            return obj.as_json()
        else:
            return super().default(obj)


# Construct the authentication endpoint URL
auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
# Replace the endpoint URL with your own FHIR service endpoint
url = fhirurl + "/Patient"

# Construct the authentication request parameters
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": fhirurl
}

# Send the authentication request and retrieve the access token
response = requests.post(auth_url, data=data)
if response.status_code != 200:
    raise Exception(f"Authentication failed: {response.text}")

# Extract the access token from the response
bearer_token = response.json()["access_token"]
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

# Make a GET request to retrieve all patients
response = requests.get(url, headers=headers)

# Parse the response into a Bundle object
if response.status_code != 200:
    raise Exception(f"GET failed: {response.text}")
bundle = Bundle.parse_raw(response.content)

# Print the Bundle object as JSON
print(json.dumps(bundle.dict(), cls=FhirJsonEncoder, indent=4))
