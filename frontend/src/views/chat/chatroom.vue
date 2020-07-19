<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <div v-for="item in group_list" :key="item.id">
          <el-button
            style="width:100%;height:100%;text-align: left;"
            type="info"
            plain
            @click="selectGroup(item)"
          >
            <el-avatar>{{item.code}}</el-avatar>
            <a style="height: 300px; margin: 0 auto;">{{item.name}}</a>
          </el-button>
        </div>
      </el-col>
      <el-col :span="16">
        <div>
          <div v-for="item in message_list" :key="item.id">
            <el-avatar>{{item.create_user}}</el-avatar>
            <el-tag>{{item.message}}</el-tag>
          </div>
        </div>
        <hr />
        <div>
          <el-input v-model="temp.message" placeholder="请输入内容" @keyup.enter.native="sendMessage"></el-input>
          <el-button type="success" round @click="sendMessage">发送</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { chatgroup, chatmessage } from "@/api/all";
import { mapGetters } from "vuex";

const heartCheck = {
  timeout: 60 * 1000,
  timer: null,
  serverTimer: null,
  reset() {
    this.timer && clearTimeout(this.timer);
    this.serverTimer && clearTimeout(this.serverTimer);
  },
  start(ws) {
    this.reset();
    this.timer = setTimeout(() => {
      // console.log('发送心跳,后端收到后，返回一个心跳消息')
      // onmessage拿到返回的心跳就说明连接正常
      ws.send(JSON.stringify({ heart: 1 }));
      this.serverTimer = setTimeout(() => {
        // 如果超过一定时间还没响应(响应后触发重置)，说明后端断开了
        ws.close();
      }, this.timeout);
    }, this.timeout);
  }
};

export default {
  name: "chatroom",

  components: {},
  data() {
    return {
      group_list: [],
      message_list: [],
      listQuery: {
        group: undefined
      },
      temp: {
        create_user: "",
        group: "",
        message: ""
      },
      room_name: "",
      ws_uri: "/chat/", // ws path
      lockReconnect: false, // 连接失败不进行重连
      maxReconnect: 5, // 最大重连次数，若连接失败
      socket: null
    };
  },
  computed: {
    ...mapGetters(["user_id"])
  },
  created() {
    this.getGroupList();
  },
  // mounted() {
  //   this.initWebSocket();
  // },
  methods: {
    getGroupList() {
      chatgroup.requestGet().then(response => {
        this.group_list = response.results;
      });
    },
    getMessageList(group_id) {
      const data = {
        group: group_id
      };
      chatmessage.requestGet(data).then(response => {
        this.message_list = response.results;
      });
    },
    selectGroup(row) {
      this.reconnect();
      this.room_name = row.code;
      this.getMessageList(row.id);
      this.initWebSocket();
      this.temp = {
        user_id: this.user_id,
        group_id: row.id,
        message: ""
      };
    },
    sendMessage() {
      this.websocketsend();
      this.temp.message = "";
    },
    reconnect() {
      console.log("尝试重连");
      if (this.lockReconnect || this.maxReconnect <= 0) {
        return;
      }
      setTimeout(() => {
        // this.maxReconnect-- // 不做限制 连不上一直重连
        this.initWebSocket();
      }, 60 * 1000);
    },
    initWebSocket() {
      //初始化weosocket
      try {
        if ("WebSocket" in window) {
          console.log(window.location.protocol);
          const ws_scheme =
            window.location.protocol == "https:" ? "wss://" : "ws://";
          const ws_host =
            process.env.NODE_ENV === "development"
              ? "127.0.0.1:8000"
              : window.location.host;
          const ws_url = ws_scheme + ws_host + this.ws_uri + this.room_name;
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
      heartCheck.start(this.socket);
      // this.socket.send('发送数据')
      // this.websocketsend();
    },
    websocketonerror(e) {
      //连接建立失败重连
      console.log("WebSocket连接发生错误", e);
      this.reconnect();
    },
    websocketonmessage(e) {
      //数据接收
      // console.log(e)
      let data = JSON.parse(e.data);
      console.log("得到响应", data);
      // 消息获取成功，重置心跳
      heartCheck.start(this.socket);
    },
    websocketclose(e) {
      //关闭连接
      console.log("connection closed (" + e.code + ")");
      // this.reconnect();
    },
    websocketsend() {
      //数据发送
      let data = { message: "a1b2c3" };
      this.socket.send(JSON.stringify(this.temp));
    }
  },
  destroyed() {
    this.socket.close(); //离开路由之后断开websocket连接
  }
};
</script>


<style lang="scss" scope>
</style>