<template>
  <el-row>
    <br>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/merchantlist' }">自习室选择</el-breadcrumb-item>
      <el-breadcrumb-item>选座预约</el-breadcrumb-item>
    </el-breadcrumb>
    <div>
      <h2>{{ "自习室预约" }}</h2>
    </div>
    <el-descriptions v-if="isShow == true" class="merchant-info" title="商户信息" :column="2">
      <el-descriptions-item label="商户名称">{{ merchantName }}</el-descriptions-item>
      <el-descriptions-item label="评分">
        <el-rate v-model="merchantGrade" disabled show-score text-color="#ff9900" :colors="colors"
          score-template="{value}"></el-rate>
      </el-descriptions-item>
      <el-descriptions-item label="商户地址">{{ merchantLocation }}</el-descriptions-item>
      <el-descriptions-item label="价格">{{ merchantPrice }}</el-descriptions-item>
      <el-descriptions-item label="联系电话">{{ merchantPhone }}</el-descriptions-item>
      <el-descriptions-item label="营业时间段">{{ merchantTime }}</el-descriptions-item>
      <el-descriptions-item label="商户邮箱">{{ merchantEmail }}</el-descriptions-item>
      <el-descriptions-item label="当前拥挤度">
        <el-tag :type="vacancyType(studyroomVacancy)" size="small">{{ studyroomVacancy }}</el-tag>
      </el-descriptions-item>
    </el-descriptions>
    <el-skeleton v-else :rows="4" class="merchant-info" animated />
    <div v-if="isShow">
      <el-button type="info" v-if="selectSeatID == -1" :disabled="true">请选择座位</el-button>
      <el-button type="primary" v-else @click="submit">立即预约</el-button>
    </div>
    <el-card v-for="studyroom in StudyRoomList" class="studyroom-seat-table" :key="studyroom.Name">
      <h3>{{ studyroom.studyRoomName }}</h3>
      <p class="additional">{{ studyroom.additional_intro }}</p>
      <div class="seat-table">
        <div class="seat-table-line" v-for="seatline in studyroom.seatTable">
          <li class="seat-table-item" v-for="seat in seatline"
            :class="{ changeBorder: (seat.id == selectSeatID & studyroom.studyRoomID == selectRoomID) }">
            <div v-if="seat.selected == 0"></div>
            <div v-else-if="seat.selected == 1" @click="selectSeat(studyroom, seat.id)">
              <img src="../assets/seat-empty.png" width=100%>
            </div>
            <div v-else>
              <img src="../assets/seat-full.png" width=100%>
            </div>
            <div v-if="seat.selected > 0">{{ seat.id }}</div>
          </li>
        </div>
      </div>
    </el-card>
    <el-card v-if="isShow & !StudyRoomList.length" class="studyroom-seat-table">
      <el-empty :image-size="50" description="暂无座位信息" />
    </el-card>
    <Comment :passvalue="merchantID"></Comment>
  </el-row>

</template>

<script>
import Comment from './Comment';

export default {
  name: "SelectSeat",
  components: { Comment },
  data() {
    return {
      isShow: false,
      selectRoomID: -1,
      selectSeatID: -1,
      selectRoomName: -1,
      studentID: localStorage.getItem("id"),
      merchantName: "这个自习室飞走了哦o(╥﹏╥)o",
      StudyRoomList: [],
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
    }
  },
  methods: {
    getMerchantSeatInfo() {
      this.merchantID = this.$route.query.merchantID;
      this.$axios({
        method: "get",
        url: "api/seat/list/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log(res.data);
        this.merchantName = res.data.merchantShowName;
        this.StudyRoomList = res.data.StudyRoomList;
        this.merchantLocation = res.data.merchantLocation;
        this.merchantPrice = res.data.merchantPrice;
        this.merchantTime = res.data.merchantTime;
        this.studyroomVacancy = res.data.studyroomVacancy;
        this.merchantGrade = res.data.merchantGrade;
        this.merchantPhone = res.data.merchantPhone;
        this.merchantEmail = res.data.merchantEmail;
        this.isShow = true;
      }).catch(err => {
        console.log(err);
      })
    },
    selectSeat: function (room, seatID) {
      if (this.selectRoomID == room.studyRoomID & this.selectSeatID == seatID) {
        this.selectSeatID = -1;
      } else {
        this.selectRoomName = room.studyRoomName;
        this.selectRoomID = room.studyRoomID;
        this.selectSeatID = seatID;
      }
    },
    submit: function () {
      console.log(this.selectRoomID, this.selectRoomName, this.selectSeatID);
      this.$axios({
        method: "post",
        url: "api/order/create",
        headers: {
          "Content-Type": "application/json"
        },
        data: {
          merchantID: this.merchantID,
          studyRoomID: this.selectRoomID,
          seatName: this.selectSeatID,
          studentID: this.studentID
        }
      }).then(res => {
        console.log(res.data);
        this.$router.push({
          path: '/selectreturn', query: {
            status: res.data.status,
            msg: '提交时间：' + res.data.timestamp,
          }
        });
      }).catch(err => {
        console.log(err);
        this.$router.push({
          path: '/selectreturn', query: {
            status: 0,
            msg: '出错啦',
          }
        });
      });
    },
    loginCheck: function () {
      if (localStorage.getItem("id") == null) {
        this.$router.push({ path: '/studentlogin' });
      }
    },
    vacancyType: function (vacancy) {
      if (vacancy == 'empty') {
        return 'success';
      } else if (vacancy == 'medium') {
        return 'warning';
      } else {
        return 'danger';
      }
    }
  },
  created() {
    this.loginCheck();
    this.getMerchantSeatInfo();
  }
}
</script>
<style type="text/css">
.studyroom-seat-table {
  display: inline-block;
  font-size: medium;
  width: 80%;
  margin: 10px;
  padding: 20px;
  overflow: auto;
  border: 1px solid #ccc;
  border-radius: .2rem;
  margin-right: 1.5rem;
  box-sizing: border-box;
}

.seat-table {
  display: table;
  width: 100%;
  margin: 10 auto;
  text-align: center;
}

.seat-table-line {
  display: flex;
  flex-direction: row;
  justify-content: center;
  height: 60px;
  margin: 10px auto;
  width: auto;
}

.seat-table-item {
  width: 40px;
  height: 40px;
  border: 2px dashed #ccc;
  margin: 5px;
  list-style-type: none;
}

.changeBorder {
  border: 2px solid red;
}

.merchant-info {
  display: inline-block;
  width: 80%;
  margin: 10px;
  padding: 20px;
  text-align: left;
}

.el-descriptions__body {
  background-color: transparent;
}

.additional {
  font-size: small;
  color: #999;
}
</style>