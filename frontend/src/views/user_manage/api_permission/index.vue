<template>
  <div class="app-container">
    <el-tabs type="border-card">
      <el-tab-pane label="角色权限规则">
        <div>
          <div slot="header" class="clearfix">
            <el-button type="primary" icon="el-icon-edit" @click="handleCreateRule">创建</el-button>
          </div>
          <el-table
            :data="tableData"
            fit
            style="width: 100%">
            <el-table-column
              prop="ptype"
              label="权限类型"
              width="100">
            </el-table-column>
            <el-table-column
              prop="role"
              label="角色">
            </el-table-column>
            <el-table-column
              prop="path"
              label="api路径">
            </el-table-column>
            <el-table-column
              prop="method"
              label="请求方法"
              width="100"
            >
            </el-table-column>
            <el-table-column
              prop="id"
              label="数据库ID"
              width="100"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              align="right"
              width="180"
            >
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="small"
                  @click="handleEditClickRule(scope.row)"
                >编辑
                </el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="small"
                  circle
                  @click="handleDeleteClickRule(scope.row)"
                >删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
      <el-tab-pane>
        <span slot="label">
          <i class="el-icon-user">用户权限绑定</i>
        </span>
        <div>
          <div slot="header" class="clearfix">
            <el-button type="success" icon="el-icon-edit" @click="handleCreateRuleBind">创建</el-button>
          </div>
          <el-table
            :data="ruleBindData"
            fit
            style="width: 100%">
            <el-table-column
              prop="ptype"
              label="权限类型"
            >
            </el-table-column>
            <el-table-column
              prop="username"
              label="用户名"
            >
            </el-table-column>
            <el-table-column
              prop="role"
              label="role"
            >
            </el-table-column>
            <el-table-column
              prop="id"
              label="数据库ID"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              align="right"
            >
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  circle
                  size="small"
                  @click="handleEditClickUserBind(scope.row)"
                >编辑
                </el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="small"
                  circle
                  @click="handleDeleteClickUserBind(scope.row)"
                >删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="90px"
        style="margin-left:50px;"
      >
        <el-form-item label="角色" prop="role">
          <el-select v-model="temp.role" filterable clearable placeholder="请输入角色名称">
            <el-option
              v-for="item in roles"
              :key="item.rid"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="api路径" prop="path">
          <el-input v-model="temp.path" placeholder="请输入API路径"/>
        </el-form-item>
        <el-form-item label="请求方法" prop="method">
          <el-select v-model="temp.method" clearable placeholder="请选择">
            <el-option
              v-for="item in HttpMethod"
              :key="item.value"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">关闭</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createRule():updateRule()">提交</el-button>
      </div>
    </el-dialog>
    <!--  用户权限绑定  -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="userBindDialogVisible">
      <el-form
        ref="userBindDataForm"
        :rules="userBindRules"
        :model="bindTemp"
        label-position="left"
        label-width="90px"
        style="margin-left:50px;"
      >
        <el-form-item label="用户名" prop="username">
          <el-select v-model="bindTemp.username" filterable clearable placeholder="请选择">
            <el-option
              v-for="item in users"
              :key="item.uid"
              :label="item.username"
              :value="item.username">
              <span style="float: left; width: 120px">{{ item.username }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.email }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="bindTemp.role" filterable clearable placeholder="请选择">
            <el-option
              v-for="item in roles"
              :key="item.rid"
              :label="item.alias"
              :value="item.name">
              <span style="float: left;">{{ item.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.remarks }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="userBindDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createUserBind():updateUserBind()">提交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  apiGetRoles,
  apiGetRule,
  apiCreateRule,
  apiUpdateRule,
  apiDeleteRule,
  apiGetRoleBind,
  apiCreateRoleBind,
  apiUpdateRoleBind,
  apiDeleteRoleBind
} from '@/api/permission/role'

import { getUsers } from '@/api/user/user-manager'

