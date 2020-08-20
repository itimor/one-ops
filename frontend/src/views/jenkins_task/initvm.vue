<template>
  <div class="app-container">
    <el-card class="box-card">
      <div class="clearfix">
        <span class="title">
          <svg-icon icon-class="base" />创建主机
        </span>
        <sticky :sticky-top="85">
          <div class="action">
            <el-button type="primary" @click="handleCreate">开始初始化</el-button>
          </div>
        </sticky>
      </div>
      <div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form
              ref="dataForm"
              :rules="rules"
              :model="temp"
              label-position="left"
              label-width="120px"
            >
              <el-divider content-position="left" class="heng">填入主机信息</el-divider>
              <template>
                <el-form-item prop="hosts">
                  <el-input v-model="temp.hosts" type="textarea" :autosize="{ minRows: 20, maxRows: 30}"/>
                </el-form-item>
              </template>
            </el-form>
          </el-col>
          <el-col :span="8">
            <div class="grid-content bg-purple">
              <a>123</a>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import { host, idc, hostgroup, auth } from "@/api/all";
import Sticky from "@/components/Sticky";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "aaa",
  components: { Sticky },

  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      temp: {},
      rules: {
        hosts: [{ required: true, message: "请输入名称", trigger: "blur" }],
      },
      temp: {
        hosts: "",
      },
    };
  },
  created() {
    this.getMenuButton();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("aaa")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    handleCreate() {
      console.log(123);
    },
  },
};
</script>
<style lang="scss" scoped>
.box-card {
  .title {
    color: #ed7107;
    font-size: 1.5em;
  }
  .action {
    float: right;
    margin: 2px;
  }
  .heng {
    background-color: #ed7107;
  }
}
</style>