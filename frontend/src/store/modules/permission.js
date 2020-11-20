import { asyncRoutes, constantRoutes } from '@/router'
import { userRouter } from '@/api/user/user-router'
import path from 'path'

/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

// const _import = require('../../router/_import_' + process.env.NODE_ENV)
const _import = require('../../router/_import_development')

export function wrapperRoutes(routers, basePath = '/') {
  const res = []

  routers.forEach(route => {
    const tmp = { ...route }
    // delete tmp.role
    // delete tmp.id
    // delete tmp.is_parent
    // delete tmp.router_id
    // delete tmp.remarks
    // delete tmp.parent
    const asyncRouter = Object.assign({}, tmp)
    asyncRouter.component = _import(tmp.component)
    asyncRouter.path = path.resolve(basePath, asyncRouter.path)
    if (asyncRouter.children) {
      asyncRouter.children = wrapperRoutes(asyncRouter.children, asyncRouter.path)
    }
    res.push(asyncRouter)
  })
  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      // 调用接口获取角色路由
      userRouter().then(response => {
        const dynamicRoutes = wrapperRoutes(response)
        let accessedRoutes
        if (roles.includes('admin_role')) {
          accessedRoutes = asyncRoutes || []
        } else {
          accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
        }
        dynamicRoutes.push(...accessedRoutes)
        // console.log(dynamicRoutes)
        commit('SET_ROUTES', dynamicRoutes)
        resolve(dynamicRoutes)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
