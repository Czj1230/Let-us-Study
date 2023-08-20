<template>
  <el-container>
    <el-header><Header/></el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
    <el-footer><Footer/></el-footer>
  </el-container>
</template>

<script>
import Header from "./Header";
import Footer from "./Footer";
import StudentLogin from "./StudentLogin";

export default {
  name: "Home",
  components: {Header,Footer,StudentLogin}
}
</script>

<style scoped>
.el-footer {
  background-color: #eeeeee;
  color: #333;
  text-align: center;
  line-height: 60px;
  padding: 0;
}
.el-header{
  background-color: #7f8488;
  color: #333;
  text-align: center;
  line-height: 60px;
  padding: 0;
}
.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  /*line-height: 500px;*/
}
</style>
