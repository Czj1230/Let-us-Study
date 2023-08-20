<template>
  <div>
    <el-descriptions title="我的日程表">
      </el-descriptions>
    <FullCalendar ref="Calendar" :options="calendarOptions" />
    <el-dialog :visible.sync="dialogFormVisible">
      <el-form class="demo-form-inline">
        <el-form-item label="事件名">
          <el-input v-model="eventItem.title" v-on:change="onChange('title')"></el-input>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="eventItem.date"
            v-on:change="onChange('date')"
            type="datetimerange"
            unlink-panels
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          >
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button v-if="isAdd === false" @click="deleteEvent">删 除</el-button>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button v-if="isAdd === true" type="primary" @click="add"
          >确 定</el-button
        >
        <el-button v-else type="primary" @click="update">确认修改</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import "@fullcalendar/core/vdom"; // solves problem with Vite
import FullCalendar from "@fullcalendar/vue";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

export default {
  // https://blog.csdn.net/qq_41460077/article/details/121158394
  name: "Calendar",
  components: {
    FullCalendar
  },
  data() {
    return {
      studentID: -1,
      dialogFormVisible: false,
      eventItem: {
        id: 0,
        title: "",
        date: "",
        changed: []
      },
      maxid: 0,
      isAdd: true,
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            }
          }
        ]
      },
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
        initialView: "dayGridMonth",
        locale: "zh",
        firstDay: 1,
        buttonText: {
          today: "今天",
          month: "月",
          week: "周",
          day: "日",
          list: "周列表"
        },
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay listWeek"
        },
        events: [],
        // datesSet: this.datesSet,
        eventClick: this.eventClick,
        dateClick: this.handleDateClick
      }
    };
  },
  created() {
    this.getEvents();
  },
  methods: {
    getEvents() {
      this.studentID = parseInt(localStorage.getItem("id"));
      this.$axios({
        method: "get",
        url: "/api/timetable/list/" + this.studentID
      })
        .then(res => {
          this.calendarOptions.events = [];
          res.data.all_timetables.forEach((ele)=>{
            this.calendarOptions.events.push({
              id: ele.id,
              title: ele.content,
              start: ele.starttime,
              end: ele.endtime,
              color: "#ffcc99",
            })
          });
        })
        .catch(err => {
          console.log(err);
        });
    },
    eventClick(info) {
      this.eventItem = {
        id: info.event.id,
        title: info.event.title,
        date: [info.event.start, info.event.end],
        changed: []
      };
      this.isAdd = false;
      this.dialogFormVisible = true;
    },
    onChange(key) {
      this.eventItem.changed.push(key);
    },
    checkChange() {
      var changedItem = {};
      this.eventItem.changed.forEach((key)=>{
        if (key === "date") {
          changedItem.starttime = this.eventItem.date[0];
          changedItem.endtime = this.eventItem.date[1];
        } else {
          changedItem["content"] = this.eventItem[key];
        }
      })
      return changedItem;
    },
    handleDateClick(arg) {
      this.isAdd = true;
      // 显示添加弹出框
      this.dialogFormVisible = true;
      // 把当前点击的数据保留
      // this.arg = arg;
    },
    add() {
      // 添加
      let data = {
        studentID: this.studentID,
        content: this.eventItem.title,
        starttime: this.eventItem.date[0],
        endtime: this.eventItem.date[1],
      };
      this.$axios({
        method: "post",
        url: "api/timetable/create",
        data: data,
        header: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        if (res.data.status == 1) {
          this.getEvents();
        } else {
          this.$message.error(res.data.msg);
          alert("error");
        }
      });
      this.eventItem = {
        title: "",
        start: "",
        end: "",
        changed: []
      };
      this.dialogFormVisible = false;
    },
    deleteEvent() {
      this.$axios({
        method: "delete",
        url: "api/timetable/" + this.eventItem.id
      }).then(res => {
        if (res.data.status == 1) {
          this.getEvents();
        } else {
          this.$message.error(res.data.msg);
          alert("error");
        }
      });
      this.eventItem = {
        title: "",
        start: "",
        end: "",
        changed: []
      };
      this.dialogFormVisible = false;
    },
    update() {
      const changed = this.checkChange();
      this.$axios({
        method: "put",
        url: "api/timetable/"+this.eventItem.id,
        params: changed
    }).then(res => {
        if (res.data.status == 1) {
          this.getEvents();
        } else {
          this.$message.error(res.data.msg);
          alert("error");
        }
      });
      // this.calendarOptions.events = this.calendarOptions.events.map(item => {
      //   if (item.id == this.eventItem.id) {
      //     item.title = this.eventItem.title;
      //     item.start = this.eventItem.date[0];
      //     item.end = this.eventItem.date[1];
      //   }
      //   return item;
      // });
      this.eventItem = {
        title: "",
        start: "",
        end: "",
        changed: []
      };
      this.dialogFormVisible = false;
    }
  }
};
</script>
<style scoped>
/* @import "~@fullcalendar/core/main.min.css"; */
/* @import "~@fullcalendar/daygrid/main.css"; */
/* @import "~@fullcalendar/timegrid/main.css"; */
</style>
