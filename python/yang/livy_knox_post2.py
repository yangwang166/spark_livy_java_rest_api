import requests
import json
from requests.auth import HTTPBasicAuth

API_ENDPOINT = 'https://hostname_livy:8443/gateway/test/livy/v1/batches'
the_headers = {
  'Content-Type': 'application/json'
}
data2 = open('job.json')
json_data = json.load(data2)
r = requests.post(url=API_ENDPOINT, headers=the_headers, 
                  data=json.dumps(json_data),
                  verify=False, auth=HTTPBasicAuth('username','password'))

print(r.text)
print(r.json())
