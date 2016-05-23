FROM 32bit/ubuntu:14.04

ENV LANG C.UTF-8
RUN locale-gen de_DE.UTF-8

RUN apt-get update \
 && apt-get install -y \
      openssh-server \
      redis-server \
      supervisor \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# User and SSH
RUN useradd --create-home -s /bin/bash vagrant \
 && mkdir -p /var/run/sshd \
 && chmod 0755 /var/run/sshd \
 && mkdir -p /home/vagrant/.ssh \
 && echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/vagrant/.ssh/authorized_keys \
 && chown -R vagrant: /home/vagrant/.ssh \
 && echo -n 'vagrant:vagrant' | chpasswd \
 && echo 'vagrant ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/vagrant

# Add files
ADD root /

EXPOSE 22
CMD ["/usr/bin/supervisord"]
