import requests
import json
from requests_kerberos import HTTPKerberosAuth

API_ENDPOINT = 'http://10.0.10.133:8999/batches'

headers = {
  'Content-Type': 'application/json'
}
data2 = open('job.json')
json_data = json.load(data2)

r = requests.post(url=API_ENDPOINT, data=json.dumps(json_data), headers=headers, verify=False, auth=HTTPKerberosAuth())

print(r)
print(r.json())
