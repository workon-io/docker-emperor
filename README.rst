*Estimated reading time: 5 minutes*

# Overview of Docker Emperor

Docker Emperor is a CLI Tool for orchestrate multi-container Docker applications with a Docker Compose YAML extended file. 
Then, with a few commands, you create and start all the services from your configuration like compose but also deploy and manage those applications in their context (via Docker Machine as possible). 
To learn more about all the features of Docker Emperor, see [the list of features](/docker/docker-emperor/overview/#features).

## Docker Emperor is designed to

- Describe **all your project** and those functionnal environments in **one smallest YML file**.

- Manage and deploy in **one or few command** (de build, de launch, de deploy).

- Work as **Never bash to remote** local CLI (with the Docker Machine little help).

- Write **custom commands** very easly in the description file.

- Has full **combinatory / heritage capabilities** (environment, commands, services, volumes, etc..). 

- Compatible with any docker-compose existing files.

- Lightweight and dependency-less.

You can learn more about each case in  [Common Use Cases](/docker/docker-emperor/overview/#common-use-cases).

## Using Docker Emperor is basically a three-step process

1.  Define your app’s environment with a  `Dockerfile`  so it can be reproduced anywhere.
    
2.  Define the services that make up your app in  `docker-emperor.yml`  so they can be run together in an isolated environment.
    
3.  Run  `docker-emperor launch` or shortly `de launch` to starts and runs your entire app.
    


### Here an example of a simple django web application, with postgres, redis over nginx :

A  `docker-emperor.yml`  looks like an `docker-compose.yml` file and is compose-compatible, but has optionnal extended features.

```
name: example_webapp
version: '3.6'

environment:
    - PYTHONBUFFERED=1
    - STG=/var/storage/example_webapp

commands:
    manage: exec webapp python manage.py
    install: 
        - build
        - hosts:set
    init: launch -d 
    debug: logs -f --tail=100 webapp
    enter: exec webapp bash    

hosts: 
    - example_webapp.com

services:
    nginx:
        links:
            - webapp:webapp
        ports:
            - '80:80'
            - '443:443'
        volumes:
            - ${STG}/static:/stg/static:ro
            - ${STG}/media:/stg/media:ro  
        restart: always
    postgres:
        volumes:
            - ${STG}/postgres/:/var/lib/postgresql/data
        restart: always
    redis:
        volumes:
            - ${STG}/redis/:/data
        restart: always
    webapp:
        volumes:
            - ./webapp:/webapp 
            - ${STG}/media:/stg/media
            - ${STG}/static:/stg/static
        links:
            - postgres:postgres
            - redis:redis
        restart: always
        command: uwsgi --ini uwsgi.ini --http-socket :8000

mounting:  

    localhost:

        environment:
            - DEBUG=1

        hosts: 
            - example_webapp.com.local

        commands:
            migrate:
                - manage migrate
                - manage makemigrations

        services:
            webapp:
                tty: true
                command: python -u manage.py runserver 0.0.0.0:8000 --traceback


    prod:

        environment:
            - COMPRESS_ENABLED=1

        commands:
            deploy:
                - bash git push origin master
                - syncfiles
                - build
                - init
                - manage migrate --no-input
                - manage collectstatic --no-input --clear
                - manage compress --force
            driver: generic 
                  --generic-ip-address example_webapp.com
                  --generic-ssh-key ~/.ssh/id_rsa 
                  --generic-ssh-user root
            files:
                - ./webapp

```

Then the commands you can run with The Docker-emperor CLI :

All commands are launched with **@localhost** default mounting if not specified.

- ```de install``` from the custom commands defined in the .yml file, that run ```de build``` and set hosts.
- ```de init``` from the custom commands defined in the .yml file, that run ```de launch -d```, a short ready composed combination of ```de down & de up -d```.
- ```de create @prod``` That create Docker Machine defined for **prod** definition.
- ```de deploy @prod``` from the custom commands defined in for **prod** definition, that deploy the application trought Docker Machine.
