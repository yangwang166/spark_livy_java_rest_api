import requests
from requests.auth import HTTPBasicAuth

API_ENDPOINT = 'https://host:8443/gateway/test/livy/v1/batches'
the_headers = {
  'Content-Type': 'application/json'
}
r = requests.get(url=API_ENDPOINT, headers = the_headers, verify=False, auth=HTTPBasicAuth('user','password'))

print(r)
print(r.json())
