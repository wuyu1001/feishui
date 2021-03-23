<template>
  <div id="app">
    <el-container style="height: 900px; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu :default-active="this.$router.path" router>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>学生数据管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="/ywsj">业务数据</el-menu-item>
              <el-menu-item index="/yscsj">已上传数据</el-menu-item>
              <el-menu-item index="/cysj">差异数据</el-menu-item>
              <el-menu-item index="/upload">待上传数据</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
        <el-menu :default-active="this.$router.path" router>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>作业调度管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="/">上传非税作业</el-menu-item>
              <el-menu-item index="/">接收非税作业</el-menu-item>
              <el-menu-item index="/">上传八骏作业</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script>
export default {
  methods: {
  },
  mounted() {

  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-weight: bold;
}
</style>
