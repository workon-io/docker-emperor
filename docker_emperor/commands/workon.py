import os
import six
import docker_emperor.logger as logger


__all__ = ['run']


def run(root, *args, **kwargs):

    project = None

    project_name = args[0] if len(args) else None
    if project_name:
        project = root.projects.get(project_name)
        if not project:
            logger.warning('Project <b>%s</b> unknow.' % project_name)
            
    if not project:

        def select_project():
            # logger.ask('0) no machine (localhost)')
            logger.ask('Select the project to work on')
            for i, p in enumerate(root.projects.items()):
                key, value = p
                logger.choice('<b>{}]</b> {}'.format(i+1, key))
            pi = six.moves.input(': ')
            try:
                if pi == '0':
                    raise Exception
                return root.projects.items()[int(pi)-1]
            except Exception as e:
                logger.error('{} is not a valid choice'.format(pi))
                return select_project()
        project_name, project = select_project()

    if project:
        workdir = project.get('workdir')
        if workdir and os.path.isdir(workdir):
            logger.success('Workon the project <b>%s</b> in <b>%s</b>' % (project_name, workdir))
            os.chdir(workdir)
            shell = os.environ.get('SHELL', '/bin/sh')
            # root.run_command('info', internal=True)
            os.execl(shell, shell)
            return
            # execl() does not return; it replaces the Python process with a new shell process
    