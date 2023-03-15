from avi.sdk.avi_api import ApiSession
import sys, json, yaml
#
# Variables
#
fileCredential = sys.argv[1]
path = 'cluster'
data = {"name": "cluster-0-1", "nodes": [{"name": "10.41.134.132", "ip": {"addr": "10.41.134.132", "type": "V4"}, "static_routes": [{"prefix": {"ip_addr": {"addr": "200.100.11.0", "type": "V4"}, "mask": 24}, "next_hop": {"addr": "10.41.134.157", "type": "V4"}, "route_id": "1"}]}], "tenant_uuid": "admin"}
#
# Avi class
#
class aviSession:
  def __init__(self, fqdn, username, password, tenant):
    self.fqdn = fqdn
    self.username = username
    self.password = password
    self.tenant = tenant

  def debug(self):
    print("controller is {0}, username is {1}, password is {2}, tenant is {3}".format(self.fqdn, self.username, self.password, self.tenant))

  def putObject(self, objectUrl, objectData):
    api = ApiSession.get_session(self.fqdn, self.username, self.password, self.tenant)
    result = api.post(objectUrl, data=objectData)
    return result.json()
#
# Main Pyhton script
#
if __name__ == '__main__':
    with open(fileCredential, 'r') as stream:
        credential = json.load(stream)
    stream.close
    defineClass = aviSession(credential['avi_credentials']['controller'], credential['avi_credentials']['username'], credential['avi_credentials']['password'], tenant)
    defineClass.putObject(path, data)
