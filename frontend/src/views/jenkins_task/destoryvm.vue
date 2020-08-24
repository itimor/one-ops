<template>
  <div class="app-container">
    <el-card class="box-card">
      <div solt="head" class="clearfix">
        <sticky :sticky-top="85">
          <div class="title">
            <svg-icon icon-class="base" />释放主机
            <el-button
              class="action"
              type="primary"
              icon="el-icon-video-play"
              @click="handleCreate"
            >开始构建</el-button>
          </div>
        </sticky>
      </div>
      <div>
        <el-form
          ref="dataForm"
          :rules="rules"
          :model="temp"
          label-position="left"
          label-width="120px"
        >
          <el-divider content-position="left" class="heng">填入主机信息</el-divider>
          <template>
            <el-input v-model="temp.hosts" type="textarea" :autosize="{ minRows: 20, maxRows: 30}" placeholder="sh-aa-01"/>
          </template>
        </el-form>
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