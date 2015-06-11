FROM ansible/ubuntu14.04-ansible:stable

ADD . /srv/bib-api
WORKDIR /srv/bib-api

RUN ansible-playbook ansible/docker_provision.yml -c local

EXPOSE 5000
ENTRYPOINT ["python3", "/srv/bib-api/run.py"]
