<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="filter-container">
          <el-select
            class="filter-item"
            style="width: 140px;"
            v-model="listQuery.idc"
            filterable
            placeholder="请选择机房"
          >
            <el-option v-for="item in idc_list" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
          <el-select
            class="filter-item"
            style="width: 140px;"
            v-model="listQuery.groups"
            filterable
            placeholder="请选择主机组"
          >
            <el-option
              v-for="item in group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
          <el-button-group>
            <el-button
              class="filter-item"
              type="primary"
              icon="el-icon-search"
              @click="handleFilter"
            >{{ "搜索" }}</el-button>
            <el-button
              :disabled="multipleSelection.length<1"
              class="filter-item"
              type="danger"
              plain
              icon="el-icon-open"
              @click="handleFilter"
            >{{ "init" }}</el-button>
          </el-button-group>
        </div>
        <el-table
          :data="list"
          v-loading="listLoading"
          style="width: 100%"
          highlight-current-row
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="50" />
          <el-table-column label="名称" prop="hostname"></el-table-column>
          <el-table-column label="主IP" prop="ip"></el-table-column>
        </el-table>
      </el-col>
      <el-col :span="16">
        <el-card>
          <div slot="header" class="clearfix">
            <span>日志</span>
            <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
          </div>
          <el-alert title="不可关闭的 alert" type="success" :closable="false"></el-alert>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { host, idc, hostgroup, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "host",

  components: { Pagination },
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      list: [],
      listLoading: true,
      loading: true,
      listQuery: {
        limit: 100,
        status: 0,
        groups: undefined,
        idc: undefined,
      },
      multipleSelection: [],
      temp: {},
      group_list: [],
      idc_list: [],
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
    this.getGroupList();
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
        .requestMenuButton("host")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      host.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.listLoading = false;
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
    handleFilter() {
      this.getList();
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
  },
};
</script>
