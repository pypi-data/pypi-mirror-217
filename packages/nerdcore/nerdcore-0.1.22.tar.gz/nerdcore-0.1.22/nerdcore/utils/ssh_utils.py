import os
import paramiko
from paramiko.config import SSHConfig


def _load_ssh_config():
    ssh_config = SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)
    return ssh_config


class SSHConnection:
    def __init__(self, server_name):
        self.server_name = server_name
        self.ssh_config = _load_ssh_config()
        self.ssh = self._connect()

    def _connect(self):
        cfg = self.ssh_config.lookup(self.server_name)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=cfg['hostname'], username=cfg.get('user'), key_filename=cfg.get('identityfile')[0])
        return ssh

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        return output

    def close(self):
        self.ssh.close()
