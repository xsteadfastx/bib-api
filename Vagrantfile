# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "redis" do |redis|

    redis.vm.provider "docker" do |d|
      d.name = "bib-api-redis"
      d.build_dir = "./vagrant/redis"
    end

  end

  config.vm.define "bib-api" do |bibapi|

    bibapi.vm.network "forwarded_port", guest: 5000, host: 5000

    bibapi.vm.provider "docker" do |d|
      d.name = "bib-api"
      d.build_dir = "./vagrant/bib-api"
      d.has_ssh = true
      d.link("bib-api-redis:redis")
      d.env = { "REDIS_PORT_6379_TCP_ADDR" => "redis" }
    end

    bibapi.ssh.port = 22
    bibapi.ssh.forward_agent = true
    bibapi.ssh.forward_env = ["LC_UID"]

    bibapi.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/vagrant.yml"
      ansible.limit = "all"
      #ansible.verbose = "v"
      ansible.host_key_checking = false
    end

  end

end
