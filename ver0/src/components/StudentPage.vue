<template>
  <div>
    <el-row>
      <el-col :span="12">
        <TodoList></TodoList>
      </el-col>
      <el-col :span="12">
        <CountDown></CountDown>
      </el-col>
    </el-row>
    <el-card class="calendar-card">
      <Calendar></Calendar>
      <!-- <el-col></el-col> -->
    </el-card>
    <!-- <Calendar></Calendar> -->
  </div>

</template>

<script>
import Calendar from './Calendar';
import CountDown from "./CountDown";
import TodoList from './TodoList';
export default {
  name: "StudentPage",
  components: { CountDown, Calendar, TodoList },
}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
  height: 400px;
  margin-left: 5%;
}

.el-col {
  border-radius: 4px;
}

.calendar-card {
  /* padding: 50px; */
  width: 90%;
  margin-left: 5%;
  padding: 10px;
  text-align: left;
}
</style>
