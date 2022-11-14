#!/usr/bin/env bash

AUTH_TOKEN=$1
RUNNER_NAME=$2

sed -i 's/%% AUTH_TOKEN %%/'${AUTH_TOKEN}'/g' /opt/circleci/launch-agent-config.yaml
sed -i 's|%% RUNNER_NAME %%|'${RUNNER_NAME}'|g' /opt/circleci/launch-agent-config.yaml
systemctl restart circleci.service