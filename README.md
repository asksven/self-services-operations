# A simple architecture for self-service ops

## Architecture

1. A workhorse (e.g. `workhorse-gitlab-source`) polls gitlab as the source for self-service requests. The workhorse implements a bash script `workhorse.sh`
2. The workhorse parses the request to determine what action was requested for; based on that it delegates the fulfillment of the request to the action, e.g. `action-grafana-app-dashboard`
3. Each action implements a script `action.sh` that is called by the worker and takes care of fulfilling the request
4. both `workhorse.sh` and `action.sh` are responsible to validate their input and environment variables they need to run

## Run locally

1. Install dependencies: see `README.md` in your `workhorse-` and `action-` directories
2. Source the environment variables using `source setenv` for both the workhorse and the actions
3. Run the workhorse

## Docker

### Build 

`docker build . -t self-service-ops`

### Run

We need to pass all the environment variables to the workhorse and actions. These are the sum of all variables defined in all relevant `setenv`:

```
docker run --env GITLAB_URL --env GITLAB_TOKEN \
--env GITLAB_PROJECT --env GRAFANA_API_KEY --env GRAFANA_HOST \
--env GRAFANA_USER --env GRAFANA_PWD --env SOURCE_FOLDER_ID \
self-service-ops
```
 
## k3d (locally)

### Prepare

Create `ops/setenv` with following variables:

```
#!/bin/bash

# base64 value created with echo -b '<value>' | base64 -w 0
export GITLAB_TOKEN=<base64-token-goes-here>
# base64 value created with echo -b '<value>' | base64 -w 0
export GRAFANA_API_KEY=<base64-api-key-goes-here>
# base64 value created with echo -b '<value>' | base64 -w 0
export GRAFANA_USER=<base64-user-goes-here>
# base64 value created with echo -b '<value>' | base64 -w 0
export GRAFANA_PWD=<base64-password-goes-here>
export NAMESPACE=<namespace-where-to-deploy>
export DEPLOY_ENV=<environment-name>
export DOCKER_REGISTRY=<registry-url>
export DOCKER_REGISTRY_NS=<image-namespace-prefix>
export DOCKER_REGISTRY_USER=<registry-user>
export DOCKER_REGISTRY_PASSWORD=<registry-password>
```

### Deploy

Pre-req: the image has been pushed to a registry accessible to k3d

```
cd ops
source setenv
./deploy.sh
```
