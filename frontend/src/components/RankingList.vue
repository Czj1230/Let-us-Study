<template>
  <div>
    <el-table height="600px" :default-sort = "{prop: 'score', order: 'descending'}"
              ref="singleTable" :data="rankinglist" highlight-current-row @current-change="handleCurrentChange" border
              class="recordtable" :key="randomUpdateKey">
      <el-table-column type="index" label="名次"></el-table-column>
      <el-table-column property="name" label="用户名"></el-table-column>
      <el-table-column property="score" label="积分"></el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'RankingList',
  data() {
    return {
      rankinglist: [],
      currentRow: null,
      randomUpdateKey: 0,
    }
  },
  methods: {
    handleCurrentChange(val) {
      this.currentRow = val;
    },
    getRankingList() {
      this.$axios({
        method: "get",
        url: "api/student/getRanking",
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log(res.data);
        this.rankinglist = res.data.rankinglist;
        this.randomUpdateKey = Math.random();
      }).catch(err => {
        console.log(err);
      })
    },
  },
  mounted() {
    this.getRankingList();
  },
}
</script>

<style>
.recordtable {
  padding: 5px;
  position: center;
}

</style>
