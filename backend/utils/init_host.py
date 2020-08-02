# -*- coding: utf-8 -*-
# author: itimor

from utils.ssh_client import SSHConnection
from utils.init_log import Log
import sys
import os

Logger = Log()
log = Logger.Logger


def gogobar(log_path, log_name, hostname, ip, monitor_node=None):
    Logger = Log(log_path, log_name, log_level='INFO')
    log = Logger.Logger
    filename = '{}/{}'.format(log_path, log_name)

    ssh = SSHConnection(host=ip)

    user = 'manager'
    # 新建管理用户，并传输秘钥
    log.info("新建管理用户[%s]" % user)
    ssh.cmd('useradd %s' % user)
    ssh.cmd('mkdir /home/%s/.ssh' % user)
    log.info("传输秘钥")
    ssh.upload('/data/scripts/%s_authorized_keys' % user, '/home/%s/.ssh/authorized_keys' % user)
    ssh.cmd('chmod -R 700 /home/{}/.ssh && chown {}.{} -R /home/{}/.ssh && chmod -R 600 /home/{}/.ssh/authorized_keys'.format(user, user, user, user, user))
    ssh.cmd("grep {} /etc/sudoers || echo '%{}    ALL=(ALL)       NOPASSWD: ALL,!/bin/su,!/usr/bin/passwd' >>/etc/sudoers".format(user, user))
    # 新建普通用户，并传输秘钥
    user = 'view'
    # 新建管理用户，并传输秘钥
    log.info("新建管理用户[%s]" % user)
    ssh.cmd('useradd %s' % user)
    ssh.cmd('mkdir /home/%s/.ssh' % user)
    log.info("传输秘钥")
    ssh.upload('/data/scripts/%s_authorized_keys' % user, '/home/%s/.ssh/authorized_keys' % user)
    ssh.cmd('chmod -R 700 /home/{}/.ssh && chown {}.{} -R /home/{}/.ssh && chmod -R 600 /home/{}/.ssh/authorized_keys'.format(user, user, user, user, user))

    # 加入ansible tmp
    log.info("机器加入ansible")
    shell = 'echo %s >> /usr/local/bfcli/inventory/hosts-tmp' % ip
    os.system(shell)
    # 测试ansible
    log.info("测试目标机器的连通性")
    shell = 'ansible -i /usr/local/bfcli/inventory/hosts-tmp {} -m ping > {}'.format(ip, filename)
    os.system(shell)

    # 传递初始化脚本
    log.info("传递初始化脚本")
    ssh.upload('/data/scripts/os_init.sh', '/root/os_init.sh')
    log.warning("目标机器执行初始化脚本， 此过程耗时较长")
    # ssh.cmd('bash /root/os_init.sh {} {}'.format(hostname, monitor_node))

    ssh.close()


if __name__ == '__main__':
    hostname = sys.argv[1]
    ip = sys.argv[2]
    monitor_node = 'sh'
    log_path = '/tmp'
    log_name = 'aaa.log'
    gogobar(log_path, log_name, hostname, ip, monitor_node)
