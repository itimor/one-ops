# -*- coding: utf-8 -*-
# author: itimor

from jenkinsapi.jenkins import Jenkins

jenkins_info = {
    'baseurl': 'http://jenkins.xxoo.com',
    'username': 'admin',
    'password': '11871bd159bd19da9ab624d161c569e3c8'
}
jj = Jenkins(baseurl=jenkins_info['baseurl'], username=jenkins_info['username'], password=jenkins_info['password'])

if __name__ == '__main__':
    a = jj.get_job('aaa').get_build(6)
    print(a.stream_logs())
    for i in a.stream_logs():
        print(i)
