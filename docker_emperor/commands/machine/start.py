import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    if not root.mounting.is_running:
        if root.mounting.is_startable:
            logger.cmd('Start mounting <b>%s</b>' % (root.mounting.name, ))
            cmd = root.bash(
                root.mounting.docker_machine_bin, 
                'start', 
                root.mounting.name, 
                *args,
                sys=True
            )
            if root.mounting.is_running:
                root.logger.success('Machine <b>%s</b> started.' % (root.mounting.name, ))
        else:
            root.logger.warning('Machine <b>%s</b> is not startable.' % (root.mounting.name, ))

    return root.mounting.is_running

# class Command():

#     def run(self, *args, **kwargs):
#         if not self.interna
#         self.success('Machine <b>%s</b> started.' % (root.mounting.name, ))