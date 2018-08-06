# Docker CLI that combine docker-compose and docker-machine for a full stack deployment

- describe all your project stack in one YML docker-emperor file
- docker-emperor file is compatible with any docker-compose existing files
- Manage and deploy in one or few command (de build, de start, de deploy)
- Switching context and machine in one: 
    - Work in local if you want: de dev@localhost start
    - Create defined machines on the fly: de test@virtualbox create
    - Start mahcine and compose project, then run all: de test@virtualbox start
    - Deploy on the targeted machine: de test@virtualbox deploy
    
- Compose file extensions with environment contexts and machines
- Combine services for extremely more readability
- Totaly Docker compatible, it just an overrider tool and a command manager
- Nginx emperor capability for manage multiple web hosted project
- Zero downtime deployment capability
- Lightweight and dependency-less