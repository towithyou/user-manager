<template>
  <div class="app-container">
    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        {{ title }}
      </div>
      <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="auto" class="demo-ruleForm">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="ruleForm.username"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="ruleForm.email"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="ruleForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="ruleForm.password"></el-input>
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="ruleForm.department"></el-input>
        </el-form-item>
        <el-form-item label="登录admin后台">
          <el-switch
            v-model="ruleForm.is_staff"
            active-color="#13ce66"
            inactive-color="#CCCCCC">
          </el-switch>
        </el-form-item>
        <el-form-item label="激活">
          <el-switch
            v-model="ruleForm.is_active"
            active-color="#13ce66"
            inactive-color="#CCCCCC">
          </el-switch>
        </el-form-item>
        <el-form-item label="超级管理员">
          <el-switch
            v-model="ruleForm.is_superuser"
            active-color="#13ce66"
            inactive-color="#CCCCCC">
          </el-switch>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <RoleTransfer
            :all-role-data="allRole"
            :bind-roles="bindRoles"
            @clickMove="handleClickTransfer"
          />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="ruleForm.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 6}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="uid ? handleClickUpdate(): handleClickCreate()">
            {{ uid ? '更新' : '创建' }}
          </el-button>
          <span v-show="!uid" style="margin-left: 10px"><el-button @click="resetForm('ruleForm')">重置</el-button></span>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>

import { apiGetRoles, apiCreateUser, apiGetUserDetail, apiUpdateUser } from '@/api/user/user-manager'
import RoleTransfer from '@/views/user_manage/components/role-transfer'

export default {
  name: 'CreateUser',
  components: { RoleTransfer },
  data() {
    const validateRole = (rule, value, callback) => {
      if (value.length === 0) {
        callback(new Error('至少选择一个权限'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (this.uid === undefined) {
        // 创建
        if (value.length === 0) {
          callback(new Error('创建用户必须输入密码'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }

    return {
      title: this.$route.meta.title,
      uid: this.$route.params.uid,
      ruleForm: {
        username: '',
        email: '',
        phone: '',
        password: '',
        department: '',
        introduction: '',
        is_staff: false,
        is_active: true,
        is_superuser: false,
        role: []
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入电话', trigger: 'blur' }
        ],
        password: [
          { required: true, trigger: 'blur', validator: validatePassword }
        ],
        department: [
          { required: true, message: '请输入部门', trigger: 'blur' }
        ],
        role: [
          { required: true, trigger: 'blur', validator: validateRole }
        ]
      },
      allRole: [],
      bindRoles: [],
      noBindRoles: []
    }
  },
  mounted() {
    this.getRoles()
    this.getUserDetail()
  },
  beforeRouteEnter(to, from, next) {
    // 不能调用this 上面的内容
    // to.meta.title = to.params.uid ? '更新' : '创建'
    next(vm => {
      vm.getRoles()
    })
  },
  beforeRouteUpdate(to, from, next) {
    // 当路由发生改变，会触发，比如 /app/1 /app/2
    next()
  },
  beforeRouteLeave(to, from, next) {
    // console.log('user detail beforeRouteLeave')
    next()
  },
  methods: {
    getRoles() {
      apiGetRoles().then((data) => {
        this.allRole = data
      })
    },
    getUserDetail() {
      console.log('user detail')
      if (this.uid === undefined) {
        return
      }

      apiGetUserDetail(this.uid).then(data => {
        Object.keys(data).forEach(item => {
          this.ruleForm[item] = data[item]
        })
        this.bindRoles = data.role.map(item => {
          return item.rid
        })
        this.ruleForm.role = this.bindRoles
      })
    },
    handleClickTransfer(value, direction, movedKeys) {
      this.bindRoles = value
      this.noBindRoles = this.allRole.filter((role) => {
        return !this.bindRoles.includes(role.rid)
      })
      this.ruleForm.role = this.bindRoles
    },
    resetForm(formName) {
      this.$nextTick(() => {
        this.$refs[formName].resetFields()
        this.ruleForm = {
          username: '',
          email: '',
          phone: '',
          password: '',
          department: '',
          introduction: '',
          is_staff: false,
          is_active: true,
          is_superuser: false,
          role: []
        }
        this.bindRoles = []
      })
    },
    handleClickCreate() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          console.log('create', this.ruleForm)
          apiCreateUser(this.ruleForm).then(response => {
            console.log(response)
            this.$router.push({ name: 'userProfile' })
          }).catch(error => {
            console.log(error)
          })
        }
      })
    },
    handleClickUpdate() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          console.log('update')
          var temp = Object.assign({}, this.ruleForm)
          delete temp.date_joined
          if (temp.password === '') {
            delete temp.password
          }
          apiUpdateUser(temp).then(response => {
            console.log('update ok', response)
            this.$router.push({ name: 'userProfile' })
          }).catch(error => {
            console.log('update error', error)
            this.$notify.error({
              title: '失败',
              message: error
            })
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
