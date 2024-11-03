#!/bin/bash

# set config
mkdir ../local_files
echo "${CONFIG}" | base64 -d > ${CIRCLE_WORKING_DIRECTORY}/ops/config
chmod go-r ${CIRCLE_WORKING_DIRECTORY}/ops/config

## set ansible_local_vars
echo "${LOCAL_VARS}" | base64 -d > ../local_files/ansible_local_vars.yml
echo "${INVENTORY}" | base64 -d > ../local_files/inventory
echo "export KUBECONFIG=${CIRCLE_WORKING_DIRECTORY}/ops/config" >> ${BASH_ENV}
echo "export PYENV_ROOT=\"/virtual-python\"" >> ${BASH_ENV}
echo "export PATH=\"\$PYENV_ROOT/bin:\$PATH\"" >> ${BASH_ENV}
echo "export PATH=\"\$PYENV_ROOT/shims:\$PATH\"" >> ${BASH_ENV}
echo "export PATH=\"\$PYENV_ROOT/libexec:\$PATH\"" >> ${BASH_ENV}