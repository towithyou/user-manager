<template>
  <div class="app-container">
    <h1>主机管理</h1>
    <div>
      <el-button style="margin:10px 5px 15px 20px;" type="primary" round @click="createData">增</el-button>
    </div>
    <div>
      <el-button style="margin:10px 5px 15px 20px;" type="danger" round @click="deleteData">删</el-button>
    </div>
    <div>
      <el-button style="margin:10px 5px 15px 20px;" type="warning" round @click="updateData">改</el-button>
    </div>
    <div>
      <el-button style="margin:10px 5px 15px 20px;" type="success" round @click="getData">查</el-button>
    </div>

  </div>
</template>

<script>

import { apiGetHost, apiPostHost, apiPutHost, apiDeleteHost } from '@/api/api-test/backend'

export default {
  name: 'Host',
  methods: {
    createData() {
      apiPostHost().then(() => {
        this.$message({
          message: '创建DNS记录成功',
          type: 'success'
        })
      })
    },
    deleteData() {
      apiDeleteHost().then(() => {
        this.$message({
          message: '删除主机成功',
          type: 'error'
        })
      })
    },
    updateData() {
      apiPutHost().then(() => {
        this.$message({
          message: '更新主机成功',
          type: 'warning'
        })
      })
    },
    getData() {
      apiGetHost().then(() => {
        this.$message({
          message: '获取主机成功',
          type: 'info'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
