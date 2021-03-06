#! /bin/bash

ssh travis@35.206.176.121 bash -c "'
  set -Eeuo pipefail
  cd /etc/rasaplatform/
  sudo docker login -u _json_key -p \"\$(cat /etc/rasaplatform/travis-gcloud.json)\" https://gcr.io
  sudo docker-compose pull --ignore-pull-failures
  sudo docker login -u _json_key -p \"\$(cat /etc/rasaplatform/gcr-auth.json)\" https://gcr.io
  sudo docker-compose pull --ignore-pull-failures
  sudo docker-compose down
  sudo docker-compose up -d'"
