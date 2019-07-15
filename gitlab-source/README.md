# poll gitlab issues

A script that polls a queue from gitlab issues and dispatches tasks to workers

See also [here](https://python-gitlab.readthedocs.io/en/stable/)

## Prepare

1. `pip install -r requirements.txt --user`
1. Generate a gitlab personal access key
1. Create a `setenv` file, with following values:

```
export GITLAB_URL=<the base URL for gitlab>
export GITLAB_TOKEN=<the personal access token>
export GITLAB_API=4
export GITLAB_PROJECT=<the relative path to your project>
```