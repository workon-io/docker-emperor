import os
import six
import docker_emperor.logger as logger


__all__ = ['run']


def run(root, *args, **kwargs):

    name = args[0].strip() if args else None
    if name:
        if name in root.project['machines']:
            root.project.config['machine'] = name
            logger.success(u'Machine <b>%s</b> selected.' % root.machine.name)
        else:
            logger.error(u'Machine <b>%s</b> unknow.' % name)
            exit(1)

    else:

        def select_machine_name():
            # logger.ask('0) no machine (localhost)')
            logger.ask(u'Please select the <b>{}</b> machine to work on'.format(root.project.name))
            for i, m in enumerate(root.project['machines']):
                logger.choice(u'<b>{}</b>] {}'.format(i+1, m.name))
            mi = six.moves.input(': ')
            try:
                if mi == '0':
                    raise Exception
                return root.project['machines'][int(mi)-1].name
            except Exception as e:
                logger.error(u'<b>%s</b> is not a valid choice' % mi)
                return select_machine_name()

        root.project.config['machine'] = select_machine_name()
        logger.success(u'Machine <b>%s</b> selected.' % root.machine.name)
