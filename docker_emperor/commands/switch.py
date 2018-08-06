

__all__ = ['run']


def run(root, *args, **kwargs):

    root.run_command('setenv', internal=True)