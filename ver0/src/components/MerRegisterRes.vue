<template>
  <div>
    <el-result v-if="status==1" icon="success" title="Success!" subTitle="注册成功">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnMain">去登录</el-button>
      </template>
    </el-result>
    <el-result v-else icon="warning" title="Failed!" subTitle="注册失败！请重试">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnRegister">返回</el-button>
      </template>
    </el-result>
  </div>

</template>
<script>
export default {
  name: "MerRegisterRes",
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
      this.$router.push("/merchantlogin");
    },
    returnRegister() {
      this.$router.push({name: 'merchantregister'});
    }
  },
  created() {
    this.getParams();
  }
};
</script>
