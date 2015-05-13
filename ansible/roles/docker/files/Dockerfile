FROM ubuntu:14.04
RUN apt-get update && \
    apt-get install --no-install-recommends -y software-properties-common && \
    apt-add-repository ppa:ansible/ansible && \
    apt-get update && \
    apt-get install -y ansible

RUN echo '[local]\nlocalhost\n' > /etc/ansible/hosts

ADD ansible /opt/
WORKDIR /opt/ansible

EXPOSE 5000
RUN ansible-playbook docker_provision.yml -c local
