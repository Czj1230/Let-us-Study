<template>
  <el-row>
    <el-col  :span="12">
      <UploadMerchantProfile></UploadMerchantProfile>
    </el-col>
    <el-col  :span="12">
    <el-form ref="form"  class="SettingForm" label-width="200px">
      <el-form-item label="商户名称">
        <el-input v-model="merchantShowName" class="name"></el-input>
      </el-form-item>
      <el-form-item label="商户地址">
        <el-input v-model="merchantLocation" class="location"></el-input>
      </el-form-item>
      <el-form-item label="营业开始时间">
        <el-time-picker v-model="merchantStartTime" value-format="HH:mm:ss"
                        :picker-options="{selectableRange: '00:00:00 - 12:00:00'}"></el-time-picker>
      </el-form-item>
      <el-form-item label="营业结束时间">
        <el-time-picker v-model="merchantEndTime" value-format="HH:mm:ss"
                        :picker-options="{selectableRange: '12:00:01 - 23:59:59'}"></el-time-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit">提交</el-button>
      </el-form-item>
    </el-form>
    </el-col>
  </el-row>
</template>

<script>
import UploadMerchantProfile from "./UploadMerchantProfile";

export default {
  name: 'MerchantSetting',
  components: { UploadMerchantProfile },
  data() {
    return {
      merchantID: localStorage.getItem("id"),
      merchantShowName: '',
      merchantLocation: '',
      merchantStartTime: '',
      merchantEndTime: ''
    };
  },
  methods: {
    // getMerchantInfo() {
    //   this.merchantID = this.$route.query.merchantId;;
    // },
    submit: function () {
      // console.log(this.merchantName,this.merchantLocation,this.merchantStartTime,this.merchantEndTime);
      this.$axios({
        method: "put",
        url: "api/merchant/"+this.merchantID,
        headers: {
          "Content-Type": "application/json"
        },
        params: {
          merchantShowName: this.merchantShowName,
          merchantLocation: this.merchantLocation,
          merchantStartTime: this.merchantStartTime,
          merchantEndTime: this.merchantEndTime
        }
      }).then(res => {
        console.log(res.data);
        this.$router.push({
          path: '/merchantsettingreturn', query: {
            status: 1,
            timestamp: res.data.timestamp,
          }
        });
      }).catch(err => {
        console.log(err);
        this.$router.push({
          path: '/merchantsettingreturn', query: {
            status: 0
          }
        });
      });
    },
    getMerchantInfo() {
      this.$axios({
        method: "get",
        url: "api/seat/list/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => {
          console.log(res.data);
          this.merchantShowName = res.data.merchantShowName;
          this.merchantLocation = res.data.merchantLocation;
          this.merchantStartTime = res.data.merchantTime.split('-')[0];
          this.merchantEndTime = res.data.merchantTime.split('-')[1];
          console.log(this.merchantStartTime)
          console.log(this.merchantEndTime)
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.getMerchantInfo();
  }
}
</script>

<style scoped>
.SettingForm{
  line-height: 45px;
}
.name{
  width: 200px;
}
.location{
  width: 200px;
}
</style>
