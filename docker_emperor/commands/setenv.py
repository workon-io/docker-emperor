

__all__ = ['run']


def run(root, *args, **kwargs):

    root.run_command('context:set', internal=True)
    root.run_command('machine:set', internal=True)