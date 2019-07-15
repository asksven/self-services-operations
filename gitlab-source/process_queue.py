import gitlab
import os
import json
import subprocess

import constants


# private token or personal token authentication
gl = gitlab.Gitlab(
    os.environ['GITLAB_URL'],
    private_token=os.environ['GITLAB_TOKEN'], 
    api_version=os.environ['GITLAB_API'],
    per_page=100)

# make an API request to create the gl.user object. This is mandatory if you
gl.auth()


project = gl.projects.get(os.environ['GITLAB_PROJECT'])
#print(project)

#print(projects)
open_issues = project.issues.list(state='opened',labels=['Automation'])

for issue in open_issues:
    
    if 'Doing' not in issue.labels:
        print('Processing %s' % issue.title)

        notes = issue.notes.list()
        for note in notes:

            try:

                data = json.loads(note.body)
                action = data["action"]
                params = data["params"]
                print(params)
                success = False
                res = ''

                # Take the issue in processing
                issue.labels = ['Doing', 'Automation']
                issue.save()
                print('Processing %s' % action)

                if action == constants.ACTION_CREATE_GRAFANA_MONITORING:
                    print('checking params')
                    app = params["app"]
                    editor = params["editor"]
                    print('Params are %s %s' % (app, editor))
                    
                    sp = subprocess.Popen(
                        '. ../grafana-worker/setenv && python ../grafana-worker/create_app.py "%s" "%s"' % (app, editor),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    
                    out, err = sp.communicate()
                    
                    out = out.decode("utf-8")
                    err = err.decode("utf-8")

                    res = '# Output:\n```bash\n%s\n```\n\n# Errors:\n```\n%s\n```' % (out, err)

                    if sp.returncode == 0:
                        success = True
                    else:
                        success = False    
                    
                    print('!!!!Returncode:')
                    print(sp.returncode)    
                    print('!!!!Out:')
                    print(out)
                    print('!!!!Err:')
                    print(err)
                    
                                        
                elif action == constants.ACTION_NOP:
                    success = True
                    lines = 'No action was defined'
                else:
                    print('Action %s is unknown' % action)
                    success = False

                print('Wrapping up issue')
                print(success)

                i_note = issue.notes.create({'body': 'Result: %s' % res})
                if success == True:
                    # we want to annotate and close the issue    
                    print('Close the issue with comment %s' % res)
                    issue.state_event = 'close'
                    issue.labels = ['Completed', 'AutomationError']
                else:
                    issue.labels = ['Doing', 'AutomationError']


                issue.save()
                                
            except json.JSONDecodeError as exc:
                print(exc)
                res = '# Invalid JSON:\n```\n%s\n```' % exc
                issue.labels = ['Doing', 'AutomationError']
                i_note = issue.notes.create({'body': '%s' % res})
                issue.save()
    else:
        print('issue is already in status Doing')