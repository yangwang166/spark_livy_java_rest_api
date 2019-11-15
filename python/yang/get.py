import requests
from requests_kerberos import HTTPKerberosAuth

API_ENDPOINT = 'http://10.0.10.133:8999/batches'
headers = {
  'Content-Type': 'application/json'
}
r = requests.get(url=API_ENDPOINT, headers=headers, verify=False, auth=HTTPKerberosAuth())
print(r)
print(r.json())
