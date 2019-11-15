import logging
import os
import requests
from requests_kerberos import HTTPKerberosAuth

# logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

method = 'GET'

url = "http://ip-10-0-10-87.amer.xxxx.local:50070/webhdfs/v1/user/liveadmin/parking/?op=LISTSTATUS"

session = requests.Session()
response = session.request(
    method=method,
    url=url,
    timeout=60,
    headers={'content-type': 'application/octet-stream'},
    auth=HTTPKerberosAuth(principal="liveadmin@HDPCLUSTER.LOCAL:cloudera")
)

logger.debug(response.status_code)
logger.debug(response.text)
