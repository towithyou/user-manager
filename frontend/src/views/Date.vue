<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <h1>
          日历
        </h1>
      </div>
      <div>
        <el-calendar v-model="value">
        </el-calendar>
      </div>
    </el-card>
  </div>
</template>

<script>

export default {
  name: 'Test1',
  data() {
    return {
      value: new Date()
    }
  }
}
</script>

<style scoped>
</style>
