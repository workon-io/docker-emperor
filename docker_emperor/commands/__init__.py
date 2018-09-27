import six
import os
import subprocess
import docker_emperor.logger as logger
import tempfile


__all__ = ['Command']


COMPOSE_COMMANDS = [
    'build',
    'bundle',
    'config',
    'create',
    'down',
    'events',
    'exec',
    'help',
    'kill',
    'logs',
    'pause',
    'port',
    'ps',
    'pull',
    'push',
    'restart',
    'rm',
    'run',
    'scale',
    'start',
    'stop',
    'top',
    'unpause',
    'up',
]

MACHINE_COMMANDS = [
    'active',
    'config',
    'create',
    'env',
    'help',
    'inspect',
    'ip',
    'kill',
    'ls',
    'mount',
    'provision',
    'regenerate-certs',
    'restart',
    'rm',
    'scp',
    'ssh',
    'start',
    'status',
    'stop',
    'upgrade',
    'url',
]



class Command():

    verbose = 0

    def __repr__(self):
        return self.cmd_line

    def __init__(self, *args, **kwargs):

        self.args = list(args)
        self.env = kwargs.pop('env', [])
        self.is_system = kwargs.pop('is_system', False)
        self.compose = kwargs.pop('compose', None)
        self.silently_fail = kwargs.pop('silently_fail', False)
        self.flat_args = kwargs.pop('flat_args', False)
        self.escape = kwargs.pop('escape', True)
        self.error = None

        for i, arg in enumerate(self.args):
            if isinstance(arg, six.integer_types):
                arg = str(arg)
            if not isinstance(arg, six.string_types):
                raise Exception("Argument {} is invalid: {} is not string types".format(i, arg))

            key_val = arg.split('=')
            if len(key_val) == 2:
                key, val = key_val
                val = val.strip('"').replace('\\"', '"').replace('"', '\\"')
                if ' ' in val:
                    val = '"%s"' % val.replace('\\ ', ' ').replace(' ', '\\ ')
                arg = '%s=%s' % (key, val)
            self.args[i] = arg

    @property
    def is_success(self):
        return not bool(self.error)

    def system_cmd(self, cmd):
        ftmp = tempfile.NamedTemporaryFile(suffix='.out', prefix='tmp', delete=False)
        fpath = ftmp.name
        if os.name=="nt":
            fpath = fpath.replace("/","\\") # forwin
        ftmp.close()
        os.system(cmd + " > " + fpath)
        data = ""
        with open(fpath, 'r') as file:
            data = file.read()
            file.close()
        os.remove(fpath)
        return data
    

    def run(self, log=False):

        if not self.env: self.env = []
        if not isinstance(self.env, list):
            raise Exception("Env arguments are invalid: {} is not list types".format(self.env))

        if isinstance(self.compose, Command.Compose):
            self.env += self.compose.mounting.docker_env       

        self.cmd_line = " ".join(self.env + self.args)

        if '--verbose' in self.args:
            self.cmd_line = self.cmd_line.replace('--verbose', '')
        #  logger.comment(self.cmd_line)

        # if kwargs.get('log', True):
        #     logger.comment("Env.\n" + "\n".join(self.env))

        if isinstance(self.compose, Command.Compose):
            for name, value in self.compose.environment:
                self.cmd_line = self.cmd_line.replace('${%s}' % (name), value)

        if self.is_system:
            self.out = os.system(self.cmd_line)
            # if self.out.startswith('ERROR:'):
            #     self.error = self.out

        else:
            self.lines = []
            self.process = subprocess.Popen(
                self.cmd_line, 
                shell=True, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            self.out = ''

            for line in iter(self.process.stdout.readline, ''):  # replace '' with b'' for Python 3
                self.out += line
                self.lines.append(line.strip())
                self.last_line = line

            self.out = self.out.strip()
            stdout, stderr = self.process.communicate()
            self.error_code = self.process.returncode
            self.error = stderr.decode('utf-8').strip()

        if self.error:                
            # self.error = self.error.replace('docker-machine ls', 'de ls')
            if not self.silently_fail:
                logger.error(self.error)
                exit(0) 

        return self

    def log(self):
        logger.success(self.out)

