from grafana_api.grafana_face import GrafanaFace
import os

print(os.environ['GRAFANA_HOST'])
# grafana_api = GrafanaFace(protocol='https', auth=os.environ['GRAFANA_API_KEY'], host=os.environ['GRAFANA_HOST'])
grafana_api = GrafanaFace(auth=(os.environ['GRAFANA_USER'], os.environ['GRAFANA_PWD']),protocol='https', host=os.environ['GRAFANA_HOST'])

print('Logged in')

# Find a user by email
user = grafana_api.users.find_user('sven.knispel@gmail.com')

print(user)

source_folder_id = '46'

res = grafana_api.search.search_dashboards(folder_ids=source_folder_id)
print(res)
for dashboard in res:
    print(dashboard["title"])

