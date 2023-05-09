#!/bin/bash
#
username=$1
password=$2
ip=$3
next_hop=$4
prefix=$5
mask=$6
rm -f avi_cookie.txt
curl_output=$(curl -s -k -X POST -H "Content-Type: application/json" -d "{\"username\": \"$username\", \"password\": \"$password\"}" -c avi_cookie.txt https://$ip/login)
curl_cluster_status=$(curl -s -k -X GET -H "Content-Type: application/json" -b avi_cookie.txt https://$ip/api/cluster/status | jq .cluster_state.state)
echo $curl_cluster_status
curl_cluster=$(curl -s -k -X GET -H "Content-Type: application/json" -b avi_cookie.txt https://$ip/api/cluster)
json_with_route=$(echo $curl_cluster | jq '.nodes[0] += {"static_routes": [{"next_hop": {"addr": '\"$next_hop\"', "type":"V4"}, "prefix": {"ip_addr": {"addr": '\"$prefix\"', "type": "V4"}, "mask": '\"$mask\"'}, "route_id": "1"}]}')
csrftoken=`cat avi_cookie.txt | grep csrftoken | awk '{print $7}'`
curl -s -k -X PUT -H "X-CSRFToken: $csrftoken" -H "Referer: https://$ip/" -H "Content-Type: application/json" -b avi_cookie.txt -d $(echo $json_with_route | jq -r -c) https://$ip/api/cluster
retry=20
pause=30
attempt=0
while [ $attempt -ne $retry ]; do
  if [[ $(curl -s -k -X GET -H "Content-Type: application/json" -b avi_cookie.txt https://$ip/api/cluster/status | jq .cluster_state.state) == $curl_cluster_status ]] ; then
    echo "controller ready"
    break
  else
    echo "controller not ready yet - waiting for $pause seconds and retry"
    ((attempt++))
    sleep $pause
  fi
done
if [ $attempt -ge $retry ] ; then
  echo "ERROR: controller not ready after $attempt attempts"
  exit 255
fi