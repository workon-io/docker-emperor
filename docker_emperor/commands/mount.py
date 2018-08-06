import os
import six
import docker_emperor.logger as logger


__all__ = ['run']


def run(root, *args, **kwargs):

    name = args[0].strip() if args else None
    if name:
        if name in root.project['mounting']:
            root.project.config['mounting'] = name
            logger.success(u'Mounting <b>%s</b> selected.' % root.mounting.name)
        else:
            logger.error(u'Mounting <b>%s</b> unknow.' % name)
            exit(1)

    else:
        def select_mounting_name():
            # logger.ask('0) no mounting (localhost)')
            logger.ask(u'Please select the <b>{}</b> mounting to work on'.format(root.project.name))
            for i, m in enumerate(root.project['mounting']):
                logger.choice(u'<b>{}</b>] {}'.format(i+1, m.name))
            mi = six.moves.input(': ')
            try:
                if mi == '0':
                    raise Exception
                return root.project['mounting'][int(mi)-1].name
            except Exception as e:
                logger.error(u'<b>%s</b> is not a valid choice' % mi)
                return select_mounting_name()

        root.project.config['mounting'] = select_mounting_name()
        logger.success(u'Mounting <b>%s</b> selected.' % root.mounting.name)
