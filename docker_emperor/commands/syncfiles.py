import os
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):

    mounting = root.mounting    
    logger.cmd('Sync files for project <b>%s</b>' % (root.compose.name, ))
    root.run_command('machine:start', internal=True)
    if not mounting.is_localhost:

        # ex. docker-machine scp -r -d . virtualbox:/home/docker/project.dev.localhost/
        for file in mounting['files']:
            
            cmd = root.bash(
                root.mounting.docker_machine_bin,
                'scp',
                '-r',
                '-d',
                file, 
                '{}:{}'.format(
                    mounting.name, 
                    root.mounting['workdir']
                ),
                is_system=True,
            )
            print(cmd.cmd_line)
    else:
        logger.warning(mounting.LOCAL_MACHINE_WARNING)
