<template>
  <el-row>
    <div>
      <h2>商户管理空间</h2>
    </div>
    <div class="info">
      <el-row>
        <el-col :span="6">
          <img
            v-if="merchantImage"
            :src="merchantImage"
            :preview-src-list="[merchantImage]"
            class="image"
          />
          <el-skeleton v-else :rows="4" class="merchant-info2" animated />
        </el-col>
        <el-col :span="18">
          <el-descriptions
            v-if="isShow == true"
            class="merchant-info2"
            title="基本信息"
            :column="2"
          >
            <template slot="extra">
              <el-button
                type="primary"
                icon="el-icon-edit"
                @click="JumpToSetting"
                size="small"
                >修改信息</el-button
              >
            </template>
            <el-descriptions-item label="商户名称">{{
              merchantName
            }}</el-descriptions-item>
            <el-descriptions-item label="评分">
              <el-rate v-model="merchantGrade" disabled show-score text-color="#ff9900" :colors="colors"
          score-template="{value}"></el-rate>
            </el-descriptions-item>
            <el-descriptions-item label="商户地址">{{
              merchantLocation
            }}</el-descriptions-item>
            <el-descriptions-item label="价格">{{
              merchantPrice
            }}</el-descriptions-item>
            <el-descriptions-item label="营业时间">{{
              merchantTime
            }}</el-descriptions-item>
            <el-descriptions-item label="当前拥挤程度">
              <el-tag size="small">{{ studyroomVacancy }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="联系电话">{{
              merchantPhone
            }}</el-descriptions-item>
          </el-descriptions>
          <el-skeleton v-else :rows="4" class="merchant-info" animated />
        </el-col>
      </el-row>
    </div>

    <el-descriptions class="merchant-info" title="自习室信息" :colon="false">
      <template slot="extra">
        <el-button
          type="primary"
          @click="NewRoom"
          size="small"
          icon="el-icon-plus"
          style="margin-right: 10px"
          >新建自习室</el-button
        >
      </template>
      <el-descriptions-item label="点击查看我的所有自习室"></el-descriptions-item>
    </el-descriptions>
    <el-collapse
      v-for="studyroom in StudyRoomList"
      :key="studyroom.studyRoomID"
      class="studyroom-collapse"
    >
      <el-collapse-item :title="studyroom.studyRoomName">
        <div class="operations">
          <el-button
            type="danger"
            icon="el-icon-delete"
            size="small"
            @click="deleteStudyRoom(studyroom.studyRoomID)"
            >删除</el-button
          >
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="small"
            @click="editStudyRoom(studyroom.studyRoomID)"
            >编辑</el-button
          >
        </div>
        <span class="additional">介绍：{{ studyroom.additional_intro }}</span>
        <div class="seat-table">
          <div class="seat-table-line" v-for="seatline in studyroom.seatTable">
            <li
              class="seat-table-item"
              v-for="seat in seatline"
              :class="{
                changeBorder:
                  (seat.id == selectSeatID) &
                  (studyroom.studyRoomID == selectRoomID)
              }"
            >
              <div v-if="seat.selected == 0"></div>
              <div v-else-if="seat.selected == 1">
                <img src="../assets/seat-empty.png" width="100%" />
              </div>
              <div v-else>
                <img src="../assets/seat-full.png" width="100%" />
              </div>
              <div v-if="seat.selected > 0">{{ seat.id }}</div>
            </li>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>


    <el-descriptions class="merchant-info" title="评价信息"  :colon="false">
      <el-descriptions-item label="浏览我的所有用户评价"></el-descriptions-item>
    </el-descriptions>
    <Comment class="comment" :passvalue="merchantID"></Comment>

  </el-row>
