import request from '@/utils/request'

export function inithost(data) {
  return request({
    url: '/cmdb/inithost/',
    method: 'post',
    data
  })
}
