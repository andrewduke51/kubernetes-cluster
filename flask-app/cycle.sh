#!/bin/bash

docker build -t andrewduke51/app:latest .                   ## build new code or feature
docker push andrewduke51/app:latest                         ## push the code to the container repository
kubectl delete pod local --namespace local                  ## delete the running one in AKS
kubectl apply -f .                                          ## deploy the new one

termdown 10
echo "latest code is being deployed from local"
kubectl port-forward local -n local  5000:5000