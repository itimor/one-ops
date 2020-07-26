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
    cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)
    # 实时输出
    while True:
        line = cmd.stdout.readline()
        print(line, end='')
        if line == '' and subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
            break

    return cmd.returncode


if __name__ == '__main__':
    cmd = "ping www.baidu.com"
    print(run_shell(cmd))
