import logging
import os
import requests
import json
from requests.auth import HTTPBasicAuth

# logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

API_ENDPOINT = 'https://hostname:8443/gateway/test/livy/v1/batches'
data2 = open('job.json')
json_data = json.load(data2)
method = 'POST'

session = requests.Session()
response = session.request(
    method=method,
    url=API_ENDPOINT,
    timeout=60,
    headers={'content-type': 'application/json'},
    data=json.dumps(json_data),
    verify=False,
    auth=HTTPBasicAuth('username','password')
)

logger.debug(response.status_code)
logger.debug(response.text)
