import gitlab
import os
import json
import subprocess
import logging

import constants

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


# private token or personal token authentication
gl = gitlab.Gitlab(
    os.environ['GITLAB_URL'],
    private_token=os.environ['GITLAB_TOKEN'], 
#    api_version=os.environ['GITLAB_API'],
    per_page=100)

# make an API request to create the gl.user object. This is mandatory if you
gl.auth()


project = gl.projects.get(os.environ['GITLAB_PROJECT'])
#print(project)

#print(projects)
open_issues = project.issues.list(state='opened',labels=['Automation'])

for issue in open_issues:
    
    if 'Doing' not in issue.labels:
        logging.info('Processing Issue %s' % issue.title)

        notes = issue.notes.list()
        for note in notes:

            try:
                logging.debug('Processing Note %s' % note.body)

                if note.body.startswith('{'):
                    data = json.loads(note.body)
                    action = data["action"]
                    params = data["params"]
                    print(params)
                    success = False
                    res = ''

                    # Take the issue in processing
                    issue.labels = ['Doing', 'Automation']
                    issue.save()
                    logging.info('Processing %s' % action)

                    if action == constants.ACTION_CREATE_GRAFANA_MONITORING:
                        logging.debug('checking params')
                        app = params["app"]
                        editor = params["editor"]
                        logging.debug('Params are %s %s' % (app, editor))
                        
                        sp = subprocess.Popen(
                            '../action-grafana-app-dashboards/action.sh "%s" "%s"' % (app, editor),
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
                        
                        logging.debug('!!!!Returncode:')
                        logging.debug(sp.returncode)    
                        logging.debug('!!!!Out:')
                        logging.debug(out)
                        logging.debug('!!!!Err:')
                        logging.debug(err)
                        
                                            
                    elif action == constants.ACTION_NOP:
                        success = True
                        lines = 'No action was defined'
                    else:
                        logging.error('Action %s is unknown' % action)
                        success = False

                    logging.debug('Wrapping up issue')
                    logging.debug(success)

                    i_note = issue.notes.create({'body': 'Result: %s' % res})
                    if success == True:
                        # we want to annotate and close the issue    
                        logging.info('Close the issue with comment %s' % res)
                        issue.state_event = 'close'
                        issue.labels = ['Completed', 'AutomationError']
                    else:
                        issue.labels = ['Doing', 'AutomationError']

                    issue.save()
                else:
                    logging.debug('Note is no JSON: %s' % note.body)       
                                 
            except json.JSONDecodeError as exc:
                logging.debug(exc)
                res = '# Invalid JSON:\n```\n%s\n```' % exc
                issue.labels = ['Doing', 'AutomationError']
                i_note = issue.notes.create({'body': '%s' % res})
                issue.save()
    else:
        logging.debug('issue is already in status Doing')