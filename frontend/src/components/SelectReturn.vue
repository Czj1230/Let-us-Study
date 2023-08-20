<template>
  <div>
    <el-result v-if="status==1" icon="success" title="预约成功" :subTitle="msg">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnRecord">查看预约记录</el-button>
      </template>
    </el-result>
    <el-result v-else icon="warning" title="预约失败" subTitle="很遗憾，请重新预约">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnSelect">返回</el-button>
      </template>
    </el-result>
  </div>

</template>
<script>
export default {
  name: "SelectReturn",
  data() {
    return {
    };
  },
  methods: {
    getParams() {
      console.log(this.$route.query.status);
      this.status = this.$route.query.status;
      this.msg = this.$route.query.msg;
    },
    returnRecord() {
      this.$router.push("reservartionrecord");
    },
    returnSelect() {
      this.$router.push("merchantlist");
    }
  },
  created() {
    this.getParams();
  }
};
</script>