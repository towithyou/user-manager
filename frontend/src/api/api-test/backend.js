import request from '@/utils/request'

export function apiGetHost() {
  return request({
    url: '/api/v1/host/',
    method: 'get'
  })
}

export function apiPostHost() {
  return request({
    url: '/api/v1/host/',
    method: 'post'
  })
}

export function apiPutHost() {
  return request({
    url: '/api/v1/host/',
    method: 'put'
  })
}

export function apiDeleteHost() {
  return request({
    url: '/api/v1/host/',
    method: 'delete'
  })
}

export function apiGetDns() {
  return request({
    url: '/api/v1/dns/',
    method: 'get'
  })
}

export function apiPostDns() {
  return request({
    url: '/api/v1/dns/',
    method: 'post'
  })
}

export function apiPutDns() {
  return request({
    url: '/api/v1/dns/',
    method: 'put'
  })
}

export function apiDeleteDns() {
  return request({
    url: '/api/v1/dns/',
    method: 'delete'
  })
}

