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
              @click="handleInithost"
            >{{ "初始化" }}</el-button>
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
            <span style="float: right; padding: 3px 0; color:red;">
              {{tail_log.log_name}}
            </span>
          </div>
          <div v-for="item in results" :key="item.id">
            <el-alert :title="item.text" :type="item.type" :closable="false"></el-alert>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { host, idc, hostgroup, c_cmdb, auth } from "@/api/all";
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
      tail_log: {},
      ws_uri: "/ws/tailf/", // ws path
      lockReconnect: false, // 连接失败不进行重连
      maxReconnect: 5, // 最大重连次数，若连接失败
      socket: null,
      results: [],
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
    this.getGroupList();
    this.getIdcList();
  },
  destroyed() {
    this.socket.close(); //离开路由之后断开websocket连接
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
    handleInithost() {
      const data = {
        hosts: this.multipleSelection.map((x) => {
          return {
            hostname: x.hostname,
            ip: x.ip,
          };
        }),
      };
      c_cmdb.inithost(data).then((response) => {
        this.tail_log = response.results;
        // this.initWebSocket(this.tail_log.log_name);
      });
    },
    scrollToBottom() {
      //  在页面加载时让信息滚动到最下面
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.list_message.scrollTop = this.$refs.list_message.scrollHeight;
        }, 0);
      });
    },
    reconnect() {
      console.log("尝试重连");
      if (this.lockReconnect || this.maxReconnect <= 0) {
        return;
      }
      setTimeout(() => {
        // this.maxReconnect-- // 不做限制
        this.initWebSocket();
      }, 60 * 1000);
    },
    initWebSocket(groupname) {
      //初始化weosocket
      try {
        if ("WebSocket" in window) {
          const ws_scheme =
            window.location.protocol == "https:" ? "wss://" : "ws://";
          const ws_host =
            process.env.NODE_ENV === "development"
              ? "127.0.0.1:8000"
              : window.location.host;
          const ws_url = ws_scheme + ws_host + this.ws_uri + groupname;
          console.log(ws_url);
          this.socket = new WebSocket(ws_url);
        } else {
          console.log("您的浏览器不支持websocket");
        }
        this.socket.onopen = this.websocketonopen;
        this.socket.onerror = this.websocketonerror;
        this.socket.onmessage = this.websocketonmessage;
        this.socket.onclose = this.websocketclose;
      } catch (e) {
        this.reconnect();
      }
    },
    websocketonopen() {
      //连接建立之后执行send方法发送数据
      console.log("WebSocket连接成功", this.socket.readyState);
      this.websocketsend();
    },
    websocketonerror(e) {
      //连接建立失败重连
      console.log("WebSocket连接发生错误", e);
      this.reconnect();
    },
    websocketonmessage(e) {
      //数据接收
      const data = JSON.parse(e.data);
      const result = { text: "null", type: "info" };
      result.text = data["text"];
      if (data["text"].search("INFO") != -1) {
        result.type = "success";
      } else if (data["text"].search("WARNING") != -1) {
        result.type = "warning";
      } else if (data["text"].search("ERROR") != -1) {
        result.type = "error";
      } else {
        result.type = "info";
      }
      console.log(data);
      this.results.push(result);
      // 消息获取成功，重置心跳
      this.scrollToBottom();
    },
    websocketclose(e) {
      //关闭连接
      console.log("ws连接已断开 (" + e.code + ")");
      // this.reconnect();
      this.getList();
    },
    websocketsend() {
      //数据发送
      this.socket.send(JSON.stringify(this.temp));
    },
  },
};
</script>
