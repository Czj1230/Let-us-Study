<template>
  <div>
    <div class="header">
      <el-autocomplete v-model="state" :fetch-suggestions="querySearchAsync" placeholder="请输入内容" @select="handleSelect"
        value-key="merchantShowName"></el-autocomplete>
      <el-button @click="returnAll">展示所有</el-button>
      <el-button icon="el-icon-d-caret" @click="SortByName">按名称排序</el-button>
      <el-button icon="el-icon-d-caret" @click="SortByGrade">按评分排序</el-button>
      <el-button icon="el-icon-d-caret" @click="SortByVacancy">按空闲程度排序</el-button>
    </div>
    <el-row :gutter="20">
      <el-col :span="6" v-for="t in merchantList" :key="t.merchantId">
        <el-card :body-style="{ padding: '0px' }" class="tenant-item">
          <img v-if="t.merchantImage" :src="t.merchantImage" :preview-src-list="[t.merchantImage]" class="image">
          <span class="tenant-name">{{ t.merchantShowName }}</span>
          <div>
            <div class="tenant-description">
              <div class="tenant-location">{{ ellipsis(t.merchantLocation) }}</div>
              <div class="tenant-grades">评分：{{ t.merchantGrade }} / 5.0</div>
              <!--          <div class="tenant-vacancy" v-if="judgeVacancy(t.studyroomVacancy)==1">空闲情况：拥挤</div>-->
              <!--          <div class="tenant-vacancy" v-else-if="judgeVacancy(t.studyroomVacancy)==2">空闲情况：中等</div>-->
              <!--          <div class="tenant-vacancy" v-else="judgeVacancy(t.studyroomVacancy)==3">空闲情况：空闲</div>-->
              <div class="tenant-vacancy" v-if="t.studyroomVacancy < 0.4">空闲情况：空闲</div>
              <div class="tenant-vacancy" v-else-if="t.studyroomVacancy < 0.8">空闲情况：中等</div>
              <div class="tenant-vacancy" v-else="t.studyroomVacancy>=0.8">空闲情况：拥挤</div>
              <el-button type="primary" plain @click="viewseat(t.merchantId)">预约</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>

export default {
  name: 'MerchantList',
  data() {
    return {
      isShow: false,
      merchantList: [],
      timeout: null,
      state: '',
    }
  },
  methods: {
    viewseat: function (merchantId) {
      if (localStorage.getItem("id") == null) {
        this.$message({
          message: '请先登录',
          type: 'warning'
        });
      } else if (localStorage.getItem("status") == 2) {
        this.$message({
          message: '您当前登录状态为商户，无法预约，您可以在商户个人空间管理您的自习室。',
          type: 'warning'
        });
      } else {
        this.$router.push({ path: '/selectseat', query: { merchantID: merchantId } })
      }
    },
    getMerchantList() {
      let that = this;
      this.$axios({
        method: "get",
        url: "api/merchant/list",
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        this.merchantList = res.data.all_merchant;
        this.isShow = true;
        for (let i = 0; i < this.merchantList.length; i++) {
          that.getImg(this.merchantList[i].merchantId, i);
        }
      }).catch(err => {
        console.log(err);
      })
    },
    getImg(merchantId, index) {
      this.$axios({
        method: "get",
        url: "api/merchant/getImg/" + merchantId,
        headers: {
          "Content-Type": "image/png"
        },
        responseType: 'blob',
      }).then(({ data }) => {
        let blob = new Blob([data]);   // 返回的文件流数据
        let url = window.URL.createObjectURL(blob);  // 将他转化为路径
        this.merchantList[index].merchantImage = url; // 将转换出来的路径赋值给变量
      }).catch(err => {
        console.log(err);
      })
    },
    querySearchAsync(queryString, cb) { // 搜索
      var temp = this.merchantList;
      var results = queryString ? temp.filter(this.createStateFilter(queryString)) : temp;
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 3000 * Math.random());
    },
    createStateFilter(queryString) { // 满足条件
      return (state) => {
        return (state.merchantShowName.toLowerCase().indexOf(queryString.toLowerCase()) > -1);
      };
    },
    handleSelect(item) {  // 选中
      this.merchantList = [item];
    },
    returnAll() { // 返回所有
      this.getMerchantList();
    },
    SortByName() {
      this.merchantList = this.SortVal(this.merchantList, 'merchantShowName');
      // console.log(this.merchantList);
    },
    SortVal(array, val) {
      return array.sort(function (a, b) {
        let x = a[val].toUpperCase();
        let y = b[val].toUpperCase();
        return (x > y) ? 1 : ((x < y) ? -1 : 0);
      }
      );
    },
    SortByGrade() {
      this.merchantList = this.SortNumDes(this.merchantList, 'merchantGrade');
      // console.log(this.merchantList);
    },
    SortNumDes(array, val) {
      return array.sort(function (a, b) {
        let x = a[val];
        let y = b[val];
        return (x < y) ? 1 : ((x > y) ? -1 : 0);
      }
      );
    },
    SortByVacancy() {
      this.merchantList = this.SortNum(this.merchantList, 'studyroomVacancy');
      console.log(this.merchantList);
    },
    SortNum(array, val) {
      return array.sort(function (a, b) {
        let x = a[val];
        let y = b[val];
        return (x > y) ? 1 : ((x < y) ? -1 : 0);
      })
    },
    ellipsis(value) {
      if (!value) return "";
      if (value.length > 18) {
        return value.slice(0, 18) + "...";
      }
      return value;
    }
    // SortValDes(array, val) {
    //   return array.sort(function(a, b) {
    //       let x = a[val].toUpperCase();
    //       let y = b[val].toUpperCase();
    //       return (x < y) ? 1 : ((x > y) ? -1 : 0) ;
    //     }
    //   );
    // },
  },
  mounted() {
    this.getMerchantList();
  },
}

</script>

<style scoped>
.tenant-item {
  padding-left: 10px;
  padding-right: 10px;
  padding-top: 10px;
  font-size: medium;
  display: inline-block;
  flex-wrap: wrap;
  justify-content: center;
  width: 280px;
  height: 320px;
  box-sizing: border-box;
  line-height: 23px;
}

.image {
  width: 260px;
  display: block;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  height: 150px;
  padding-bottom: 10px;
}

.tenant-name {
  height: 40px;
  font-size: x-large;
}
</style>
