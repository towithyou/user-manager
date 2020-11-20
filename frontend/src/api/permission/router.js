import request from '@/utils/request'

export function apiGetRouterManager() {
  return request({
    url: '/api/v1/router-manager/',
    method: 'get'
  })
}

// 创建
export function apiCreateRouterManager(data) {
  return request({
    url: '/api/v1/router-manager/',
    method: 'post',
    data
  })
}

// 更新
export function apiUpdateRouterManager(data) {
  return request({
    url: '/api/v1/router-manager/' + data.router_id + '/',
    method: 'put',
    data
  })
}

// 删除
export function apiDeleteRouterManager(routerId) {
  return request({
    url: '/api/v1/router-manager/' + routerId + '/',
    method: 'delete'
  })
}
