import requests
import json
from requests_kerberos import HTTPKerberosAuth, REQUIRED

API_ENDPOINT = 'https://10.0.10.133:8999/batches'

headers = {
  'Content-Type': 'application/json'
}
data2 = open('job.json')
json_data = json.load(data2)
r = requests.post(url=API_ENDPOINT, data=json.dumps(json_data), headers=headers, auth=HTTPKerberosAuth(mutual_authentication=REQUIRED, sanitize_mutual_error_response=False), verify=False)


#r = requests.post(url=API_ENDPOINT, data=json.dumps(json_data), headers=headers, verify=False, auth=HTTPKerberosAuth())
#r = requests.post(url=API_ENDPOINT, data=json.dumps(json_data), headers=headers, verify=True, auth=HTTPKerberosAuth(), cert=['/home/liveadmin/yang2/livy.crt'])

print(r.text)