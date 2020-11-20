<template>
  <div class="app-container">
    <el-card class="box-card" style="">
      <div slot="header" class="clearfix">
        <el-button type="primary" icon="el-icon-edit" @click="handleCreateRole">创建</el-button>
      </div>
      <el-table
        :data="tableData"
        fit
        style="width: 100%">
        <el-table-column
          prop="rid"
          label="ID"
          width="300">
        </el-table-column>
        <el-table-column
          prop="name"
          label="名称"
        >
        </el-table-column>
        <el-table-column
          prop="alias"
          label="别名">
        </el-table-column>
        <el-table-column
          prop="remarks"
          label="备注">
        </el-table-column>
        <el-table-column
          label="操作"
          align="right"
          width="300"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-view"
              @click="handleDetailClick(scope.row)"
            >查看
            </el-button>
            <el-button
              type="primary"
              icon="el-icon-edit"
              circle
              size="small"
              @click="handleEditClick(scope.row)"
            >编辑
            </el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="small"
              circle
              @click="handleDeleteClick(scope.row)"
            >删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="90px"
        style="margin-left:50px;"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" placeholder="请输入英文名称"/>
        </el-form-item>
        <el-form-item label="别名" prop="alias">
          <el-input v-model="temp.alias" placeholder="请输入别名"/>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="temp.remarks"
            :autosize="{ minRows: 2, maxRows: 4}"
            type="textarea"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">关闭</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">提交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import { apiGetRoles, apiCreateRole, apiUpdateRole, apiDeleteRole } from '@/api/permission/role'

export default {
  name: 'Role',
  data() {
    const validateName = (rule, value, callback) => {
      if (value === undefined || value === '') {
        callback(new Error('请输入角色名'))
      } else if (!value.endsWith('_role')) {
        callback(new Error('用户名必须以_role结尾'))
      } else {
        callback()
      }
    }
    return {
      tableData: [],
      dialogFormVisible: false,
      textMap: {
        'create': '创建',
        'edit': '编辑'
      },
      dialogStatus: '',
      temp: {
        name: '',
        alias: '',
        remarks: ''
      },
      updateTemp: {},
      rules: {
        name: [
          { required: true, trigger: 'blur', validator: validateName }
        ],
        alias: [
          { required: true, message: '请输入角色别名', trigger: 'blur' }
        ],
        remarks: [
          { required: true, message: '请输入备注', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.getRoles()
  },
  methods: {
    resetTemp() {
      this.temp = {}
    },
    getRoles() {
      apiGetRoles().then(response => {
        this.tableData = response
      })
    },
    handleCreateRole() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs.dataForm.clearValidate()
      })
    },
    createData() {
      console.log('create data', this.temp)
      this.$refs.dataForm.validate((valid) => {
        if (valid) {
          apiCreateRole(this.temp).then(response => {
            this.$notify({
              title: '创建OK',
              message: '创建成功',
              type: 'success',
              duration: 5000
            })
            this.getRoles()
            this.dialogFormVisible = false
          })
        }
      })
    },
    updateData() {
      this.$refs.dataForm.validate((valid) => {
        if (valid) {
          apiUpdateRole(this.temp).then(response => {
            this.$notify({
              title: '更新',
              message: '更新成功',
              type: 'success',
              duration: 5000
            })
            this.getRoles()
            this.dialogFormVisible = false
          })
        }
      })
    },
    handleEditClick(row) {
      this.resetTemp()
      this.dialogStatus = 'edit'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs.dataForm.clearValidate()
      })
      this.temp = Object.assign({}, row)
    },
    handleDeleteClick(row) {
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiDeleteRole(row.rid).then(response => {
          this.$notify({
            title: '删除',
            message: '删除成功',
            type: 'success',
            duration: 5000
          })
          this.getRoles()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    handleDetailClick(row) {
      this.$router.push({
        name: 'roleRelated',
        params: { rid: row.rid }
      })
    }
  }
}
</script>

<style scoped>

</style>
