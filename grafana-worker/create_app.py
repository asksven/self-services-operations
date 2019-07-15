from grafana_api.grafana_face import GrafanaFace
from grafana_api.grafana_api import GrafanaAPI

import os
import argparse
import json
import sys

parser = argparse.ArgumentParser(description='Create a team and dashboards for an app')

# Add the arguments
parser.add_argument('App',
                       metavar='app',
                       type=str,
                       help='the name of the application')

parser.add_argument('Editor',
                       metavar='editor',
                       type=str,
                       help='the e-mail address of the user who should be added as editor')

# Execute the parse_args() method
args = parser.parse_args()

#input_path = args.App
print('App: %s' % args.App)
print('Editor: %s' % args.Editor)
print('Endpoint: %s' % os.environ['GRAFANA_HOST'])

try:
    grafana_api = GrafanaFace(auth=(os.environ['GRAFANA_USER'], os.environ['GRAFANA_PWD']),protocol='https', host=os.environ['GRAFANA_HOST'])

    # 1. Create team if it does not exist
    # 2. Add user to team if he is not already member
    try:
        user = grafana_api.users.find_user(args.Editor)
        user_id = user["id"]
        print(user)
    except:
        sys.stderr.write('User does not exist. Aborting!')
        exit(1)

    name = 'Team %s' % args.App
    print('Searching for team %s' % name)
    team = grafana_api.teams.get_team_by_name(name)
    print(team)
    if not team:
        # team does not exist
        try:
            json = {"name": name} 
            print(json)
            res = grafana_api.teams.add_team(json)
            team_id = res["teamId"]
            #res = grafana_api.teams.add_team(name)
            print(team_id)
        except Exception as ex:
            sys.stderr.write('Creating team failed. Aborting!')
            print(ex)
            exit(1)
    else:
        team_id = team[0]["id"]

    print('Adding user %i to team %i' % (user_id, team_id))
    try:
        res = grafana_api.teams.add_team_member(team_id, user_id)
        print(res)
    except Exception as ex:
        print('Info: User is already in team')

    # 3. Create a folder
    # 4. Grant team editor on folder
    name = '%s monitoring' % args.App
    try:
        folder = grafana_api.folder.create_folder(name)
        print(folder)
        folder_uid = folder["uid"]
        folder_id = folder["id"]
        
        print('Folder created %s' % folder_uid)
        try:    
            json = { "items": [
                {"role": "Viewer","permission": 1},
                {"role": "Editor", "permission": 2},
                {"teamId": team_id, "permission": 2}
            ]} 

            res = grafana_api.folder.update_folder_permissions(folder_uid, json)
            print(res)    
        except Exception as ex:
            sys.stderr.write('Adding permissions to folder failed. Aborting!')
            print(ex)
            exit(1)
   
    except Exception as ex:
        sys.stderr.write('Folder already exists. Aborting!')
        print(ex)
        exit(1)

    # 5. Import dashboards to folder (from folder "App monitoring templates")
    source_folder_id = os.environ['SOURCE_FOLDER_ID']

    res = grafana_api.search.search_dashboards(folder_ids=source_folder_id)
    print(res)
    for dashboard in res:
        print('Copying %s' % dashboard["title"])
    
        
        try:    
            res = grafana_api.dashboard.get_dashboard(dashboard["uid"])
            #res = grafana_api.dashboard.get_dashboard(source_dashboard_uid)
            dashboard = res['dashboard']
            dashboard["id"] = None
            dashboard["uid"] = None
            dashboard["version"] = 0

            json = {
                "dashboard": dashboard,
                "folderId": folder_id,
                "overwrite": False
            }
            #print(json)
            res = grafana_api.dashboard.update_dashboard(json)
        except Exception as ex:
            sys.stderr.write('Adding dashboard to folder failed. Aborting!')
            print(ex)
            exit(1)


except Exception as ex:
    sys.stderr.write('API Call failed')
    print(ex)
    exit(1)

