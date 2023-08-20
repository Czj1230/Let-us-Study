<template>
  <el-card class="comment-card">
    <h3 class="comment-list">用户评论</h3>
    <div class="comment-list" v-if="isShow">
      <el-row class="comment-line"
        v-for="item in commentList.slice((currentPage - 1) * pageSize, currentPage * pageSize)" :key="item.id">
        <el-col :xs="2" :sm="2" :md="1" :xl="1">
          <el-avatar icon="el-icon-user-solid" size="small"></el-avatar>
        </el-col>
        <el-col :xs="22" :sm="22" :md="23" :xl="23">
          <div class="comment-item">
            <div class="comment-item-header">
              <div>
                <el-rate v-model="item.rate" disabled show-score text-color="#ff9900" score-template="{value}">
                </el-rate>
              </div>
              <span class="comment-item-date">{{ item.endTime }}</span>
            </div>
            <div class="comment-item-content">
              {{ item.comment }}
            </div>
          </div>
        </el-col>
      </el-row>
      <el-empty v-if="!commentList.length" :image-size="50" description="暂无评论"></el-empty>
    </div>
    <el-skeleton v-else :rows="4" class="comment-list" animated />
    <div class="block">
      <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentPage" :page-size="pageSize"
        layout="total, prev, pager, next" :total="totalComment">
      </el-pagination>
    </div>
  </el-card>
</template>
<script>
export default {
  name: "Comment",
  props: ['passvalue'],
  data() {
    return {
      merchantID: this.passvalue,
      currentPage: 1,
      commentList: [],
      totalComment: 0,
      pageSize: 3,
      isShow: false,
    };
  },
  methods: {
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    getCommentInfo() {
      // console.log(this.merchantID);
      this.$axios({
        method: "get",
        url: "api/order/comment/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        // console.log(res.data);
        res.data.records.forEach(item => {
          item.endTime = item.endTime.split("GMT")[0];
          item.rate = item.grade;
        });
        this.commentList = res.data.records;
        this.totalComment = res.data.records.length;
        this.isShow = true;
      }).catch(err => {
        console.log(err);
      })
    },
  },
  created() {
    this.getCommentInfo();
  }
}
</script>

<style scoped>
.comment-card {
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

.comment-line {
  margin: 20px 0;
}

.comment-list {
  width: 100%;
  text-align: left;
}

.comment-item-header {
  display: flex;
  justify-content: space-between;
}

.comment-item-date {
  margin-left: 15px;
  color: #999;
}

.comment-item-content {
  margin-top: 10px;
  color: #666;
  text-align: left;
}
</style>