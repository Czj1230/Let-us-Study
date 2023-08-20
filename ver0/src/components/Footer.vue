<template>
  <div>
    <span class="el-icon-user-solid">版权所有：啊对对队</span>
    <el-divider direction="vertical"></el-divider>
    <span class="el-icon-s-home">地址：上海市杨浦区邯郸路220号</span>
    <el-divider direction="vertical"></el-divider>
    <span class="el-icon-phone">电话：021-123456</span>
    <el-divider direction="vertical"></el-divider>
    <span class="el-icon-s-cooperation">邮箱：xuebaservice@fudan.edu.cn</span>
    <span class="app-foot" style="white-space: pre-wrap;">
      {{footerMsgCopyright}}
    </span>

  </div>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      // 版权说明的文字
      footerMsgCopyright: 'Copyright © 2022-2023 学吧 - Powered By 啊对对队',
      // 单位
      //footerMsgName: '啊对对队',
      //footerDetail: '版权所有：啊对对队\n地址：邯郸路255号\n电话：123456\n邮箱：123@fudan.edu.cn'
    }
  }
}
</script>

<style scoped>
.app-foot {
  /* footer 固定在页面底部 */
  margin-top: -30px;
  max-height: 100px;
  background-color: #eeeeee;
  width: 100%;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.source{
  font-weight: 600;
}
.detail{
  /* footer 固定在页面底部 */
  min-height: 0px;
  background-color: #eeeeee;

  font-size: 14px;
  display: inline;
  align-items: flex-start;
  justify-content: left;
}
</style>

