import request from '@/utils/request'

export function userLogin(data) {
  return request({
    url: '/api-token-auth/',
    method: 'post',
    data
  })
}

export function getUserProfile(params) {
  return request({
    url: '/api/v1/user-profile/',
    method: 'get',
    params
  })
}

