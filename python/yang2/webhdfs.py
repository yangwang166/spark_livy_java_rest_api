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
#url = 'https://nightly61x-2.nightly61x.root.hwx.site:20102/webhdfs/v1/user/hue?op=liststatus'

url = "http://ip-10-0-10-87.amer.xxx.local:50070/webhdfs/v1/user/userssss/parking/?op=LISTSTATUS"

session = requests.Session()
response = session.request(
    method=method,
    url=url,
    timeout=60,
    headers={'content-type': 'application/octet-stream'},
    auth=HTTPKerberosAuth(principal="usersss@HDPCLUSTER.LOCAL")
)
#print(response.text)

logger.debug(response.status_code)
logger.debug(response.text)
