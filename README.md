# bib-api
[![Build Status](https://travis-ci.org/xsteadfastx/bib-api.svg?branch=master)](https://travis-ci.org/xsteadfastx/bib-api)
[![Coverage Status](https://coveralls.io/repos/xsteadfastx/bib-api/badge.svg?branch=master)](https://coveralls.io/r/xsteadfastx/bib-api?branch=master)

Unofficial Stadtbibliothek Nürnberg API

## using docker-compose

thats the most easiest way to get everything up and running. it will get redis and link everything together. dont forget to set the secret key evironment variable in `docker-compose.yml`.

1. `git clone https://github.com/xsteadfastx/bib-api.git`
2. `cd bib-api`
3. `docker-compose up -d`

## manual

of course you can start everything by your own.

1. `docker pull xsteadfastx/bib-api`
2. `docker run -d --name bib-api-redis redis`
3. `docker run -d --name bib-api --link bib-api-redis:redis -p 127.0.0.1:9999:5000 xsteadfastx/bib-api`
