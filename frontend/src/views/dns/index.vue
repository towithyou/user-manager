<template>
  <div class="app-container">
    <h1>DNS管理</h1>
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
import {
  apiGetDns,
  apiPostDns,
  apiPutDns,
  apiDeleteDns
} from '@/api/api-test/backend'

export default {
  name: 'Host',
  methods: {
    createData() {
      apiPostDns().then(() => {
        this.$message({
          message: '创建DNS记录成功',
          type: 'success'
        })
      })
    },
    deleteData() {
      apiDeleteDns().then(() => {
        this.$message({
          message: '删除DNS记录成功',
          type: 'error'
        })
      })
    },
    updateData() {
      apiPutDns().then(() => {
        this.$message({
          message: '更新DNS记录成功',
          type: 'warning'
        })
      })
    },
    getData() {
      apiGetDns().then(() => {
        this.$message({
          message: '获取DNS记录成功',
          type: 'info'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
