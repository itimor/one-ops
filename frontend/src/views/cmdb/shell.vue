<template>
  <div class="chat-app">
    <div style="margin-top: 15px;">
      <el-input placeholder="请输入内容" v-model="temp.cmd">
        <el-button slot="append" icon="el-icon-open" @click="cmdrun"></el-button>
      </el-input>
    </div>
  </div>
</template>

<script>
import { history } from "@/api/all";
import { mapGetters } from "vuex";

export default {
  name: "shell",

  components: {  },
  data() {
    return {
      listQuery: {
        search: "",
        join_user: "",
        group: undefined
      },
      temp: {
        cmd: "ping www.baidu.com"
      },
      ws_uri: "/ws/shell/123", // ws path
      lockReconnect: false, // 连接失败不进行重连
      maxReconnect: 5, // 最大重连次数，若连接失败
      socket: null
    };
  },
  computed: {
    ...mapGetters(["user_id"])
  },
  created() {
  },
  methods: {
    cmdrun(){
      const date = new Date()
      const m = date.getMinutes() + 1 < 10 ? '0' + date.getMinutes() : date.getMinutes()
      const s = date.getSeconds() + 1 < 10 ? '0' + date.getSeconds() : date.getSeconds()
      const ms = date.getMilliseconds().toString().length < 3 ? '0' + date.getMilliseconds() : date.getMilliseconds()
      const groupname = m + '-' + s + '-' + ms
      this.initWebSocket(groupname);
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
      heartCheck.start(this.socket);
    },
    websocketonerror(e) {
      //连接建立失败重连
      console.log("WebSocket连接发生错误", e);
      this.reconnect();
    },
    websocketonmessage(e) {
      //数据接收
      const data = JSON.parse(e.data);
      this.message_list.push(data);
      // console.log("得到响应", data);
      // 消息获取成功，重置心跳
      this.scrollToBottom();
      heartCheck.start(this.socket);
    },
    websocketclose(e) {
      //关闭连接
      console.log("ws连接已断开 (" + e.code + ")");
      this.reconnect();
    },
    websocketsend() {
      //数据发送
      this.socket.send(JSON.stringify(this.temp));
    }
  },
  destroyed() {
    this.socket.close(); //离开路由之后断开websocket连接
  }
};
</script>


<style lang="scss" scoped>
</style>