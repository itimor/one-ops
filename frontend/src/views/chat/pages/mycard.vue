<!-- 最左边的选择框 -->
<template>
  <div class="mycard">
    <header>
      <el-avatar class="avatar" shape="square">我</el-avatar>
    </header>
    <div class="navbar">
      <i style="color: green;" class="icon el-icon-chat-dot-round"></i>
      <i class="icon el-icon-connection"></i>
      <i class="icon el-icon-picture-outline"></i>
    </div>
    <footer>
      <i class="icon el-icon-s-operation"></i>
    </footer>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
.mycard {
  position: relative;
  width: 100%;
  height: 100%;
  .avatar {
    width: 36px;
    height: 36px;
    margin: 20px 12px 0 12px;
    border-radius: 2px;
  }
  .navbar {
    width: 100%;
    text-align: center;
  }
  .icon {
    display: inline-block;
    font-size: 26px;
    margin-top: 28px;
    padding: 0 16px;
    box-sizing: border-box;
    color: #adaeaf;
    opacity: 0.8;
    cursor: pointer;
    &:hover {
      opacity: 1;
    }
  }
  footer {
    position: absolute;
    bottom: 20px;
    width: 100%;
    text-align: center;
  }
}
</style>