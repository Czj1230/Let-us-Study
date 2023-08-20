<template>
  <div>
    <el-result v-if="status==1" icon="success" title="Success!" subTitle="登录成功">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnMain">返回首页</el-button>
      </template>
    </el-result>
    <el-result v-else icon="warning" title="Failed!" subTitle="登录失败！请重试">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnLogin">返回</el-button>
      </template>
    </el-result>
  </div>

</template>
<script>
export default {
  name: "StdLoginRes",
  data() {
    return {
    };
  },
  methods: {
    getParams() {
      console.log(this.$route.params.status);
      this.status = this.$route.query.status;
      if (this.status == 1) {
        this.timestamp = this.$route.query.timestamp;
      }
    },
    returnMain() {
      this.$router.push("/");
    },
    returnLogin() {
      this.$router.push({name: 'studentlogin'});
    }
  },
  created() {
    this.getParams();
  }
};
</script>
