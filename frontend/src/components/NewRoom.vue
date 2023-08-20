<template>
  <div class="new-room">
    <h1>新建自习室</h1>
    <div class="room-form">
     
      <el-form label-width="25%" :label-position="left">
        <el-form-item label="自习室名称">
          <el-input v-model="roomName" class="name"></el-input>
        </el-form-item>
        <el-form-item label="自习室简介">
          <el-input
            v-model="roomIntro"
            placeholder="Room Introductory Text"
            clearable
            :autosize="{ minRows: 10, maxRows: 20 }"
            maxlength="1000"
            show-word-limit
            class="intro"
            type="textarea"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-form :inline="true" class="demo-form-inline row-col-form" >
        <el-form-item label="行数">
          <el-input-number
            v-model="rows"
            :min="1"
            label="请输入数量"
            class="number"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="列数">
          <el-input-number
            v-model="cols"
            :min="1"
            label="请输入数量"
            class="number"
          ></el-input-number>
          <!-- <el-divider></el-divider> -->
        </el-form-item>
      </el-form>
      <el-divider></el-divider>
      <el-card :body-style="{ padding: '0px' }" class="room-table">
        <table class="room-img">
          <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
            <td id="seatblock" v-for="(col, colIndex) in cols" :key="colIndex">
              <input
                type="checkbox"
                v-on:change="updateRoomVec(rowIndex, colIndex)"
                v-model="checkedVec[rowIndex][colIndex]"
              />
              <br />
              <div
                class="seatNumber"
                v-if="checkedVec[rowIndex][colIndex] == 1"
              >
                {{ roomVec[rowIndex][colIndex] }}
              </div>
            </td>
          </tr>
        </table>
      </el-card>
      <el-divider></el-divider>
      <el-form>
        <el-form-item>
          <el-button type="primary submit" @click="createRoom">提交</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
Vue.prototype.$axios = axios;

export default {
  name: "NewRoom",
  // props: ["merchantId"],
  data() {
    // console.log(parseInt(this.$route.query.merchantId));
    return {
      roomName: "",
      roomIntro: "",
      rows: 0,
      cols: 0,
      checkedVec: [],
      roomVec: [],
      seatNumber: 0,
      merchantId: parseInt(this.$route.query.merchantId)
    };
  },
  watch: {
    rows() {
      if (this.rows > 0) this.updateRoomSize();
    },
    cols() {
      if (this.cols > 0) this.updateRoomSize();
    }
  },
  methods: {
    updateRoomSize() {
      if (this.rows > 0 && this.cols > 0) {
        this.checkedVec = Array(this.rows)
          .fill(false)
          .map(() => Array(this.cols).fill(false));
        this.roomVec = Array(this.rows)
          .fill(0)
          .map(() => Array(this.cols).fill(0));
      } else {
        this.checkedVec = [];
        this.roomVec = [];
      }
      this.seatNumber = 0;
    },
    createRoom() {
      // console.log(this.$route.params.merchantId);
      let data = {
        merchantID: this.merchantId,
        studyRoomName: this.roomName,
        seatTable: this.roomVec,
        additional_intro: this.roomIntro
      };
      // console.log(data);
      this.$axios({
        method: "post",
        url: "api/studyroom/newroom",
        data: data,
        header: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        this.$router.push({
          path: "/newroomres",
          query: {
            status: res.data.status
          }
        });
      });
    },
    updateRoomVec(row, col) {
      this.seatNumber += this.checkedVec[row][col] ? 1 : -1;
      // correct other seat number
      if (!this.checkedVec[row][col] && this.roomVec[row][col]) {
        this.roomVec.forEach((rowVec, rowIndex) => {
          rowVec.forEach((colVec, colIndex) => {
            if (this.roomVec[rowIndex][colIndex] > this.roomVec[row][col]) {
              this.roomVec[rowIndex][colIndex] -= 1;
            }
          });
        });
        this.roomVec[row][col] = 0;
      } else if (this.checkedVec[row][col])
        this.roomVec[row][col] = this.seatNumber;
    }
  }
};
</script>

<style scoped>
.room-form {
  display: inline-block;
  width: 60%;
  margin: 0 auto;
}
.new-room {
  text-align: center;
}
.room-img {
  margin: 0 auto;
}
.room-table {
  padding-left: 10px;
  /* padding-right: 10px; */
  padding-top: 10px;
  font-size: medium;
  display: inline-block;
  min-width: 90%;
  max-width: 800px;
  min-height: 280px;
  white-space: nowrap;
  overflow: auto;
  border: 1px solid #ccc;
  border-radius: 0.2rem;
  /* margin-right: 1.5rem; */
  box-sizing: border-box;
}

.number {
  /* margin-left: 12%; */
  /* margin-right: 12%; */
}
.name {
  /* width: 200px; */
  margin-left: 10%;
  margin-right: 10%;
  width: 80%;
}
.intro {
  width: 80%;
  height: 200px;
  padding-bottom: 10px;
  margin-left: 10%;
  margin-right: 10%;
}

.row-col-form {
  display: inline-flex;
  /* margin: 0 auto; */
}
.seatNumber {
  font-size: 12px;
}
.seat-block {
  width: 20px;
  height: 20px;
  margin: 0 auto;
}
#seatblock {
  display: inline-block;
  width: 2.5em;
  height: 2.5em;
  /* overflow:hidden; */
}

input[type="checkbox"] {
  width: 20px;
  height: 20px;
  background-color: #fff;
  appearance: none;
  -webkit-appearance: none;
  -o-appearance: none;
  -moz-appearance: none;
  border: 1px rgb(170, 169, 169) dashed;
  /* border-radius: 2px; */
  outline: none;
}
input[type="checkbox"]:checked {
  background: url("../assets/seat-empty.png") no-repeat;
  background-size: 20px 20px;
}
</style>
