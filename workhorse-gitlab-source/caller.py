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

open_issues = project.issues.list(state='opened',labels=['Automation'])

for issue in open_issues:
    print('Processing %s' % issue.title)
    
    if 'Doing' not in issue.labels:
        
        notes = issue.notes.list()
        for note in notes:
            print('Processing note: %s' % note.body)
            try:
                data = json.loads(note.body)
                action = data["action"]
                params = data["params"]
                app = params['app']
                print(params)
                exit()
                success = False
                res = ''

                print('Processing %s' % action)

                if action == constants.ACTION_CREATE_GRAFANA_MONITORING:
                    print('checking params')
                    app = params["app"]
                    editor = params["editor"]
                    print('Params are %s %s' % (app, editor))
                    sp = subprocess.Popen(
                        '. ../grafana-worker/setenv && python called.py %s %s' % (app, editor),
                        shell=True, 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    out, err = sp.communicate()
                    out = out.decode("utf-8")
                    err = err.decode("utf-8")
                    print('!!!!Returncode:')
                    print(sp.returncode)    
                    print('!!!!Out:')
                    print(out)
                    print('!!!!Err:')
                    print(err)

                    res = '# Output:\n```bash\n%s\n```\n\n# Errors:\n```\n%s\n```' % (out, err)
                    #for line in out.split():
                    #    res.append(line)
                    print('!!!!Res:')
                    print(res)

    #                if out:
    #                    print('Finished')
                    success = True
                    #res = out
                    print('!!!!Res:')
                    print(res)
    #                if err:    
    #                    print('ERR %s' % err)
    #                    success = True
                    #for line in lines:
                    #    res += line
                    #print(res)
                    
                elif action == constants.ACTION_NOP:
                    success = True
                    lines = 'No action was defined'
                else:
                    print('Action %s is unknown' % action)
                    success = False

                print('Wrapping up issue')
                print(success)
                if success == True:
                    # we want to annotate and close the issue    
                    print('Close the issue')
                    i_note = issue.notes.create({'body': '%s' % res})
                    issue.save()
                
            except json.JSONDecodeError as exc:
                print(exc)
                res = '# Invalid JSON:\n```\n%s\n```' % exc
                issue.labels = ['Doing', 'AutomationError']
                i_note = issue.notes.create({'body': '%s' % res})
                issue.save()

                    
    else:
        print('issue is already in status Doing')                
