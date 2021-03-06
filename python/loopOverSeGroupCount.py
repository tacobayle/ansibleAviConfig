import requests, json, os, yaml, sys
#
# this python script is used to iterate over a list of tasks (when using other loop inside the list of tasks)
#
playbook = sys.argv[1]
avi_credentials = sys.argv[2]
cloud_no_access_vcenter_uuid = sys.argv[3]
ova_path = sys.argv[4]
vsphere_username = sys.argv[5]
vsphere_password = sys.argv[6]
jsonFile = sys.argv[7]
# no_access_vcenter = sys.argv[8]
#data_loaded = json.loads(str(sys.argv[9]).replace("'", '"'))
# data_loaded = yaml.load(sys.argv[9])
with open(jsonFile, 'r') as stream:
    data_loaded = json.load(stream)
stream.close
count = 0
# print(data_loaded)
for item in data_loaded['serviceEngineGroup']:
    os.system('ansible-playbook {0} --extra-vars \'{{"seg":{1}}}\' --extra-vars \'{{"avi_credentials":{2}}}\' --extra-vars \'{{"cloud_no_access_vcenter_uuid":{3}}}\' --extra-vars \'{{"ova_path":{4}}}\' --extra-vars \'{{"vsphere_username":{5}}}\' --extra-vars \'{{"vsphere_password":{6}}}\' --extra-vars \'{{"count":{7}}}\''.format(playbook, item, avi_credentials, cloud_no_access_vcenter_uuid, ova_path, vsphere_username, vsphere_password, count))
    count += int(item['numberOfSe'])
#os.system('rm -f {0}'.format(jsonFile))
