import requests
import json
from requests_kerberos import HTTPKerberosAuth, REQUIRED

import logging
logging.basicConfig(filename='log.log',level=logging.DEBUG)

API_ENDPOINT = 'http://10.0.10.133:8999/batches'

headers = {
  'Content-Type': 'application/json'
}
data2 = open('job.json')
json_data = json.load(data2)

kerberos_auth = HTTPKerberosAuth(principal="user@HDP.LOCAL")
r = requests.post(url=API_ENDPOINT, data=json.dumps(json_data), headers=headers, verify=False, auth=kerberos_auth)
print(r.text)
