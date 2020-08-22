# -*- coding: utf-8 -*-
# author: itimor

from jenkinsapi.jenkins import Jenkins
import time

jenkins_info = {
    'baseurl': 'http://jenkins.xxoo.com',
    'username': 'admin',
    'password': '11871bd159bd19da9ab624d161c569e3c8'
}
jj = Jenkins(baseurl=jenkins_info['baseurl'], username=jenkins_info['username'], password=jenkins_info['password'])

if __name__ == '__main__':
    job = jj.get_job('ping')
    # print(job_build.stream_logs())
    # for i in job_build.stream_logs():
    #     print(i)
    # job_build.stop()
    # params = {"num": 10}
    # r = job.invoke(build_params=params)
    # print(r)
    # n = 0
    # while True:
    #     time.sleep(2)
    #     n += 1
    #     print('check status %d time' % n)
    #     print(r.is_running())
    #     if r.is_running():
    #         b = r.get_build_number()
    #         print(b)
    #         break

    job_build = job.get_build(int(38))
    b = job_build.is_running()
    print(b)
