<template>
  <div class="block">
    <el-carousel height="500px" indicator-position="outside">
      <el-carousel-item v-for="item in 4" :key="item">
        <img v-if="item==1" src="../assets/aboutxueba1.png" style="display: block; width: 100%; height: 100%">
        <img v-if="item==2" src="../assets/r1.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==3" src="../assets/r2.jpg" style="display: block; width: 100%; height: 100%">
        <img v-if="item==4" src="../assets/r3.jpg" style="display: block; width: 100%; height: 100%">
      </el-carousel-item>
    </el-carousel>
    <el-tabs v-model="activeName" @tab-click="handleClick" stretch>
      <el-tab-pane class="fontClass" label="学吧介绍" name="first">
        <h2>“学吧”——自习室预约平台 & 专属自习管家</h2>
        <h3>功能导引——学生</h3>
        <p>
        1.实时查看自习室座位情况以及环境条件，以便于选择心仪的座位与时间，实现自习室的预约；<br>
        2.利用学吧的学习管家模块，指定专属学习任务清单，规划个人日程安排；<br>
        3.利用学吧的激励机制，通过参与积分榜排行来督促学习。<br></p>
        <br>
        <h3>功能导引——商户</h3>
        <p>
        1.设置自习室的基本信息、座位布局与环境条件，以便于学生在学吧平台上更全面的了解自习室概况；<br>
        2.实时查看自习室预约情况，并根据实际自习室座位使用情况进行线上自习室座位管理。</p>
      </el-tab-pane>
      <el-tab-pane class="fontClass" label="学吧愿景" name="second">
        <h4>当下生活中，去自习室自习已经成为了学生们的常态。然而，学生们会面临一些问题：</h4>
        <p>自习室心仪位置的稀缺？自习室环境条件的不舒适？<br>
          现有的自习室预约平台入口分散、复杂，不方便使用？<br>
          学习时没有计划，ddl总是赶不完？<br>
          缺乏奖励机制，自习时没有动力？<br>
          ......<br></p>
        <h4>学吧致力于解决学生自习方面的问题：</h4>
        <p>高效透明的自习室预约机制予你良好的预约体验；</p>
        <p>方便简洁的自习管家模块会成为你学习的得力助手；</p>
        <p>激烈的积分榜排行随时为你充电！</p>
      </el-tab-pane>
      <el-tab-pane class="fontClass" label="入驻商家" name="third">
        <h4>迄今为止，多达数十家商家入驻，快来加入我们吧！</h4>
        <p>2022年 阳光自习室 &nbsp&nbsp&nbsp&nbsp邯郸路222号</p>
        <p>2022年 全家便利店&nbsp&nbsp&nbsp&nbsp五角场大学</p>
        <p>2022年 FDU北食二楼静音仓&nbsp&nbsp&nbsp&nbsp武东路57号</p>
        <p>......</p>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: "AboutXueba",
  data() {
    return {
      activeName: 'second'
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    }
  }
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
::v-deep .el-tabs__nav-scroll{
  width:50%!important;
  margin:0 auto!important;
}
.fontClass{
  font-size: 17px;
  font-family: "Microsoft YaHei";
}
::v-deep .el-tabs__item{
  font-size: 30px !important;
}

</style>
