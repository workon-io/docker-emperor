import os
import six
import docker_emperor.logger as logger


__all__ = ['run']


def run(root, *args, **kwargs):

    machines = root.project['machines']
    for i, m in enumerate(root.project['machines']):
        logger.choice(u'<b>{}</b>] {}'.format(i+1, m.name))
