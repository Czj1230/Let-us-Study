<template>
  <el-card class="box-card">
    <el-descriptions title="我的待办" :column="2">
      <template slot="extra">
        <div>
          <el-button class="task-button" icon="el-icon-circle-plus-outline" type="primary" size="small"
            @click="addItem">添加
          </el-button>
        </div>
      </template>
      <el-descriptions-item label="待办项">{{ todoNum }}</el-descriptions-item>
      <el-descriptions-item label="已完成">{{ finishNum }}</el-descriptions-item>
    </el-descriptions>
    <el-input class="new-task-input" v-model="taskItem.content" placeholder="新建ToDo"></el-input>
    <el-scrollbar class="task-item-list" v-if="isShow">
      <el-row class="task-item-line" v-for="(item, index) in taskList" :key="item.id" @scroll="true">
        <el-col :xs="2" :sm="1" :md="1" :xl="1">
          <el-checkbox v-model="item.checked" @change="changeState(index)"></el-checkbox>
        </el-col>
        <el-col class="task-item-content" :xs="12" :sm="15" :md="15" :xl="15">
          <span v-show="!item.edit" :class="{ 'checked': item.checked, 'topped': item.sequence }"
            @dblclick="editItem(index)">{{ item.content }}</span>
          <el-input v-show="item.edit" v-model="item.content"></el-input>
        </el-col>
        <el-col :xs="4" :sm="4" :md="4" :xl="2">
          <i v-if="item.edit" class="el-icon-check" @click="updateItem(index)"></i>
          <i v-if="!item.edit" :class="{ 'el-icon-top': !item.sequence, 'el-icon-bottom': item.sequence }"
            @click="topItem(index)"></i>
          <i class="el-icon-close" @click="deleteItem(index)"></i>
        </el-col>
      </el-row>
      <el-empty v-if="!taskList.length" :image-size="50" description="暂无待办"></el-empty>
    </el-scrollbar>
    <el-skeleton v-else :rows="4" class="task-item-list" animated />
  </el-card>
</template>
<script>
export default {
  name: "TodoList",
  data() {
    return {
      studentID: localStorage.getItem("id"),
      taskList: [],
      taskItem: {
        content: '',
        checked: false,
        edit: false
      },
      isShow: false,
    }
  },
  methods: {
    getTodoListInfo() {
      this.$axios({
        method: "get",
        url: "api/todo_list/list/" + this.studentID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        res.data.all_todos.forEach(item => {
          item.edit = false;
        });
        this.taskList = res.data.all_todos;
        // console.log(this.taskList);
        this.isShow = true;
      }).catch(err => {
        console.log(err);
      })
    },
    addItem: function () {
      this.$axios({
        method: "post",
        url: "api/todo_list/create",
        headers: {
          "Content-Type": "application/json"
        },
        data: {
          studentID: this.studentID,
          content: this.taskItem.content,
          checked: false,
          sequence: 0,
        }
      }).then(res => {
        // console.log(res);
        this.getTodoListInfo();
        if (res.data.status == 0) {
          this.$message.error("添加失败");
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("添加失败");
      })
      this.taskItem.content = '';
    },
    changeState: function (index) {
      this.$axios({
        method: "put",
        url: "api/todo_list/" + this.taskList[index].id,
        headers: {
          "Content-Type": "application/json"
        },
        params: {
          checked: this.taskList[index].checked,
        }
      }).then(res => {
        // console.log(res);
        this.getTodoListInfo();
        if (res.data.status == 0) {
          this.$message.error("操作失败");
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("操作失败");
      })
    },
    editItem: function (index) {
      this.taskList[index].edit = !this.taskList[index].edit;
    },
    topItem: function (index) {
      this.$axios({
        method: "put",
        url: "api/todo_list/" + this.taskList[index].id,
        headers: {
          "Content-Type": "application/json"
        },
        params: {
          sequence: 1 - this.taskList[index].sequence
        }
      }).then(res => {
        // console.log(res);
        this.getTodoListInfo();
        if (res.data.status == 0) {
          this.$message.error("操作失败");
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("操作失败");
      })
    },
    deleteItem: function (index) {
      this.$axios({
        method: "delete",
        url: "api/todo_list/" + this.taskList[index].id,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        // console.log(res);
        this.getTodoListInfo();
        if (res.data.status == 0) {
          this.$message.error("删除失败");
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("删除失败");
      })
    },
    updateItem: function (index) {
      this.$axios({
        method: "put",
        url: "api/todo_list/" + this.taskList[index].id,
        headers: {
          "Content-Type": "application/json"
        },
        params: {
          content: this.taskList[index].content
        }
      }).then(res => {
        // console.log(res);
        this.getTodoListInfo();
        if (res.data.status == 0) {
          this.$message.error("修改失败");
        }
      }).catch(err => {
        console.log(err);
        this.$message.error("修改失败");
      })
    },
  },
  computed: {
    todoNum: function () {
      return this.taskList.filter(function (item) {
        return !item.checked;
      }).length;
    },
    finishNum: function () {
      return this.taskList.filter(function (item) {
        return item.checked;
      }).length;
    },
  },
  created() {
    this.getTodoListInfo();
  }
}
</script>
<style type="text/css">
.box-card {
  width: 90%;
  height: 360px;
  margin-bottom: 20px;
  padding: 10px;
  text-align: left;
}

.new-task-line {
  margin: 20px 0;
  display: flex;
  justify-content: space-between;
}

.el-form-item {
  margin-right: 0;
}

.task-item-list {
  height: 200px;
  margin-top: 20px;
}

.el-scrollbar__wrap
{
  overflow-x: hidden;
}

.task-item-line {
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
}

.task-item-content {
  text-align: left;
  line-height: 24px;
  font-size: 15px;
}

.checked {
  text-decoration: line-through;
  color: #999;
}

.topped {
  font-weight: bold;
}
</style>