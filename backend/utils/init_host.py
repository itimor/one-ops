# -*- coding: utf-8 -*-
# author: itimor

from ssh_client import SSHConnection
import sys
import os


def gogobar():
    # 新建管理用户，并传输秘钥
    ssh.cmd('useradd manager')
    ssh.cmd('mkdir /home/manager/.ssh')
    ssh.upload('/data/scripts/manager_authorized_keys', '/home/manager/.ssh/authorized_keys')
    ssh.cmd('chmod -R 700 /home/manager/.ssh && chown manager.manager -R /home/manager/.ssh && chmod -R 600 /home/manager/.ssh/authorized_keys')
    ssh.cmd("grep manager /etc/sudoers || echo '%manager    ALL=(ALL)       NOPASSWD: ALL,!/bin/su,!/usr/bin/passwd' >>/etc/sudoers")

    # 新建查看用户，并传输秘钥
    ssh.cmd('useradd view')
    ssh.cmd('mkdir /home/view/.ssh')
    ssh.upload('/data/scripts/view_authorized_keys', '/home/view/.ssh/authorized_keys')
    ssh.cmd('chmod -R 700 /home/view/.ssh && chown view.view -R /home/view/.ssh && chmod -R 600 /home/view/.ssh/authorized_keys')

    # 传递初始化脚本
    ssh.upload('/data/scripts/os_init.sh', '/root/os_init.sh')
    ssh.cmd('bash /root/os_init.sh {} {}'.format(hostname, monitor_node))

    # 加入ansible tmp
    shell = 'echo {}>>/data/scripts/wahaha/inventory/hosts-tmp'.format(ip)
    os.system(shell)
    # 测试ansible
    shell = 'ansible -i /data/scripts/wahaha/inventory/hosts-tmp {} -m ping'.format(ip)
    os.system(shell)


if __name__ == '__main__':
    hostname = sys.argv[1]
    ip = sys.argv[2]
    monitor_node = 'sh'
    ssh = SSHConnection(host=ip)
    gogobar()
    ssh.close()
