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
        self.mounting = kwargs.pop('mounting', None)
        self.silently_fail = kwargs.pop('silently_fail', False)
        self.error = None


    @property
    def is_success(self):
        return not bool(self.error)

    def system_cmd(self, cmd):
        ftmp = tempfile.NamedTemporaryFile(suffix='.out', prefix='tmp', delete=False)
        fpath = ftmp.name
        if os.name=="nt":
            fpath = fpath.replace("/","\\") # forwin
        ftmp.close()
        print(cmd + " > " + fpath)
        os.system(cmd + " > " + fpath)
        data = ""
        with open(fpath, 'r') as file:
            data = file.read()
            file.close()
        os.remove(fpath)
        return data
    

    def run(self, log=False):

        for i, arg in enumerate(self.args):
            if isinstance(arg, six.integer_types):
                self.args[i] = str(arg)
            elif not isinstance(arg, six.string_types):
                raise Exception("Argument {} is invalid: {} is not string types".format(i, arg))

        # if kwargs.get('log', True):
        #     logger.info(" ".join(self.cmd))

        if not self.env: self.env = []
        if not isinstance(self.env, list):
            raise Exception("Env arguments are invalid: {} is not list types".format(self.env))

        if isinstance(self.mounting, Command.Mounting):
            self.env += self.mounting.docker_env       

        self.cmd_line = " ".join(self.env + self.args)

        if '--verbose' in self.args:
            self.cmd_line = self.cmd_line.replace('--verbose', '')
            logger.comment(self.cmd_line)

        # if kwargs.get('log', True):
        #     logger.comment("Env.\n" + "\n".join(self.env))

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


    # def _run(self, cmd, raise_error=True):
    #     """
    #     Run a docker-machine command, optionally raise error if error code != 0
    #     Args:
    #         cmd (List[str]): a list of the docker-machine command with the arguments to run
    #         raise_error (bool): raise an exception on non 0 return code
    #     Returns:
    #         tuple: stdout, stderr, error_code
    #     """
    #     cmd = [self.machine.bin] + cmd
    #     print(" ".join(cmd))

    #     # output = subprocess.check_output(cmd)
    #     # print(output.strip())
    #     # return output

    #     process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     for line in iter(process.stdout.readline, ''):  # replace '' with b'' for Python 3
    #         print(line.strip())

    #     stdout, stderr = process.communicate()
    #     # print(stdout, stderr)
    #     error_code = process.returncode
    #     # if raise_error and error_code:
    #     #     raise RuntimeError("cmd returned error %s: %s" % (error_code, stderr.decode('utf-8').strip()))
    #     return stdout.decode('utf-8'), stderr.decode('utf-8'), error_code


    # def _run_blocking(self, cmd, raise_error=True):
    #     """
    #     Run a docker-machine command, optionally raise error if error code != 0
    #     Args:
    #         cmd (List[str]): a list of the docker-machine command with the arguments to run
    #         raise_error (bool): raise an exception on non 0 return code
    #     Returns:
    #         tuple: stdout, stderr, error_code
    #     """
    #     cmd = [self.machine.bin] + cmd

    #     # output = subprocess.check_output(cmd)
    #     # print(output.strip())
    #     # return output


    #     p = subprocess.open(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     stdout, stderr = p.communicate()
    #     error_code = p.wait()

    #     # if raise_error and error_code:
    #     #     raise RuntimeError("cmd returned error %s: %s" % (error_code, stderr.decode('utf-8').strip()))
    #     return stdout.decode('utf-8'), stderr.decode('utf-8'), error_code