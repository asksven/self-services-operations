#!/usr/bin/env bash

if [ -z "$NAMESPACE" ] || [ -z "$DEPLOY_ENV" ]
then
  echo "\$NAMESPACE and \$DEPLOY_ENV should not be empty! If you run locall please source setenv"
  exit 1
fi

# $NAMESPACE is defined in .gitlab-ci.yaml


#kubectl delete namespace $NS
kubectl create namespace $NAMESPACE

kubectl --namespace=$NAMESPACE delete secret regcred
kubectl --namespace=$NAMESPACE create secret docker-registry regcred --docker-server=$DOCKER_REGISTRY --docker-username=$DOCKER_REGISTRY_USER --docker-password=$DOCKER_REGISTRY_PASSWORD --docker-email=foo@bar.com


K8S_DIR=./manifests
TARGET_DIR=${K8S_DIR}/.generated
mkdir -p ${TARGET_DIR}
for f in ${K8S_DIR}/*.yaml
do
  jinja2 $f ./variables/${DEPLOY_ENV}.yaml \
  --format=yaml --strict \
  -D DOCKER_REGISTRY=${DOCKER_REGISTRY} \
  -D DOCKER_REGISTRY_NS=${DOCKER_REGISTRY_NS} \
  -D DOCKER_REGISTRY_USER=${DOCKER_REGISTRY_USER} \
  -D DOCKER_REGISTRY_PASSWORD=${DOCKER_REGISTRY_PASSWORD} \
  -D GITLAB_TOKEN=${GITLAB_TOKEN} \
  -D GRAFANA_API_KEY=${GRAFANA_API_KEY} \
  -D GRAFANA_USER=${GRAFANA_USER} \
  -D GRAFANA_PWD=${GRAFANA_PWD} \
  > "${TARGET_DIR}/$(basename ${f})"
done

  
kubectl --namespace=$NAMESPACE apply -f ${TARGET_DIR}

# todo: find a better solution for recycling pods: we do this to make sure that changes in configmaps are getting re-read by the pods
kubectl -n $NAMESPACE delete pods -l app=self-service-ops

