<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="title" v-if="active==1">
          <svg-icon icon-class="base" />
          {{namemarks[active]}}
        </span>
        <span class="title" v-if="active==2">
          <svg-icon icon-class="spec" />
          {{namemarks[active]}}
        </span>
        <span class="title" v-if="active==3">
          <svg-icon icon-class="network" />
          {{namemarks[active]}}
        </span>
        <div class="action">
          <el-button type="primary" @click="backStep">上一步</el-button>
          <el-button v-if="active<3" type="success" @click="nextStep">下一步</el-button>
          <el-button v-else type="danger" @click="nextStep">开始创建</el-button>
        </div>
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
              <template v-if="active==1">
                <el-form-item label="主机名" prop="hostname">
                  <el-input v-model="temp.hostname" />
                </el-form-item>
                <el-form-item label="机房" prop="idc">
                  <el-select v-model="temp.idc" filterable placeholder="请选择机房">
                    <el-option
                      v-for="item in idc_list"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="类型" prop="asset_type">
                  <el-select v-model="temp.asset_type" filterable placeholder="请选择设备类型">
                    <el-option
                      v-for="(label, value) in ASSET_TYPE"
                      :key="value"
                      :label="label"
                      :value="value"
                    ></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="系统" prop="os">
                  <el-select v-model="temp.os" filterable placeholder="请选择系统版本">
                    <el-option
                      v-for="(label, value) in OS_TYPE"
                      :key="value"
                      :label="label"
                      :value="value"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </template>
              <template v-if="active==2">
                <el-form-item label="所在vcenter" prop="vcenter">
                  <el-input v-model="temp.vcenter" />
                </el-form-item>
                <el-form-item label="所在datastore" prop="datastore">
                  <el-input v-model="temp.datastore" />
                </el-form-item>
                <el-form-item label="ip" prop="ip">
                  <el-input v-model="temp.ip" />
                </el-form-item>
                <el-form-item label="子网掩码" prop="netmask">
                  <el-input v-model="temp.netmask" />
                </el-form-item>
                <el-form-item label="网关" prop="gateway">
                  <el-input v-model="temp.gateway" />
                </el-form-item>
                <el-form-item label="dns" prop="dns">
                  <el-input v-model="temp.dns" />
                </el-form-item>
              </template>
              <template v-if="active==3">
                <el-form-item label="cpu个数" prop="cpu_num">
                  <el-slider
                    v-model="temp.cpu_num"
                    :min="2"
                    :max="16"
                    :step="1"
                    :marks="cpumarks"
                    show-input
                  ></el-slider>
                </el-form-item>
                <el-form-item label="内存大小" prop="memory">
                  <el-slider
                    v-model="temp.memory"
                    :min="4"
                    :max="64"
                    :step="4"
                    :marks="memmarks"
                    show-input
                  ></el-slider>
                </el-form-item>
                <el-form-item label="系统磁盘" prop="sys_disk">
                  <el-slider
                    v-model="temp.sys_disk"
                    :min="300"
                    :max="2000"
                    :step="100"
                    :marks="diskmarks"
                    show-input
                  ></el-slider>
                </el-form-item>
                <el-form-item label="数据磁盘" prop="data_disk">
                  <el-slider
                    v-model="temp.data_disk"
                    :min="300"
                    :max="2000"
                    :step="100"
                    :marks="diskmarks"
                    show-input
                  ></el-slider>
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

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "aaa",
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
        hostname: [{ required: true, message: "请输入名称", trigger: "blur" }],
        idc: [{ required: true, message: "请输入code", trigger: "blur" }],
        vcenter: [{ required: true, message: "请输入code", trigger: "blur" }],
        datastore: [{ required: true, message: "请输入code", trigger: "blur" }],
        ip: [{ required: true, message: "请输入code", trigger: "blur" }],
        netmask: [{ required: true, message: "请输入code", trigger: "blur" }],
        gateway: [{ required: true, message: "请输入code", trigger: "blur" }],
        dns: [{ required: true, message: "请输入code", trigger: "blur" }],
      },
      ASSET_TYPE: {
        1: "物理机",
        2: "虚拟机",
        3: "容器",
        4: "网络设备",
        5: "其他设备",
      },
      OS_TYPE: {
        1: "centos",
        2: "windows",
        3: "debian",
        4: "other",
      },
      idc_list: [],
      cpumarks: {
        2: "2核",
        4: "4核",
        8: "8核",
        12: "12核",
        16: "16",
      },
      memmarks: {
        4: "4G",
        8: "8G",
        16: "16G",
        24: "24G",
        32: "32G",
        48: "48G",
        64: "64",
      },
      diskmarks: {
        300: "300G",
        500: "500G",
        800: "800G",
        1000: "1T",
        1500: "1.5T",
        2000: "2",
      },
      active: 1,
      namemarks: {
        1: "基础配置",
        2: "网络配置",
        3: "规格配置",
        4: "完成",
      },
      temp: {
        hostname: "sh-aa-01",
        ip: "192.168.0.111",
        other_ip: null,
        have_net: false,
        netmask: "255.255.255.0",
        gateway: null,
        dns: null,
        vcenter: null,
        os: "1",
        cpu: null,
        cpu_num: "2",
        memory: "4",
        sys_disk: "300",
        data_disk: "300",
        other_disk: null,
        datastore: null,
        asset_type: "2",
        status: 1,
        memo: "",
      },
    };
  },
  created() {
    this.getMenuButton();
    this.getIdcList();
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
    getGroupList() {
      hostgroup.requestGet().then((response) => {
        this.group_list = response.results;
      });
    },
    getIdcList() {
      idc.requestGet().then((response) => {
        this.idc_list = response.results;
      });
    },
    backStep() {
      if (this.active-- < 1) this.active = 1;
    },
    nextStep() {
      if (this.active++ > 2) this.active = 1;
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
}
</style>