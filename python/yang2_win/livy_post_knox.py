import requests
import json
from requests.auth import HTTPBasicAuth

API_ENDPOINT = 'https://ip-10-0-10-87.amer.xxx.local:8443/gateway/test2/livy/v1/batches'
the_headers = {
  'Content-Type': 'application/json'
}
data2 = open('job.json')
json_data = json.load(data2)
r = requests.post(url=API_ENDPOINT, headers=the_headers,
                  data=json.dumps(json_data),
                  verify=False, auth=HTTPBasicAuth('yang.wang','xxx'))

print(r.text)
print(r.json())
