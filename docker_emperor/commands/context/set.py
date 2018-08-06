import six
import docker_emperor.logger as logger
from docker_emperor.nodes.context import Context


def run(root, *args, **kwargs):

    name = args[0].strip() if args else None
    if name:
        if name in root.project['contexts']:
            root.project.config['context'] = name
            logger.success(u'Context <b>%s</b> selected.' % root.context.name)
        else:
            logger.error(u'Context <b>%s</b> unknow.' % name)
            exit(0)

    else:
        contexts = root.project['contexts']
        if not contexts:
            contexts['default'] = Context('default')
            root.project.config['context'] = 'default'
            logger.warning(u'No context defines, use <b>%s</b>.' % root.context.name)
        else:

            def select_context_name(contexts):
                logger.ask(u'Please select the <b>{}</b> context to work on'.format(root.project.name))
                for i, c in enumerate(contexts):
                    logger.choice(u'<b>%s</b>] %s' % (i+1, c.name))
                ci = six.moves.input(': ')
                try:
                    if ci == '0':
                        raise Exception
                    return contexts[int(ci)-1].name
                except Exception as e:
                    logger.error(u'<b>%s/b> is not a valid choice' % ci)
                    return select_context_name(contexts)

            root.project.config['context'] = select_context_name(contexts)
            logger.success(u'Context <b>%s</b> selected.' % root.context.name)