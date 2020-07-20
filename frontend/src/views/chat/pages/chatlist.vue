<!-- 聊天列表 -->
<template>
  <div class="msglist">
    <ul>
      <li
        v-for="item in group_list"
        class="sessionlist"
        :class="{ active: item.id === selectId }"
        @click="selectSession(item)"
      >
        <div class="list-left">
          <img
            class="avatar"
            width="42"
            height="42"
            :alt="item.name"
            :src="item.create_user.avatar"
          />
        </div>
        <div class="list-right">
          <p class="name">{{item.name}}</p>
          <span class="time">{{item.messages[item.messages.length-1].create_time|chatTime}}</span>
          <p class="lastmsg">{{item.messages[item.messages.length-1].message}}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { chatgroup, chatmessage } from "@/api/all";
import { mapGetters } from "vuex";
export default {
  name: "chatlist",

  components: {},
  data() {
    return {
      group_list: [],
      selectId: "",
      listQuery: {
        search: "",
        join_user: "",
        group: undefined
      }
    };
  },
  computed: {
    ...mapGetters(["user_id"])
  },
  created() {
    this.getGroupList();
  },
  methods: {
    getGroupList() {
      this.listQuery.join_user = this.user_id;
      chatgroup.requestGet(this.listQuery).then(response => {
        this.group_list = response.results;
      });
    },
    selectSession(row) {
      this.room_name = row.code;
      this.selectId = row.id;
    }
  }
};
</script>

<style lang="scss" scoped>
.sessionlist {
  display: flex;
  padding: 12px;
  transition: background-color 0.1s;
  font-size: 0;

  &:hover {
    background-color: rgb(220, 220, 220);
  }

  &.active {
    background-color: #c4c4c4;
  }

  .avatar {
    border-radius: 2px;
    margin-right: 12px;
  }

  .list-right {
    position: relative;
    flex: 1;
    margin-top: 4px;
  }

  .name {
    display: inline-block;
    vertical-align: top;
    font-size: 14px;
  }

  .time {
    float: right;
    color: #999;
    font-size: 10px;
    vertical-align: top;
  }

  .lastmsg {
    position: absolute;
    font-size: 12px;
    width: 130px;
    height: 15px;
    line-height: 15px;
    color: #999;
    bottom: 4px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
</style>