</template>
<script>
import Comment from "./Comment.vue";
export default {
  name: "MerchantManage",
  data() {
    return {
      isShow: false,
      selectRoomID: -1,
      selectSeatID: -1,
      selectRoomName: -1,
      merchantID: localStorage.getItem("id"),
      merchantName: "这个自习室飞走了哦o(╥﹏╥)o",
      StudyRoomList: [],
      merchantImage: "",
      colors: ["#99A9BF", "#F7BA2A", "#FF9900"]
    };
  },
  components: {
    Comment
  },
  methods: {
    deleteStudyRoom(id) {
      // console.log(id);
      this.$axios({
        method: "delete",
        url: "api/studyroom/" + id
      }).then(res => {
        // console.log(res.data.status);
        if (res.data.status == 1) {
          this.$message({
            message: "删除成功",
            type: "success"
          });
          this.getStudyRoomList();
        } else {
          this.$message({
            message: "删除失败",
            type: "error"
          });
        }
      });
    },
    getImg() {
      this.$axios({
        method: "get",
        url: "api/merchant/getImg/" + this.merchantID,
        headers: {
          "Content-Type": "image/png"
        },
        responseType: "blob"
      })
        .then(({ data }) => {
          let blob = new Blob([data]); // 返回的文件流数据
          let url = window.URL.createObjectURL(blob); // 将他转化为路径
          this.merchantImage = url; // 将转换出来的路径赋值给变量
          console.log(this.merchantImage);
        })
        .catch(err => {
          console.log(err);
        });
    },
    getMerchantSeatInfo() {
      console.log(this.merchantID);
      this.$axios({
        method: "get",
        url: "api/seat/list/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => {
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
          console.log(this.merchantGrade);
        })
        .catch(err => {
          console.log(err);
        });
    },
    getStudyRoomList() {
      this.$axios({
        method: "get",
        url: "api/seat/list/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => {
          this.StudyRoomList = res.data.StudyRoomList;
        })
        .catch(err => {
          console.log(err);
        });
    },
    loginCheck: function() {
      if (localStorage.getItem("id") == null) {
        this.$router.push({ path: "/merchantlogin" });
      }
    },
    JumpToSetting() {
      this.$router.push({ path: "/merchantsetting" });
    },
    NewRoom() {
      this.$router.push({
        path: "/newroom",
        query: {
          merchantId: this.merchantID
        }
      });
    },
    editStudyRoom(id) {
      this.$router.push({
        path: "/editroom",
        query: {
          merchantId: this.merchantID,
          studyRoomId: id
        }
      });
    }
  },
  created() {
    this.loginCheck();
    this.getMerchantSeatInfo();
    this.getImg();
  }
};
</script>
<style>
.info {
  margin: 0 auto;
  padding: 20px;
  /* background-color: #fff; */
  border-radius: 5px;
  width: 78%;
  background-color: transparent;
  /* text-align: center; */
}
.studyroom-collapse {
  width: 80%;
  display: inline-block;
}

.el-collapse-item__header {
  border-bottom: 0px;
  padding-left: 10px;
  font-weight: bold; 
}

.seat-table {
  display: table;
  width: 100%;
  /* margin: 10 auto; */
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

.merchant-info2 {
  display: inline-block;
  /* width: 80%; */
  /* margin: 10px; */
  padding-left: 30px;
  text-align: left;
}
.merchant-info {
  display: inline-block;
  width: 80%;
  margin: 10px;
  /* padding: 20px; */
  padding-bottom: 0;
  text-align: left;
}
.el-descriptions__body {
  background-color: transparent;
}

.studyroom-name {
  float: left;
  margin-left: 25%;
  width: 50%;
}

.operations {
  float: right;
  margin-right: 5%;
  /* width: 50%; */
}

.comment {
  /* display: inline-block; */
  /* width: 75% !important; */
  margin-left: 24px !important;
}
.image {
  /* margin-top: 10%; */
  width: 100%;
  display: flex;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  height: 100%;
  /* padding-bottom: 10px; */
}
.additional {
  float: left;
  padding-left: 30px;
  font-size: small;
  color: #999;
}
</style>
