<template>
  <div style="text-align: center">
    <el-transfer
      v-model="bindData"
      :style="transferStyle"
      filterable
      filter-placeholder="请输入..."
      :left-default-checked="leftChecked"
      :right-default-checked="rightChecked"
      :titles="titles"
      :button-texts="buttonTexts"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
      }"
      :data="transferData()"
      @change="handleChange"
    >
      <span slot-scope="{ option }">
        <el-popover
          placement="right-end"
          :title="option.alias"
          width="200"
          trigger="hover"
          :content="option.remarks"
        >
          <el-button slot="reference" type="text">{{ option.label }}</el-button>
        </el-popover>
      </span>
    </el-transfer>
  </div>
</template>

<script>
export default {
  name: 'RoleTransfer',
  props: {
    allRoleData: {
      type: Array,
      required: true
    },
    bindRoles: {
      type: Array,
      required: true
    },
    noBindRolesChecked: {
      type: Array,
      default() {
        return []
      }
    },
    bindRolesChecked: {
      type: Array,
      default() {
        return []
      }
    },
    transferTitle: {
      type: Array,
      default() {
        return ['所有权限', '已绑定权限']
      }
    },
    transferButtonTexts: {
      type: Array,
      default() {
        return ['移除权限', '添加权限']
      }
    }
  },
  data() {
    return {
      transferStyle: 'text-align: left; display: inline-block',
      transferData: () => {
        const data = []
        for (const role of this.allRoleData) {
          data.push({
            key: role.rid,
            label: role.name,
            alias: role.alias,
            remarks: role.remarks
          })
        }
        return data
      },
      // bindData: this.bindRoles,
      leftChecked: this.noBindRolesChecked,
      rightChecked: this.bindRolesChecked,
      titles: this.transferTitle,
      buttonTexts: this.transferButtonTexts
    }
  },
  computed: {
    bindData: {
      get: function() {
        return this.bindRoles
      },
      set: function(value) {}
    }
  },
  methods: {
    handleChange(value, direction, movedKeys) {
      this.$emit('clickMove', value, direction, movedKeys)
    }
  }
}
</script>

<style scoped>

</style>
