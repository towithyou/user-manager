import request from '@/utils/request'

// 获取所有用户
export function getUsers() {
  return request({
    url: '/api/v1/user/',
    method: 'get'
  })
}

// 创建用户
export function apiCreateUser(data) {
  return request({
    url: '/api/v1/user/',
    method: 'post',
    data
  })
}

// 获取用户详细信息
export function apiGetUserDetail(uid) {
  return request({
    url: '/api/v1/user/' + uid + '/',
    method: 'get'
  })
}

// 更新用户信息
export function apiUpdateUser(data) {
  return request({
    url: '/api/v1/user/' + data.uid + '/',
    method: 'put',
    data
  })
}

// 删除用户信息
export function apiDeleteUser(uid) {
  return request({
    url: '/api/v1/user/' + uid + '/',
    method: 'delete'
  })
}

// 获取指定角色id
export function role(id) {
  return request({
    url: '/api/v1/role/' + id + '/',
    method: 'get'
  })
}

// 获取所有角色
export function apiGetRoles() {
  return request({
    url: '/api/v1/role/',
    method: 'get'
  })
}
