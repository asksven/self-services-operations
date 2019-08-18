FROM python:3


ADD workhorse-gitlab-source/*.py /workhorse-gitlab-source/
ADD workhorse-gitlab-source/*.cfg /workhorse-gitlab-source/ 
ADD workhorse-gitlab-source/workhorse.sh /workhorse-gitlab-source/
ADD workhorse-gitlab-source/requirements.txt /workhorse-gitlab-source/

RUN pip install -r /workhorse-gitlab-source/requirements.txt


ADD action-grafana-app-dashboards/*.py /action-grafana-app-dashboards/
ADD action-grafana-app-dashboards/action.sh /action-grafana-app-dashboards/
ADD action-grafana-app-dashboards/requirements.txt /action-grafana-app-dashboards/

RUN pip install -r /action-grafana-app-dashboards/requirements.txt


ENTRYPOINT [ "/bin/bash", "-c", "cd /workhorse-gitlab-source && ./workhorse.sh" ]