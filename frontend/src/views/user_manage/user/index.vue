<template>
  <div class="app-container">
    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        <span><el-button type="text" size="small" @click="handleCreate">创建</el-button></span>
      </div>
      <el-table
        :data="tableData"
        style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="姓名">
                <span>{{ props.row.username }}</span>
              </el-form-item>
              <el-form-item label="邮箱">
                <span>{{ props.row.email }}</span>
              </el-form-item>
              <el-form-item label="电话">
                <span>{{ props.row.phone }}</span>
              </el-form-item>
              <el-form-item label="简介">
                <span>{{ props.row.introduction }}</span>
              </el-form-item>
              <el-form-item label="部门">
                <span>{{ props.row.department }}</span>
              </el-form-item>
              <el-form-item label="uid">
                <span>{{ props.row.uid }}</span>
              </el-form-item>
              <el-form-item label="创建时间">
                <span>{{ props.row.date_joined }}</span>
              </el-form-item>
              <el-form-item label="是否有效">
                <span>{{ props.row.is_active }}</span>
              </el-form-item>
              <el-form-item label="登录admin后台">
                <span>{{ props.row.is_staff }}</span>
              </el-form-item>
              <el-form-item label="超级管理员">
                <span>{{ props.row.is_superuser }}</span>
              </el-form-item>
              <el-form-item label="角色">
                <span>
                  <el-tag
                    v-for="(role, idx) in props.row.role"
                    :key="idx"
                    style="margin-right: 5px"
                  >{{ role.name }}</el-tag>
                </span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="姓名"
          prop="username">
        </el-table-column>
        <el-table-column
          label="邮箱"
          prop="email">
        </el-table-column>
        <el-table-column
          label="电话"
          prop="phone">
        </el-table-column>
        <el-table-column
          label="部门"
          prop="department">
        </el-table-column>
        <el-table-column
          label="操作"
        >
          <template slot-scope="props">
            <span><el-button type="text" size="small" @click="handleEdit(props.row)">编辑</el-button></span>
            <span style="margin-left: 10px"><el-button type="text" size="small" @click="handleDelete(props.row)">删除</el-button></span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>

</template>

<script>
import { apiDeleteUser, getUsers } from '@/api/user/user-manager'

export default {
  name: 'User',
  data() {
    return {
      tableData: []
    }
  },
  created() {
    this.getUserInfo()
  },
  methods: {
    getUserInfo() {
      getUsers().then(data => {
        this.tableData = data
      }).catch(error => {
        console.log(error)
        this.$notify({
          title: '失败',
          message: '获取用户列表失败',
          type: 'error'
        })
      })
    },
    handleCreate() {
      // this.$router.push({ name: 'userCreate' })
      this.$router.push({ name: 'addUser' })
    },
    handleEdit(row) {
      this.$router.push({
        name: 'editUser',
        params: { uid: row.uid }
        // query: { t: (new Date()) }
      })
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiDeleteUser(row.uid).then((resp) => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getUserInfo()
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
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
