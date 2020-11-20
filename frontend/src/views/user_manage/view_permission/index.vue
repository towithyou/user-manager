<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>前端路由视图</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click="handleClickCreateRouter">添加</el-button>
          </div>
          <el-input
            v-model="filterText"
            clearable
            placeholder="输入关键字进行过滤"
          >
          </el-input>

          <el-tree
            ref="tree"
            class="filter-tree"
            :data="routerViewData"
            :props="defaultProps"
            default-expand-all
            :filter-node-method="filterNode"
            @node-click="handleClickNode"
          >
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card class="box-card" style="">
          <div slot="header" class="clearfix">
            <span>点击左侧路由列表</span>
          </div>
          <div v-if="flag">
            <el-form
              ref="form"
              :rules="dialogFormRules"
              :model="form"
              inline
              label-suffix=":"
              label-position="right"
              label-width="100px"
            >
              <el-form-item label="英文名称" prop="name">
                <el-input v-model="form.name" placeholder="前端组件调用名字"></el-input>
              </el-form-item>
              <el-form-item label="中文名称" prop="alias">
                <el-input v-model="form.alias" placeholder="中文名字"></el-input>
              </el-form-item>
              <el-form-item label="前端路由" prop="path">
                <el-input v-model="form.path" placeholder="前端访问路由"></el-input>
              </el-form-item>
              <el-form-item label="组件路径" prop="component">
                <el-input v-model="form.component" placeholder="layout/index"></el-input>
              </el-form-item>
              <el-form-item label="重定向">
                <el-input v-model="form.redirect"></el-input>
              </el-form-item>
              <el-form-item label="隐藏">
                <el-switch
                  v-model="form.hidden"
                >
                </el-switch>
              </el-form-item>
              <div>
                <el-form-item label="顶级路由">
                  <el-switch
                    v-model="form.isParent"
                  >
                  </el-switch>
                </el-form-item>
              </div>
              <div>
                <el-form-item label="父路由">
                  <el-select
                    v-model="form.parent"
                    placeholder="请选择"
                    :disabled="form.isParent"
                    clearable
                  >
                    <el-option
                      v-for="item in parentRouter"
                      :key="item.router_id + '1'"
                      :label="item.name"
                      :value="item.id">
                    </el-option>
                  </el-select>
                </el-form-item>
              </div>
              <el-form-item label="角色">
                <RoleTransfer
                  :all-role-data="allRole"
                  :bind-roles="bindRoles"
                  @clickMove="handleClickTransfer"
                />
              </el-form-item>
              <el-form-item label="标题" prop="title">
                <el-input
                  v-model="form.title"
                  placeholder="输入标题内容"
                >
                </el-input>
              </el-form-item>
              <el-form-item label="图标" prop="icon">
                <el-input
                  v-model="form.icon"
                  placeholder="Icon 图标"
                >
                </el-input>
              </el-form-item>
              <el-form-item label="固定导航栏">
                <el-switch
                  v-model="form.meta.affix"
                >
                </el-switch>
              </el-form-item>
              <el-form-item label="关闭缓存">
                <el-switch
                  v-model="form.meta.noCache"
                >
                </el-switch>
              </el-form-item>
              <el-form-item label="面包屑显示">
                <el-switch
                  v-model="form.meta.breadcrumb"
                >
                </el-switch>
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="form.remarks"></el-input>
              </el-form-item>
            </el-form>
            <div style="float: right; padding: 3px 0">
              <el-button type="primary" @click="handleClickUpdateRouter">更新</el-button>
              <el-button type="danger" @click="handleClickDeleteRouter">删除</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dialogForm"
        :rules="dialogFormRules"
        :model="dialogForm"
        inline
        label-suffix=":"
        label-position="right"
        label-width="100px"
      >
        <el-form-item label="英文名称" prop="name">
          <el-input v-model="dialogForm.name" placeholder="前端组件调用名字"></el-input>
        </el-form-item>
        <el-form-item label="中文名称" prop="alias">
          <el-input v-model="dialogForm.alias" placeholder="中文名字"></el-input>
        </el-form-item>
        <el-form-item label="前端路由" prop="path">
          <el-input v-model="dialogForm.path" placeholder="前端访问路由"></el-input>
        </el-form-item>
        <el-form-item label="组件路径" prop="component">
          <el-input v-model="dialogForm.component" placeholder="layout/index"></el-input>
        </el-form-item>
        <el-form-item label="重定向">
          <el-input v-model="dialogForm.redirect"></el-input>
        </el-form-item>
        <el-form-item label="隐藏">
          <el-switch
            v-model="dialogForm.hidden"
          >
          </el-switch>
        </el-form-item>
        <div>
          <el-form-item label="顶级路由">
            <el-switch
              v-model="dialogForm.isParent"
            >
            </el-switch>
          </el-form-item>
        </div>
        <div>
          <el-form-item label="父路由">
            <el-select
              v-model="dialogForm.parent"
              placeholder="请选择"
              :disabled="dialogForm.isParent"
              clearable
            >
              <el-option
                v-for="item in parentRouter"
                :key="item.router_id + '1'"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
        </div>
        <el-form-item label="角色">
          <el-select v-model="dialogForm.role" multiple filterable placeholder="请选择" style="width: 400px">
            <el-option
              v-for="item in allRole"
              :key="item.rid"
              :label="item.name"
              :value="item.id"
            >
              <span style="float: left">{{ item.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.alias }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="dialogForm.title"
            placeholder="输入标题内容"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input
            v-model="dialogForm.icon"
            placeholder="Icon 图标"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="固定导航栏">
          <el-switch
            v-model="dialogForm.meta.affix"
          >
          </el-switch>
        </el-form-item>
        <el-form-item label="关闭缓存">
          <el-switch
            v-model="dialogForm.meta.noCache"
          >
          </el-switch>
        </el-form-item>
        <el-form-item label="面包屑显示">
          <el-switch
            v-model="dialogForm.meta.breadcrumb"
          >
          </el-switch>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="dialogForm.remarks"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">关闭</el-button>
        <el-button type="primary" @click="createRouter">提交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { apiDeleteUser, apiGetRoles } from '@/api/user/user-manager'
import {
  apiGetRouterManager,
  apiCreateRouterManager,
  apiUpdateRouterManager,
  apiDeleteRouterManager
} from '@/api/permission/router'
import RoleTransfer from '@/views/user_manage/components/role-transfer'

export default {
  name: 'ViewPerm',
  components: { RoleTransfer },
  data() {
    const validateRole = (rule, value, callback) => {
      console.log(value)
      console.log(rule)
      if (this.dialogFormVisible) {
        console.log(this.dialogForm.role)
      } else {
        console.log(this.form.role)
      }
      if (value.length === 0) {
        callback(new Error('至少选择一个权限'))
      } else {
        callback()
      }
    }

    return {
      filterText: '',
      routerViewData: [],
      defaultProps: {
        children: 'children',
        label: 'alias'
      },
      tableData: [],
      form: {
        meta: {},
        role: []
      },
      dialogForm: {
        meta: {
          affix: false,
          noCache: true,
          breadcrumb: true
        },
        role: [],
        isParent: false
      },
      parentRouter: [],
      allRole: [],
      flag: false,
      textMap: {
        'create': '创建',
        'edit': '编辑'
      },
      dialogStatus: '',
      dialogFormVisible: false,
      dialogFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        alias: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入路径', trigger: 'blur' }
        ],
        component: [
          { required: true, message: '请输入组件路径', trigger: 'blur' }
        ],
        title: [
          { required: true, message: '请输入标题', trigger: 'blur' }
        ],
        icon: [
          { required: true, message: '请输入icon', trigger: 'blur' }
        ],
        role: [
          { required: false, validator: validateRole, triangle: 'change' }
        ]
      },
      bindRoles: []
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    }
  },
  mounted() {
    this.mountedAfter()
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    mountedAfter() {
      this.getRouter()
      this.flag = false
    },
    getRouter() {
      apiGetRouterManager().then(response => {
        this.routerViewData = response
        this.routerViewData.forEach((r) => {
          this.parentRouter.push(r)
        })
        apiGetRoles().then((data) => {
          this.allRole = data
        })
      })
    },
    handleClickNode(data, node, component) {
      this.resetForm()
      var temp = Object.assign({}, data)
      this.form = temp
      console.log(this.form)
      this.form.title = this.form.meta.title
      this.form.icon = this.form.meta.icon
      this.flag = this.flag ? true : !this.flag
      this.bindRoles = this.form.role.map(item => {
        return item.rid
      })
    },
    resetCreateForm() {
      this.dialogForm = {
        meta: {
          affix: false,
          noCache: true,
          breadcrumb: true
        },
        role: [],
        isParent: false
      }
    },
    resetForm() {
      this.form = {
        meta: {
          affix: false,
          noCache: true,
          breadcrumb: true
        },
        role: [],
        isParent: false
      }
    },
    handleClickCreateRouter() {
      console.log('create router')
      this.resetCreateForm()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs.dialogForm.clearValidate()
      })
    },
    createRouter() {
      this.$refs.dialogForm.validate((valid) => {
        if (valid) {
          var title = this.dialogForm.title
          delete this.dialogForm.title
          var icon = this.dialogForm.icon
          delete this.dialogForm.icon
          this.dialogForm.meta.title = title
          this.dialogForm.meta.icon = icon
          console.log(this.dialogForm, 'submit router')
          apiCreateRouterManager(this.dialogForm).then(response => {
            this.$router.go(0)
            this.dialogFormVisible = false
          })
        }
      })
    },
    handleClickTransfer(value, direction, movedKeys) {
      this.bindRoles = value
      var tmp = []
      this.bindRoles.forEach(rid => {
        this.allRole.forEach((item) => {
          if (item.rid === rid) {
            tmp.push(item.id)
          }
        })
      })
      this.form.role = tmp
    },
    handleClickUpdateRouter() {
      var roles = []
      this.form.role.forEach(item => {
        if (typeof item === 'object') {
          roles.push(item.id)
        } else {
          roles.push(item)
        }
      })
      this.form.role = roles
      console.log('update', this.form)
      apiUpdateRouterManager(this.form).then(response => {
        this.$router.go(0)
      })
    },
    handleClickDeleteRouter() {
      console.log('delete', this.form)
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiDeleteRouterManager(this.form.router_id).then(() => {
          this.$router.go(0)
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
