<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button-group>
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="handleFilter"
        >{{ "搜索" }}</el-button>
      </el-button-group>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
    >
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="code" prop="code"></el-table-column>
      <el-table-column label="构建id" prop="build_id">
        <template slot-scope="{ row }">
          <el-tag>#{{row.build_id}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" prop="status">
        <template slot-scope="{ row }">
          <el-tag v-if="row.status==1" type="info">{{row.status|STATUS_TYPEFilter}}</el-tag>
          <el-tag v-if="row.status==2" type="success">{{row.status|STATUS_TYPEFilter}}</el-tag>
          <el-tag v-if="row.status==3">{{row.status|STATUS_TYPEFilter}}</el-tag>
          <el-tag v-if="row.status==4" type="warning">{{row.status|STATUS_TYPEFilter}}</el-tag>
          <el-tag v-if="row.status==5" type="danger">{{row.status|STATUS_TYPEFilter}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="small"
              type="warning"
              @click="handleShowlog(row)"
            >{{ "日志" }}</el-button>
            <el-button
              v-if="permissionList.del && row.status < 3"
              size="small"
              type="danger"
              @click="handleStop(row)"
            >{{ "停止" }}</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.offset"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
    <el-drawer :visible.sync="showlog" :with-header="false" size="30%">
      <div class="showlog" ref="showlog">
        <p v-for="(item, index) in results" :key="index">{{item}}</p>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { tasklog, c_jenkins, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "tasklog",

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
      total: 0,
      listLoading: true,
      listQuery: {
        offset: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
      },
      temp: {},
      showlog: false,
      ws_uri: "/ws/jenkins/",
      results: [],
      socket: null,
      check_job_status: null,
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
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
        .requestMenuButton("tasklog")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      tasklog.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
        const job_status = this.list.map(function (item) {
          return item.status;
        });
        if (job_status.indexOf(1) > -1 || job_status.indexOf(2) > -1) {
          this.check_job_status = setInterval(() => {
            c_jenkins.flush().then((response) => {
              if (response.results.count === 0) {
                this.getList();
                clearInterval(this.check_job_status);
              } else {
                console.log("check job_status 3/s!");
              }
            });
          }, 3000);
        }
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    },
    resetTemp() {
      this.temp = {
        name: "",
        code: "",
        status: 2,
        memo: "",
      };
    },
    handleStop(row) {
      this.temp = row;
      c_jenkins.stop(this.temp).then((response) => {
        console.log(response);
        this.getList();
      });
    },
    scrollToBottom() {
      //  在页面加载时让信息滚动到最下面
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.showlog.scrollTop = this.$refs.showlog.scrollHeight;
        }, 0);
      });
    },
    handleShowlog(row) {
      this.temp = row;
      this.showlog = true;
      this.initWebSocket();
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
    initWebSocket() {
      //初始化weosocket
      try {
        if ("WebSocket" in window) {
          const ws_scheme =
            window.location.protocol == "https:" ? "wss://" : "ws://";
          const ws_host =
            process.env.NODE_ENV === "development"
              ? "127.0.0.1:8000"
              : window.location.host;
          const ws_url = ws_scheme + ws_host + this.ws_uri;

          if (this.socket != null) {
            this.results = [];
            this.socket.close();
          }
          this.socket = new WebSocket(ws_url);
        } else {
          console.log("您的浏览器不支持websocket");
        }
        this.socket.onopen = this.websocketonopen;
        this.socket.onerror = this.websocketonerror;
        this.socket.onmessage = this.websocketonmessage;
        this.socket.onclose = this.websocketclose;
      } catch (e) {
        console.log(e);
        // this.reconnect();
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
      // this.reconnect();
    },
    websocketonmessage(e) {
      //数据接收
      const data = JSON.parse(e.data);
      this.results.push(data["text"]);
      // console.log("得到响应", data);
      // 消息获取成功，重置心跳
      this.scrollToBottom();
    },
    websocketclose(e) {
      //关闭连接
      console.log("ws连接已断开 (" + e.code + ")");
      // this.reconnect();
      // this.getList();
    },
    websocketsend() {
      //数据发送
      this.socket.send(JSON.stringify(this.temp));
    },
  },
};
</script>

<style scoped lang="scss">
.showlog {
  padding: 5px 10px;
  top: 0;
  bottom: 0;
  width: 100%;
  position: fixed;
  overflow: scroll;
  -ms-overflow-style: none;
  overflow: -moz-scrollbars-none;
  &::-webkit-scrollbar {
    width: 0px;
  }
}
</style>