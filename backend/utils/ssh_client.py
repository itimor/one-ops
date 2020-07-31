# -*- coding: utf-8 -*-
# author: itimor


import paramiko


class SSHConnection(object):
    def __init__(self, host='192.168.0.111', port=22, username='root', pwd='momo520'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__transport = self.connect()

    def run(self):
        self.connect()  # 连接远程服务器
        self.upload('index.py', '/tmp/1.py')  # 将本地的db.py文件上传到远端服务器的/tmp/目录下并改名为1.py
        self.cmd('ls -l /tmp/1.py')  # 执行df 命令

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        return transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        # result = stdout.read()
        # 循环发送消息
        while True:
            nextline = stdout.readline().strip()  # 读取脚本输出内容
            print(nextline)
            # 判断消息为空时,退出循环
            if not nextline:
                break


if __name__ == '__main__':
    ssh = SSHConnection()
    ssh.run()
    ssh.cmd('ping -c 10 www.google.com')
    ssh.close()  # 关闭连接
