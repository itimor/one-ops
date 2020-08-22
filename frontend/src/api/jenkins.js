import request from '@/utils/request'

export function ping(data) {
  return request({
    url: '/jenkins/task/ping/',
    method: 'post',
    data
  })
}

export function flush() {
  return request({
    url: '/jenkins/tasklog/flush/',
    method: 'get'
  })
}

export function stop(data) {
  return request({
    url: '/jenkins/task/stop/',
    method: 'post',
    data
  })
}