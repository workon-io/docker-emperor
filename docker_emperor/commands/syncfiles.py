import os
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):
  
    logger.cmd('Sync files for project <b>%s</b>' % (root.compose.name, ))
    root.run_command('machine:start', internal=True)
    if not root.mounting.is_localhost:

        # ex. docker-machine scp -r -d . virtualbox:/home/docker/project.dev.localhost/
        for file in root.mounting['files']:
            
            cmd = root.bash(
                root.mounting.docker_machine_bin,
                'scp',
                '--quiet',
                '-r',
                '-d',
                file, 
                '{}:{}'.format(
                    root.mounting.docker_machine_name,#root.compose.name, 
                    root.mounting['workdir']
                ),
                is_system=True,
            )
            print(cmd.cmd_line)
    else:
        logger.warning(root.mounting.LOCAL_MACHINE_WARNING)
