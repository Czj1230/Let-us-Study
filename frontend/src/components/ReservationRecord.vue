<template>
  <div>
    <div>
      <el-table ref="singleTable" :data="new_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="新建订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column property="merchantShowName" label="商户名称"></el-table-column>
          <el-table-column property="merchantLocation" label="商户地址"></el-table-column>
          <el-table-column property="roomName" label="自习室名称"></el-table-column>
          <el-table-column property="seatId" label="座位序号"></el-table-column>
          <el-table-column property="startTime" label="预约座位时间"></el-table-column>
        </el-table-column>
      </el-table>
    </div>

    <div>
      <el-table ref="singleTable" :data="active_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="进行中订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column property="merchantShowName" label="商户名称"></el-table-column>
          <el-table-column property="merchantLocation" label="商户地址"></el-table-column>
          <el-table-column property="roomName" label="自习室名称"></el-table-column>
          <el-table-column property="seatId" label="座位序号"></el-table-column>
          <el-table-column property="startTime" label="预约座位时间"></el-table-column>
        </el-table-column>
      </el-table>
    </div>

    <div>
      <el-table ref="singleTable" :data="end_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="未评价订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column property="merchantShowName" label="商户名称"></el-table-column>
          <el-table-column property="merchantLocation" label="商户地址"></el-table-column>
          <el-table-column property="roomName" label="自习室名称"></el-table-column>
          <el-table-column property="seatId" label="座位序号"></el-table-column>
          <el-table-column property="startTime" label="预约座位时间"></el-table-column>
          <el-table-column label="订单终止时间" property="endTime"></el-table-column>
          <el-table-column property="state" label="订单操作">
            <template slot-scope="scope">
              <el-button @click="makeComment(scope.row.recordId)">评价</el-button>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
    </div>

    <div>
      <el-table ref="singleTable" :data="end_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="已评价订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column property="merchantShowName" label="商户名称"></el-table-column>
          <el-table-column property="merchantLocation" label="商户地址"></el-table-column>
          <el-table-column property="roomName" label="自习室名称"></el-table-column>
          <el-table-column property="seatId" label="座位序号"></el-table-column>
          <el-table-column property="startTime" label="预约座位时间"></el-table-column>
          <el-table-column label="订单终止时间" property="endTime"></el-table-column>
        </el-table-column>
      </el-table>
    </div>

    <div>
      <el-table ref="singleTable" :data="scrap_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="废弃订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column property="merchantShowName" label="商户名称"></el-table-column>
          <el-table-column property="merchantLocation" label="商户地址"></el-table-column>
          <el-table-column property="roomName" label="自习室名称"></el-table-column>
          <el-table-column property="seatId" label="座位序号"></el-table-column>
          <el-table-column property="startTime" label="预约座位时间"></el-table-column>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog title="订单评价" :visible.sync="dialogTableVisible" width="30%">
      <el-form>
        <el-form-item label="设施使用方便程度" label-width="40%">
          <el-rate v-model="facility" show-score text-color="#ff9900"></el-rate>
        </el-form-item>
        <el-form-item label="环境安静度" label-width="40%">
          <el-rate v-model="quietness" show-score text-color="#ff9900"></el-rate>
        </el-form-item>
        <el-form-item label="环境舒适度" label-width="40%">
          <el-rate v-model="confortLevel" show-score text-color="#ff9900"></el-rate>
        </el-form-item>
        <el-form-item label="评论">
          <el-input
            type="textarea"
            placeholder="请输入内容"
            v-model="comment"
            maxlength="30"
            show-word-limit
          >
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>

export default {
  name: 'ReservationRecord',
  data() {
    return {
      studentID: localStorage.getItem("id"),
      Records: [],
      currentRow: null,
      dialogTableVisible: false,
      comment: '',
      commentId: 0,
      facility: 0,
      quietness: 0,
      confortLevel: 0,
      randomUpdateKey: 0,
      end_records: [],
      scrap_records: [],
      active_records: [],
      new_records: [],
      commented_records: [],
    }
  },
  methods: {
    handleCurrentChange(val) {
      this.currentRow = val;
    },
    getReservationRecord() {
      // this.studentID = this.$route.query.studentId;
      this.$axios({
        method: "get",
        url: "api/order/listForStudent/" + this.studentID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log(res.data);
        this.clear();
        this.MakeRecord(res.data.records);
        this.randomUpdateKey = Math.random();
      }).catch(err => {
        console.log(err);
      })
    },
    clear() {
      this.end_records = [];
      this.scrap_records = [];
      this.active_records = [];
      this.new_records = [];
      this.commented_records = [];
    },
    MakeRecord(records) {
      for (let i = 0; i < records.length; i++)
        if (records[i].state == 'new') this.new_records.push(records[i]);
        else if (records[i].state == 'end')
          if (records[i].commented == false)
            this.end_records.push(records[i]);
          else
            this.commented_records.push(records[i])
        else if (records[i].state == 'scrap') this.scrap_records.push(records[i]);
        else this.active_records.push(records[i]);
    },
    makeComment(id) {
      this.commentId = id;
      this.dialogTableVisible = true;
    },
    submit() {
      this.$axios({
        method: "post",
        url: "api/order/comment",
        headers: {
          "Content-Type": "application/json"
        },
        data: {
          recordId: this.commentId,
          comment: this.comment,
          facility: this.facility,
          quietness: this.quietness,
          confortLevel: this.confortLevel,
        }
      }).then(res => {
        console.log(res.data);
        this.$message({
          type: 'success',
          message: '评论提交成功！',
        });
        this.dialogTableVisible = false;
        this.getReservationRecord();
      }).catch(err => {
        console.log(err);
        this.$message({
          type: 'info',
          message: '评论提交失败，请再次提交'
        });
      });
    }
  },
  mounted() {
    this.getReservationRecord();
  },
  activated() {
    this.getReservationRecord();
  }
}
</script>

<style>
.recordtable {
  position: center;
  margin-bottom: 20px;
}

</style>
