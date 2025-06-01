import sys
import time
import jwt

# Open PEM
private_key = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIManFOb+prO2BzEOsI/+7qadTDThNuDI54n9X2UahYcH
-----END PRIVATE KEY-----
"""

payload = {
    'iat': int(time.time()) - 30,
    'exp': int(time.time()) + 900,
    'sub': '2B2F6DK7JK'
}
headers = {
    'kid': 'T7PT8GP2CP'
}

# Generate JWT
encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers = headers)

print(f"JWT:  {encoded_jwt}")