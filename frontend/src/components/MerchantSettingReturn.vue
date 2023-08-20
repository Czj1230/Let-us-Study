<template>
  <div>
    <el-result v-if="status==1" icon="success" title="Success!" subTitle="恭喜您，修改设置成功">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnMain">返回</el-button>
      </template>
    </el-result>
    <el-result v-else icon="warning" title="Failed!" subTitle="很遗憾，设置失败，请重新设置">
      <template slot="extra">
        <el-button type="primary" size="medium" @click="returnSetting">返回</el-button>
      </template>
    </el-result>
  </div>

</template>
<script>
export default {
  name: "MerchantSettingReturn",
  data() {
    return {
    };
  },
  methods: {
    getParams() {
      console.log(this.$route.query.status);
      this.status = this.$route.query.status;
      if (this.status == 1) {
        this.timestamp = this.$route.query.timestamp;
      }
    },
    returnMain() {
      this.$router.push("merchantmanage");
    },
    returnSetting() {
      this.$router.push("merchantsetting");
    }
  },
  created() {
    this.getParams();
  }
};
</script>
