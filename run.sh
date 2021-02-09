#!/bin/bash

docker-compose up -d

# bit ugly, find a better way to wait for grafana startup
sleep 10

echo 'Creating a new Viewer for yearn dashboards in grafana...'
BASIC_AUTH=${GF_SECURITY_ADMIN_USER:=admin}:${GF_SECURITY_ADMIN_PASSWORD:=admin}
URL=http://$BASIC_AUTH@localhost:3000/api/admin/users

curl -X POST -d@grafana/yearn_user.json $URL -H 'Content-Type: application/json'
