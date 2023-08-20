<template>
    <div>
      <el-result v-if="status==1" icon="success" title="Success!" subTitle="新建成功">
        <template slot="extra">
          <el-button type="primary" size="medium" @click="returnRecord">返回首页</el-button>
        </template>
      </el-result>
      <el-result v-else icon="warning" title="Failed!" subTitle="新建失败！请重试">
        <template slot="extra">
          <el-button type="primary" size="medium" @click="returnSelect">返回</el-button>
        </template>
      </el-result>
    </div>
  
  </template>
  <script>
  export default {
    name: "NewRoomRes",
    data() {
      return {
      };
    },
    methods: {
      getParams() {
        this.status = this.$route.query.status;
        if (this.status == 1) {
          this.timestamp = this.$route.query.timestamp;
        }
      },
      returnRecord() {
        this.$router.push("/");
      },
      returnSelect() {
        this.$router.push({name: 'newroom', query: {
        merchantId: localStorage.getItem("id")
      }});
      }
    },
    created() {
      this.getParams();
    }
  };
  </script>