export default {
  name: 'ApiView',
  data() {
    return {
      tableData: [],
      ruleBindData: [],
      dialogFormVisible: false,
      userBindDialogVisible: false,
      textMap: {
        'create': '创建',
        'edit': '编辑'
      },
      dialogStatus: '',
      temp: {
        ptype: 'p',
        role: '',
        alias: '',
        remarks: ''
      },
      bindTemp: {
        ptype: 'g',
        username: '',
        role: ''
      },
      rules: {
        role: [
          { required: true, message: '请输入角色名称', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入API路径', trigger: 'blur' }
        ],
        method: [
          { required: true, message: '请选择请求方法', trigger: 'change' }
        ]
      },
      userBindRules: {
        role: [
          { required: true, message: '请输入角色名称', trigger: 'change' }
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'change' }
        ]
      },
      users: [],
      roles: [],
      HttpMethod: [{
        value: 'GET',
        label: '查'
      }, {
        value: 'POST',
        label: '增'
      }, {
        value: 'DELETE',
        label: '删'
      }, {
        value: 'PUT',
        label: '改'
      }, {
        value: '*',
        label: '增删改查'
      }, {
        value: '(GET|POST)',
        label: '增查'
      }, {
        value: '(GET|DELETE)',
        label: '删查'
      }, {
        value: '(GET|PUT)',
        label: '查改'
      }, {
        value: '(GET|POST|DELETE)',
        label: '查增删'
      }, {
        value: '(GET|POST|PUT)',
        label: '查增改'
      }, {
        value: '(POST|PUT)',
        label: '增改'
      }, {
        value: '(POST|DELETE)',
        label: '增删'
      }, {
        value: '(PUT|DELETE)',
        label: '改删'
      }
      ],
      value: ''
    }
  },
  mounted() {
    this.getRoleRule()
    this.getRoles()
    this.handleClickBindTab()
  },
  methods: {
    resetTemp() {
      this.temp = { ptype: 'p' }
      this.bindTemp = { ptype: 'g' }
    },
    handleCreateRule() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs.dataForm.clearValidate()
      })
    },
    getRoleRule() {
      apiGetRule().then(response => {
        this.tableData = response
      })
    },
    handleEditClickRule(row) {
      console.log('edit rule')
      this.resetTemp()
      this.dialogStatus = 'edit'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs.dataForm.clearValidate()
      })
      this.temp = Object.assign({}, row)
    },
    handleDeleteClickRule(row) {
      console.log('delete rule')
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiDeleteRule(row.cid).then(response => {
          this.$notify({
            title: '删除',
            message: '删除成功',
            type: 'success',
            duration: 5000
          })
          this.getRoleRule()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    createRule() {
      this.$refs.dataForm.validate((valid) => {
        if (valid) {
          console.log('create rule', this.temp)
          apiCreateRule(this.temp).then(response => {
            this.$notify({
              title: '创建权限',
              message: '创建成功',
              type: 'success',
              duration: 5000
            })
            this.getRoleRule()
            this.dialogFormVisible = false
          }).catch(error => {
            console.log(error.response)
          })
        }
      })
    },
    updateRule() {
      this.$refs.dataForm.validate((valid) => {
        if (valid) {
          apiUpdateRule(this.temp).then(response => {
            this.$notify({
              title: '更新',
              message: '更新成功',
              type: 'success',
              duration: 5000
            })
            this.getRoleRule()
            this.dialogFormVisible = false
          })
        }
      })
    },
    getRoles() {
      apiGetRoles().then(response => {
        this.roles = response
      })
    },
    handleCreateRuleBind() {
      console.log('rule bind')
      this.resetTemp()
      this.dialogStatus = 'create'
      this.userBindDialogVisible = true
      this.$nextTick(() => {
        this.$refs.userBindDataForm.clearValidate()
      })
    },
    handleClickBindTab() {
      // console.log('click tab', tab)
      apiGetRoleBind().then((response) => {
        this.ruleBindData = response
      })
      getUsers().then(response => {
        this.users = response
      })
    },
    createUserBind() {
      this.$refs.userBindDataForm.validate((valid) => {
        if (valid) {
          apiCreateRoleBind(this.bindTemp).then(response => {
            this.$notify({
              title: '创建绑定',
              message: '创建用户角色绑定成功',
              type: 'success',
              duration: 5000
            })
            this.handleClickBindTab()
            this.userBindDialogVisible = false
          }).catch(error => {
            console.log(error.response)
          })
        }
      })
    },
    updateUserBind() {
      this.$refs.userBindDataForm.validate((valid) => {
        if (valid) {
          console.log(this.bindTemp)
          apiUpdateRoleBind(this.bindTemp).then(response => {
            this.$notify({
              title: '更新',
              message: '更新绑定成功',
              type: 'success',
              duration: 5000
            })
            this.handleClickBindTab()
            this.userBindDialogVisible = false
          }).catch(error => {
            console.log(error.response)
          })
        }
      })
    },
    handleEditClickUserBind(row) {
      console.log('edit bind')
      this.resetTemp()
      this.dialogStatus = 'edit'
      this.userBindDialogVisible = true
      this.$nextTick(() => {
        this.$refs.userBindDataForm.clearValidate()
      })
      this.bindTemp = Object.assign({}, row)
    },
    handleDeleteClickUserBind(row) {
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiDeleteRoleBind(row.bid).then(response => {
          apiGetRoleBind().then((response) => {
            this.ruleBindData = response
          })
          this.$notify({
            title: '删除',
            message: '删除成功',
            type: 'success',
            duration: 5000
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
