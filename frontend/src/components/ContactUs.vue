<template>
  <div class="block">
    <el-carousel height="500px" indicator-position="outside">
      <el-carousel-item v-for="item in 4" :key="item">
        <img v-if="item==1" src="../assets/cop2.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==2" src="../assets/cop3.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==3" src="../assets/cop.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==4" src="../assets/r3.jpg" style="display: block; width: 100%; height: 100%">
      </el-carousel-item>
    </el-carousel>
    <h2>联系我们 CONTACT US</h2>
    <p>地址：上海市杨浦区邯郸路220号</p>
    <p>电话：021-123456</p>
    <p>邮箱：xuebaservice@fudan.edu.cn</p>
    <p>商务合作邮箱：xuebacoop@fudan.edu.cn</p>
    <br>
    <h2>商务合作 BUSINESS COOPERATION</h2>
    <p>欢迎与学吧进行品牌/IP跨界合作！请在下方留下您的联系方式与合作期望：</p>
    <el-link type="primary" href="https://www.wjx.cn/vm/tXAarrS.aspx" target="_blank">点击填写您的具体合作意向及需求</el-link>
  </div>
</template>

<script>
export default {
  name: "ContactUs"
}
</script>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  display: block;
  width: 100%;
  height: 100%;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}
</style>
