import request from '@/utils/request'

export function userRouter() {
  return request({
    url: '/api/v1/router/',
    method: 'get'
  })
}

