<template>
  <div>
    <!--  创建纪念日  -->
    <el-card class="create">
      <el-descriptions title="我的倒计时" :column="2">
        <template slot="extra">
          <div>
            <el-button class="task-button" icon="el-icon-circle-plus-outline" type="primary" size="small"
              @click="onSubmit">创建
            </el-button>
          </div>
        </template>
      </el-descriptions>
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="倒计日名称">
          <el-input v-model="form.content" show-word-limit maxlength="8"></el-input>
        </el-form-item>
        <el-form-item label="日期">
          <el-col :span="11">
            <el-date-picker type="date" placeholder="选择日期" v-model="form.deadline" style="width: 100%;"
              value-format="yyyy-MM-dd"></el-date-picker>
          </el-col>
        </el-form-item>
      </el-form>
      <!--  纪念日展示  -->
    <el-scrollbar class="scrollMenuBox">
      <el-row>
        <el-col class="card-item-col" v-for="d in daylist" :key="d.id">
          <el-card class="card-item">

            <div v-if="Compute(d.deadline) < 0">距离{{ d.content }}
              <span class="close">
                <i class="el-icon-close" @click="Delete(d.id)"></i>
              </span>
              <div>还有{{ Math.abs(Compute(d.deadline)) }}天</div>
            </div>

            <div v-if="Compute(d.deadline) > 0">距离{{ d.content }}
              <span class="close">
                <i class="el-icon-close" @click="Delete(d.id)"></i>
              </span>
              <div>已经过去了{{ Math.abs(Compute(d.deadline)) }}天</div>
            </div>

            <div v-if="Compute(d.deadline) == 0">{{ d.content }}
              <span class="close">
                <i class="el-icon-close" @click="Delete(d.id)"></i>
              </span>
              <div class="day-difference">就在今天！</div>
            </div>

          </el-card>
        </el-col>
      </el-row>
    </el-scrollbar>
    </el-card>

    
  </div>
</template>

<script>
import moment from 'moment'
import 'moment/locale/zh-cn'

export default {
  name: "CountDown",
  data() {
    return {
      studentID: localStorage.getItem("id"),
      daylist: [],
      form: {
        content: '',
        deadline: '',
      }
    }
  },
  methods: {
    Compute(day) {
      let now = new Date();
      now = moment(now).format("YYYY-MM-DD");
      day = moment(day).format("YYYY-MM-DD");
      let dif = this.DateDiff(now, day);
      return dif;
    },
    getCountdownInfo() {
      this.$axios({
        method: "get",
        url: "api/countdown/list/" + this.studentID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        res.data.all_countdowns.forEach(item => {
          item.edit = false;
        });
        this.daylist = res.data.all_countdowns;
        // console.log(this.daylist);
      }).catch(err => {
        console.log(err);
      })
    },
    onSubmit() {
      this.$axios({
        method: "post",
        url: "api/countdown/create",
        headers: {
          "Content-Type": "application/json"
        },
        data: {
          studentID: this.studentID,
          content: this.form.content,
          deadline: this.form.deadline,
        }
      }).then(res => {
        // console.log(res.data);
        if (res.data.status == 0) {
          this.$message.error("新建失败");
        } else {
          this.$message({
            type: 'success',
            message: '新建成功'
          });
          this.getCountdownInfo();
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("新建失败");
      })
    },
    DateDiff(sDate1, sDate2) {    //sDate1和sDate2是2006-12-18格式
      var aDate, oDate1, oDate2, iDays
      aDate = sDate1.split("-")
      oDate1 = new Date(aDate[0], aDate[1], aDate[2])    //转换为12-18-2006格式
      aDate = sDate2.split("-")
      oDate2 = new Date(aDate[0], aDate[1], aDate[2])
      iDays = parseInt((oDate1 - oDate2) / 1000 / 60 / 60 / 24)    //把相差的毫秒数转换为天数
      // console.log(iDays, 'ts');
      return iDays;
    },
    Delete(id) {
      this.$axios({
        method: "delete",
        url: "api/countdown/" + id,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        // console.log(res);
        this.getCountdownInfo();
        if (res.data.status == 0) {
          this.$message.error("删除失败");
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("删除失败");
      })
    },
    // editContent(index) {
    //   this.daylist[index].edit = !this.daylist[index].edit;
    // },
    // updateItem(index) {
    //   this.$axios({
    //     method: "put",
    //     url: "api/countdown/" + this.daylist[index].id,
    //     headers: {
    //       "Content-Type": "application/json"
    //     },
    //     params: {
    //       content: this.daylist[index].content
    //     }
    //   }).then(res => {
    //     // console.log(res);
    //     this.getCountdownInfo();
    //     if (res.data.status == 0) {
    //       this.$message.error("操作失败");
    //     }
    //   }).catch(err => {
    //     console.log(err);
    //     this.$message.error("操作失败");
    //   })
    // },
    // ellipsis(value) {
    //   if (!value) return "";
    //   if (value.length > 10) {
    //     return value.slice(0, 10) + "...";
    //   }
    //   return value;
    // }
  },
  mounted() {
    this.getCountdownInfo();
  }
}
</script>

<style scoped>
.create {
  width: 90%;
  height: 360px;
  padding: 10px;
  margin-bottom: 20px;
}

.scrollMenuBox {
  height: 180px;
}

.card-item-col {
  width: 45%;
  margin: 0 10px 10px 0;
}
.card-item {
  width: 100%;
  height: 70px;
  position: relative;
  background-color: cornsilk;
}

.card-item .close {
  position: absolute;
  top: 2px;
  right: 2px;
}

.card-item .content {
  position: center;
  padding-top: 1px;
}
</style>
