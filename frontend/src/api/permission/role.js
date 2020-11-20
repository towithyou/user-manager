import request from '@/utils/request'

// 获取所有角色
export function apiGetRoles() {
  return request({
    url: '/api/v1/role/',
    method: 'get'
  })
}

// 创建角色
export function apiCreateRole(data) {
  return request({
    url: '/api/v1/role/',
    method: 'post',
    data
  })
}

// 更新角色
export function apiUpdateRole(data) {
  return request({
    url: '/api/v1/role/' + data['rid'] + '/',
    method: 'put',
    data
  })
}

// 删除角色
export function apiDeleteRole(rid) {
  return request({
    url: '/api/v1/role/' + rid + '/',
    method: 'delete'
  })
}

// 获取所有角色对应的权限
export function apiGetRule() {
  return request({
    url: '/api/v1/permission/',
    method: 'get'
  })
}

// 创建权限
export function apiCreateRule(data) {
  return request({
    url: '/api/v1/permission/',
    method: 'post',
    data
  })
}

// 修改权限
export function apiUpdateRule(data) {
  return request({
    url: '/api/v1/permission/' + data.cid + '/',
    method: 'put',
    data
  })
}

// 删除权限
export function apiDeleteRule(cid) {
  return request({
    url: '/api/v1/permission/' + cid + '/',
    method: 'delete'
  })
}

// 获取用户权限绑定
export function apiGetRoleBind() {
  return request({
    url: '/api/v1/role-bind/',
    method: 'get'
  })
}

// 创建用户权限绑定
export function apiCreateRoleBind(data) {
  return request({
    url: '/api/v1/role-bind/',
    method: 'post',
    data
  })
}

// 更新用户权限绑定
export function apiUpdateRoleBind(data) {
  return request({
    url: '/api/v1/role-bind/' + data.bid + '/',
    method: 'put',
    data
  })
}

// 删除用户权限绑定
export function apiDeleteRoleBind(bid) {
  return request({
    url: '/api/v1/role-bind/' + bid + '/',
    method: 'delete'
  })
}

// 获取角色关联数据
export function apiGetRoleRelated(rid) {
  return request({
    url: '/api/v1/role-related/' + rid + '/',
    method: 'get'
  })
}
