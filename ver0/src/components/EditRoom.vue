<template>
    <div class="new-room">
      <h1>修改自习室</h1>
      <div class="room-form">
        <el-form label-width="25%" :label-position="left">
          <el-form-item label="自习室名称">
          <el-input v-model="StudyRoom.studyRoomName" class="name"></el-input>
        </el-form-item>
        <el-form-item label="自习室简介">
          <el-input
            v-model="StudyRoom.additional_intro"
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
            @change="changeRows"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="列数">
          <el-input-number
            v-model="cols"
            :min="1"
            label="请输入数量"
            class="number"
            @change="changeRows"
          ></el-input-number>
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
              <br/>
              <div
                class="seatNumber"
                v-if="checkedVec[rowIndex][colIndex] == 1"
                >{{ seatVec[rowIndex][colIndex] }}</div
              >
            </td>
          </tr>
        </table>
      </el-card>
      <el-divider></el-divider>
      <el-form>
        <el-form-item>
          <el-button type="primary submit" @click="editRoom">提交</el-button>
        </el-form-item>
      </el-form>
      </div>
    </div>
  </template>
  
  <script>
  import Vue from 'vue';
  import axios from "axios";
  Vue.prototype.$axios=axios;
  
  export default {
    name: "EditRoom",
    // props: ["merchantID"],
    data() {
      console.log(this.$route.query);
      return {
        StudyRoom: {
          studyRoomName: "",
          additional_intro: "",
          seatTable: []
        },
        rows: 0,
        cols: 0,
        checkedVec: [],
        seatVec: [],
        seatNumber: 0,
        merchantID: this.$route.query.merchantId,
        studyRoomId: this.$route.query.studyRoomId,
      };
    },
    methods: {
      changeRows() {
        if (this.rows > 0) this.updateRoomSize();
      },
      changeCols() {
        if (this.cols > 0) this.updateRoomSize();
      },
      updateRoomSize() {
        if (this.rows > 0 && this.cols > 0) {
          this.checkedVec = Array(this.rows)
            .fill(false)
            .map(() => Array(this.cols).fill(false));
          this.seatVec = Array(this.rows)
            .fill(0)
            .map(() => Array(this.cols).fill(0));
        } else {
          this.checkedVec = [];
          this.seatVec = [];
        }
        this.seatNumber = 0;
      },
      editRoom() {
        let data = {
          name: this.StudyRoom.studyRoomName,
          seatTable: JSON.stringify(this.seatVec),
          additional_intro: this.StudyRoom.additional_intro
        };
        this.$axios({
          method: "put",
          url: "api/studyroom/" + this.studyRoomId,
          params: data,
        }).then(res => {
          if (res.data.status == 1) {
            this.$message({
              message: "修改成功",
              type: "success"
            });
            this.$router.push({path:'/merchantmanage'});
          } else this.$message({
            message: "修改失败",
            type: "error"
          })
        });
      },
      updateRoomVec(row, col) {
        this.seatNumber += this.checkedVec[row][col] ? 1 : -1;
        // correct other seat number
        if (!this.checkedVec[row][col] && this.seatVec[row][col]) {
          this.seatVec.forEach((rowVec, rowIndex) => {
            rowVec.forEach((colVec, colIndex) => {
              if (this.seatVec[rowIndex][colIndex] > this.seatVec[row][col]) {
                this.seatVec[rowIndex][colIndex] -= 1;
              }
            });
          });
          this.seatVec[row][col] = 0;
        } else if (this.checkedVec[row][col])
          this.seatVec[row][col] = this.seatNumber;
      },
    getStudyRoom() {
      this.$axios({
        method: "get",
        url: "api/seat/list/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        this.StudyRoom = res.data.StudyRoomList.find(item => {
          return item.studyRoomID == this.studyRoomId;
        }); // studyRoomName,seatTable,additional_intro
        this.rows = this.StudyRoom.seatTable.length;
        this.cols = this.StudyRoom.seatTable[0].length;
        this.updateRoomSize();
        this.StudyRoom.seatTable.forEach((rowVec, rowIndex) => {
          rowVec.forEach((colVec, colIndex) => {
            this.seatVec[rowIndex][colIndex] = colVec.id;
            if (colVec.id) {
              this.checkedVec[rowIndex][colIndex] = true;
              this.seatNumber += 1;
            }
          });
        });
      }).catch(err => {
        console.log(err);
      })
    }
  },
    created() {
      this.getStudyRoom();
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
  