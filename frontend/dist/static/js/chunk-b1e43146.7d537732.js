(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-b1e43146"],{"6c07":function(t,e,s){"use strict";var o=s("c2df"),n=s.n(o);n.a},a4db:function(t,e,s){"use strict";s.r(e);var o=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"app-container"},[s("div",{staticClass:"cmd-container"},[s("el-row",{attrs:{gutter:20}},[s("el-col",{attrs:{span:18}},[s("div",{ref:"list_message",staticClass:"text"},[s("div",{staticClass:"emoji"},[s("span",[t._v("[root@localhost ~]#")]),t._v(" "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.temp.cmd,expression:"temp.cmd"}],attrs:{type:"text",placeholder:"输入命令"},domProps:{value:t.temp.cmd},on:{keyup:t.onKeyup,input:function(e){e.target.composing||t.$set(t.temp,"cmd",e.target.value)}}})]),t._v(" "),t._l(t.results,(function(e){return s("p",{key:e},[t._v(t._s(e))])}))],2)]),t._v(" "),s("el-col",{attrs:{span:6}},[s("ul",{staticClass:"infinite-list"},t._l(t.history_list,(function(e){return s("li",{key:e.id,staticClass:"infinite-list-item",on:{click:function(s){return t.changeCdm(e.cmd)}}},[s("a",[t._v(t._s(e.cmd))])])})),0)])],1)],1)])},n=[],c=(s("6b54"),s("db72")),i=s("8c63"),l=s("2f62"),r={name:"shell",components:{},data:function(){return{listQuery:{search:"",join_user:"",group:void 0},temp:{cmd:"ping www.baidu.com"},ws_uri:"/ws/shell/",lockReconnect:!1,maxReconnect:5,socket:null,results:[],history_list:[],hostory_listQuery:{offset:1,limit:10}}},computed:Object(c["a"])({},Object(l["b"])(["user_id"])),created:function(){this.getList()},destroyed:function(){this.socket.close()},methods:{getList:function(){var t=this;i["g"].requestGet().then((function(e){t.history_list=e.results}))},changeCdm:function(t){this.temp.cmd=t},scrollToBottom:function(){var t=this;this.$nextTick((function(){setTimeout((function(){t.$refs.list_message.scrollTop=t.$refs.list_message.scrollHeight}),0)}))},onKeyup:function(t){13===t.keyCode&&this.cmdrun()},cmdrun:function(){var t=new Date,e=t.getMinutes()+1<10?"0"+t.getMinutes():t.getMinutes(),s=t.getSeconds()+1<10?"0"+t.getSeconds():t.getSeconds(),o=t.getMilliseconds().toString().length<3?"0"+t.getMilliseconds():t.getMilliseconds(),n=e+"-"+s+"-"+o;this.results=[],this.initWebSocket(n)},reconnect:function(){var t=this;console.log("尝试重连"),this.lockReconnect||this.maxReconnect<=0||setTimeout((function(){t.initWebSocket()}),6e4)},initWebSocket:function(t){try{if("WebSocket"in window){var e="https:"==window.location.protocol?"wss://":"ws://",s=window.location.host,o=e+s+this.ws_uri+t;console.log(o),this.socket=new WebSocket(o)}else console.log("您的浏览器不支持websocket");this.socket.onopen=this.websocketonopen,this.socket.onerror=this.websocketonerror,this.socket.onmessage=this.websocketonmessage,this.socket.onclose=this.websocketclose}catch(n){this.reconnect()}},websocketonopen:function(){console.log("WebSocket连接成功",this.socket.readyState),this.websocketsend()},websocketonerror:function(t){console.log("WebSocket连接发生错误",t),this.reconnect()},websocketonmessage:function(t){var e=JSON.parse(t.data);this.results.push(e["text"]),this.scrollToBottom()},websocketclose:function(t){console.log("ws连接已断开 ("+t.code+")"),this.getList()},websocketsend:function(){this.socket.send(JSON.stringify(this.temp))}}},a=r,u=(s("6c07"),s("2877")),d=Object(u["a"])(a,o,n,!1,null,"941b5082",null);e["default"]=d.exports},c2df:function(t,e,s){}}]);