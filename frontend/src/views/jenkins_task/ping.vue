<template>
  <div class="app-container">
    <el-card class="box-card">
      <div solt="head" class="clearfix">
        <sticky :sticky-top="85">
          <div class="title">
            <svg-icon icon-class="base" />ping测试
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
          <el-divider content-position="left" class="heng">选择参数</el-divider>
          <template>
            <el-form-item prop="num">
              <el-radio-group v-model="temp.num">
                <el-radio :label="10">10</el-radio>
                <el-radio :label="100">100</el-radio>
                <el-radio :label="500">500</el-radio>
              </el-radio-group>
            </el-form-item>
          </template>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { c_jenkins, auth } from "@/api/all";
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
        num: [{ required: true, message: "请输入名称", trigger: "blur" }],
      },
      temp: {
        num: 10,
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
      c_jenkins.ping(this.temp).then((response) => {
        this.$router.push("/tasklog");
      });
    },
  },
};
</script>
<style lang="scss" scoped>
</style>