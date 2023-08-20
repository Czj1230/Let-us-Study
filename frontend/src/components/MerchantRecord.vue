<template>
  <div>
    <div>
      <el-table ref="singleTable" :data="new_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="新建订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column label="预约人id" property="studentId"></el-table-column>
          <el-table-column label="自习室名称" property="roomName"></el-table-column>
          <el-table-column label="座位序号" property="seatId"></el-table-column>
          <el-table-column label="预约座位时间" property="startTime"></el-table-column>
          <el-table-column label="订单终止时间" property="endTime"></el-table-column>
          <el-table-column label="订单操作" property="state">
            <template slot-scope="scope">
              <el-button @click="CheckIn(scope.row.recordId)">签到</el-button>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-table ref="singleTable" :data="active_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="进行中订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column label="预约人id" property="studentId"></el-table-column>
          <el-table-column label="自习室名称" property="roomName"></el-table-column>
          <el-table-column label="座位序号" property="seatId"></el-table-column>
          <el-table-column label="预约座位时间" property="startTime"></el-table-column>
          <el-table-column label="订单终止时间" property="endTime"></el-table-column>
          <el-table-column label="订单操作" property="state">
            <template slot-scope="scope">
              <el-button type='info' @click="CheckOut(scope.row.recordId)">签离</el-button>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-table ref="singleTable" :data="end_records" border class="recordtable" highlight-current-row
                :header-cell-style="{ textAlign: 'center' }"
                max-height="400px" @current-change="handleCurrentChange" :key="randomUpdateKey">
        <el-table-column label="已完成订单">
          <el-table-column label="序号" type="index"></el-table-column>
          <el-table-column label="预约人id" property="studentId"></el-table-column>
          <el-table-column label="自习室名称" property="roomName"></el-table-column>
          <el-table-column label="座位序号" property="seatId"></el-table-column>
          <el-table-column label="预约座位时间" property="startTime"></el-table-column>
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
          <el-table-column label="预约人id" property="studentId"></el-table-column>
          <el-table-column label="自习室名称" property="roomName"></el-table-column>
          <el-table-column label="座位序号" property="seatId"></el-table-column>
          <el-table-column label="预约座位时间" property="startTime"></el-table-column>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MerchantRecord',
  data() {
    return {
      merchantID: localStorage.getItem("id"),
      records: [],
      currentRow: null,
      randomUpdateKey: 0,
      end_records: [],
      scrap_records: [],
      active_records: [],
      new_records: [],
    }
  },
  methods: {
    handleCurrentChange(val) {
      this.currentRow = val;
    },
    getMerchantRecord() {
      // this.merchantID = this.$route.query.merchantId;
      this.$axios({
        method: "get",
        url: "api/order/listForMerchant/" + this.merchantID,
        headers: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log(res.data);
        this.clear();
        this.EndRecord(res.data.records);
        this.NewRecord(res.data.records);
        this.ScrapRecord(res.data.records);
        this.ActiveRecord(res.data.records);
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
    },
    NewRecord(records) {
      for (let i = 0; i < records.length; i++)
        if (records[i].state == 'new') this.new_records.push(records[i]);
    },
    EndRecord(records) {
      for (let i = 0; i < records.length; i++)
        if (records[i].state == 'end') this.end_records.push(records[i]);
    },
    ScrapRecord(records) {
      for (let i = 0; i < records.length; i++)
        if (records[i].state == 'scrap') this.scrap_records.push(records[i]);
    },
    ActiveRecord(records) {
      for (let i = 0; i < records.length; i++)
        if (records[i].state == 'active') this.active_records.push(records[i]);
    },
    CheckIn(id) {
      this.$axios({
        method: "post",
        url: "api/order/signIn",
        headers: {
          "Content-Type": "application/json"
        },
        data: {
          recordId: id,
          state: 'active'
        }
      }).then(res => {
        // console.log(res.data);
        this.getMerchantRecord();
        if (res.data.status === 1) {
          this.$message({
            type: 'success',
            message: '订单签到成功！'
          });
          this.$forceUpdate();
        } else {
          this.$message.error('订单签到失败');
        }
      }).catch(err => {
        console.log(err);
        this.$message.error('订单签到失败');
      })
    },
    CheckOut(id) {
      this.$axios({
        method: "post",
        url: "api/order/signIn",
        headers: {
          "Content-Type": "application/json"
        },
        data: {
          recordId: id,
          state: 'end'
        }
      }).then(res => {
        // console.log(res.data);
        this.getMerchantRecord();
        if (res.data.status === 1) {
          this.$message({
            type: 'success',
            message: '订单签离成功！'
          });
        } else {
          this.$message.error('订单签离失败');
        }
      }).catch(err => {
        console.log(err);
        this.$message.error('订单签离失败');
      })
    },
  },
  mounted() {
    this.getMerchantRecord();
  },
  activated() {
    this.getMerchantRecord();
  }
}
</script>

<style>
.recordtable {
  padding: 10px;
  position: center;
  margin: 20px;
}

</style>
