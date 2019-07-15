# Grafana automation

A couple of python runbooks to complete common grafana tasks. 

See also [here](https://github.com/m0nhawk/grafana_api/blob/master/README.md)

## Prepare

1. `pip install -r requirements.txt --user`
1. Generate a Grafana API key as well as an admin user
1. Create a `setenv` file, with following values:

```
export GRAFANA_API_KEY=<the grafana API key>
export GRAFANA_HOST=<the grafana host without protocol>

export GRAFANA_USER=<the grafana admin username>
export GRAFANA_PWD=<the grafana adimin's password>

export SOURCE_FOLDER_ID=<the id (not uid) of the "template folder>
```


