<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <el-page-header style="float: left; padding: 3px 0" @back="goBack">
        </el-page-header>
      </div>
      <div>
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
          <el-tab-pane name="userInfo">
            <span slot="label"><i class="el-icon-user-solid"></i>用户信息</span>
            <el-table
              :data="userInfo"
              border
              fit
              style="width: 100%">
              <el-table-column
                prop="username"
                label="姓名"
                width="100"
              >
              </el-table-column>
              <el-table-column
                prop="email"
                label="邮箱"
              >
              </el-table-column>
              <el-table-column
                prop="phone"
                label="电话"
              >
              </el-table-column>
              <el-table-column
                prop="department"
                label="部门"
              >
              </el-table-column>
              <el-table-column
                prop="uid"
                label="UID"
                width="300"
              >
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane name="routerView">
            <span slot="label"><i class="el-icon-s-order"></i>前端路由</span>
            <el-table
              :data="routerView"
              border
              fit
              style="width: 100%">
              <el-table-column
                prop="alias"
                label="别名"
              >
              </el-table-column>
              <el-table-column
                prop="path"
                label="路径"
              >
              </el-table-column>
              <el-table-column
                prop="name"
                label="英文名"
              >
              </el-table-column>
              <el-table-column
                prop="component"
                label="组件路径"
              >
              </el-table-column>
              <el-table-column
                prop="router_id"
                label="路由ID"
                width="300"
              >
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane name="permissionRule">
            <span slot="label"><i class="el-icon-s-flag"></i>权限规则</span>
            <el-table
              :data="permissionRule"
              border
              fit
              style="width: 100%">
              <el-table-column
                prop="ptype"
                label="权限类型"
              >
              </el-table-column>
              <el-table-column
                prop="role"
                label="角色名"
              >
              </el-table-column>
              <el-table-column
                prop="path"
                label="api路径"
              >
              </el-table-column>
              <el-table-column
                prop="method"
                label="请求方法"
              >
              </el-table-column>
              <el-table-column
                prop="cid"
                label="规则ID"
                width="300"
              >
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane name="roleBind">
            <span slot="label"><i class="el-icon-position"></i>角色用户绑定</span>
            <el-table
              :data="roleBind"
              border
              fit
              style="width: 100%">
              <el-table-column
                prop="ptype"
                label="权限类型"
              >
              </el-table-column>
              <el-table-column
                prop="role"
                label="角色名"
              >
              </el-table-column>
              <el-table-column
                prop="username"
                label="用户名"
              >
              </el-table-column>
              <el-table-column
                prop="bid"
                label="绑定ID"
                width="300"
              >
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>

  </div>

</template>

<script>
import { apiGetRoleRelated } from '@/api/permission/role'

export default {
  name: 'RoleRelated',
  data() {
    return {
      name: 'role name',
      rid: this.$route.params.rid,
      activeName: 'userInfo',
      userInfo: [],
      routerView: [],
      permissionRule: [],
      roleBind: []
    }
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.getRoleRelated()
    })
  },
  mounted() {
    this.getRoleRelated()
  },
  methods: {
    getRoleRelated() {
      apiGetRoleRelated(this.rid).then((data) => {
        const { user, routerView, permissionRule, roleBind } = data
        this.userInfo = user
        this.routerView = routerView
        this.permissionRule = permissionRule
        this.roleBind = roleBind
      })
    },
    goBack() {
      console.log('go back')
      this.$router.push({ name: 'role' })
    },
    handleClick(tab, event) {
      // console.log(tab, event)
    }
  }
}
</script>

<style scoped>

</style>
