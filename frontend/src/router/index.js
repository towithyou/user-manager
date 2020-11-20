import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: 'Dashboard', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: '个人中心', icon: 'user', noCache: true }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  // 404 page must be placed at the end !!!
  {
    path: '/user',
    component: Layout,
    redirect: '/user/profile',
    name: 'userManage',
    meta: { title: '用户权限管理', icon: 'user', roles: ['admin_role'] },
    children: [
      {
        path: 'profile',
        component: () => import('@/views/user_manage/user/index'),
        name: 'userProfile',
        meta: { title: '用户信息', icon: 'peoples', roles: ['admin_role'] }
      },
      {
        path: 'role',
        component: () => import('@/views/user_manage/role/index'),
        name: 'role',
        meta: { title: '角色管理', icon: 'example', roles: ['admin_role'] }
      },
      {
        path: 'api-permission',
        component: () => import('@/views/user_manage/api_permission/index'),
        name: 'apiPerm',
        meta: { title: 'api权限设置', icon: 'component', roles: ['admin_role'] }
      },
      {
        path: 'view-permission',
        component: () => import('@/views/user_manage/view_permission/index'),
        name: 'viewPerm',
        meta: { title: '视图权限设置', icon: 'eye-open', roles: ['admin_role'] }
      },
      {
        path: 'add',
        component: () => import('@/views/user_manage/user/user-detail/index'),
        name: 'addUser',
        hidden: true,
        meta: { title: '添加用户', icon: 'example', activeMenu: '/user/profile', roles: ['admin_role'] }
      },
      {
        path: 'change/:uid',
        component: () => import('@/views/user_manage/user/user-detail/index'),
        name: 'editUser',
        hidden: true,
        meta: { title: '更改用户', icon: 'eye-open', activeMenu: '/user/profile', roles: ['admin_role'] }
      },
      {
        path: 'role/:rid',
        component: () => import('@/views/user_manage/role/role-related/index'),
        name: 'roleRelated',
        hidden: true,
        meta: { title: '角色关联', icon: 'eye-open', activeMenu: '/user/role', roles: ['admin_role'], noCache: true }
      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
