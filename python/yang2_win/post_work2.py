import requests
import json
from requests_kerberos import HTTPKerberosAuth, REQUIRED
from krbcontext import krbContext

import logging
logging.basicConfig(filename='post.log',level=logging.DEBUG)

API_ENDPOINT = 'http://10.0.10.133:8999/batches'

headers = {
  'Content-Type': 'application/json'
}
data2 = open('job.json')
json_data = json.load(data2)

with krbContext(using_keytab=True, principal='liveadmin@HDPCLUSTER', keytab_file='C:\yang\liveadmin.keytab',ccache_file='C:\yang\krb5cc_post2'):
    kerberos_auth = HTTPKerberosAuth(principal="liveadmin@HDPCLUSTER.LOCAL:cloudera")
    r = requests.post(url=API_ENDPOINT, data=json.dumps(json_data), headers=headers, verify=False, auth=kerberos_auth)
    print(r.text)