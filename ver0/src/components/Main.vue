<template>
  <div class="block">
    <el-carousel :interval="4000" type="card" height="500px" indicator-position="outside">
      <el-carousel-item v-for="item in 4" :key="item">
        <img v-if="item==1" src="../assets/r1.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==2" src="../assets/r2.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==3" src="../assets/r3.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==4" src="../assets/r4.jpg" style="display: block; width: 100%; height: 100%">
      </el-carousel-item>
    </el-carousel>
    <img src="../assets/study4.png" alt="Smiley face" style="float:left" width="500" height="350">
    <br>
    <h2>关于我们 ABOUT US</h2>
    <p>是时候提高生产力了！</p>
    <p>学吧StudyRoom聚焦于当下自习室的一系列问题，</p>
    <p>专为学生打造了高效便捷的自习室预约平台。</p>
    <p>此外，学吧还为用户提供了“专属自习管家模块”、</p>
    <p>“积分榜排行机制”等。</p>
    <p>学吧将见证你学习中的点滴进步，</p>
    <p>时刻让你动力满满！</p>
    <br><br><br><br>
    <img src="../assets/study1.png" alt="Smiley face" style="float:right" width="500" height="350">
    <h2>自习室预约 STUDY ROOM APPOINTMENT</h2>
    <p>学吧提供了高效便捷的自习室预约平台</p>
    <p>在这里，用户可以细致清晰地多家自习室的基本信息：</p>
    <p>地址、评分、评价、价格、</p>
    <p>环境条件、空闲情况、营业时间等应有尽有！</p>
    <p>学生可以随时个性化地预约专属的自习时间与座位。</p>
    <p>此外，学吧还提供了用户评价功能，</p>
    <p>让用户们的感受共同打造一个真实的自习室！</p>
    <br><br><br><br>
    <img src="../assets/study5.png" alt="Smiley face" style="float:left" width="500" height="350">
    <h2>自习管家 STUDY MANAGEMENT</h2>
    <p>学习没有计划，ddl很多却无从下手？</p>
    <p>学吧为用户专属打造了自习管家模块：</p>
    <p>Todo list为你管理待办&完成事项，为你的ddl们排序；</p>
    <p>倒数日帮你铭记重要的日子，生活中的大事有条不紊地在你面前展开；</p>
    <p>日程安排为你规划专属日程，为事情做计划，让你的学习更高效！</p>
    <p>快来体验更多的宝藏功能，</p>
    <p>让学吧为你专属打造规律的学习生活！</p>
    <br><br><br><br>
    <img src="../assets/study2.png" alt="Smiley face" style="float:right" width="500" height="350">
    <h2>自习激励 STUDY MOTIVATION</h2>
    <p>学吧提供了激烈的积分榜排行机制：</p>
    <p>在这里，用户可以根据自己的自习时长获取积分、参与排行，</p>
    <p>排行前十名的用户可以获得相应的精美小奖品！</p>
    <p>在积分排行的过程中，</p>
    <p>激励用户养成良好的自习习惯。</p>
    <p>快来学吧体验，</p>
    <p>让你时刻充满学习动力！</p>
  </div>
</template>

<script>
export default {
  name: "Main"
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
