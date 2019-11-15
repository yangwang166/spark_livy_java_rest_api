import requests
from requests.auth import HTTPBasicAuth

API_ENDPOINT = 'https://ip-10-0-10-87.amer.o9solutions.local:8443/gateway/test/livy/v1/batches'
the_headers = {
  'Content-Type': 'application/json'
}
r = requests.get(url=API_ENDPOINT, headers = the_headers, verify=False, auth=HTTPBasicAuth('liveadmin','cloudera'))

print(r)
print(r.json())
