# -*- coding: utf-8 -*-
# author: itimor

import subprocess
import sys


# def run_shell(shell):
#     cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
#                            stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
#     cmd.communicate()
#     return cmd.returncode

def run_shell(shell):
    shell = '{} {}'.format(shell, '2>&1')
    cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)

    return cmd


if __name__ == '__main__':
    cmd = "ping www.google.com"
    a = run_shell(cmd)
    while True:
        line = a.stdout.readline()
        print(line, end='')
        if line == '' or a.poll() is not None:  # 判断子进程是否结束
            break
