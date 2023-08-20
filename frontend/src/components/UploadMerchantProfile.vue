<template>
  <div>
    <h1>上传缩略图</h1>
    <el-upload
      v-model="fileList"
      ref="uploadref"
      action="#"
      :auto-upload="false"
      list-type="picture-card"
      :file-list="fileList"
      :limit="1"
      :on-change="handleChange"
      :on-remove="handleRemove"
    >
      <i class="el-icon-plus"></i>
    </el-upload>
    <el-dialog v-model="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="" />
    </el-dialog>
    <br>
    <el-button type="primary" @click="handleClick">上传图片</el-button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fileList: [],
      dialogImageUrl: '',
      dialogVisible: false,
      fileParam: '',
      image: '',
      merchantId: localStorage.getItem("id"),
    };
  },
  methods: {
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    // handlePictureCardPreview(file) {
    //   this.dialogImageUrl = file.url;
    //   console.log(this.dialogImageUrl);
    //   this.dialogVisible = true;
    // },
    handleChange(file) {
      this.fileParam = new FormData(); //创建form对象
      this.fileParam.append("image", file.raw);
      // this.fileParam.append("merchantId", this.$route.query.merchantId);
      this.fileParam.append("merchantId", this.merchantId);
    },
    handleClick() {
      this.$axios({
        url: '/api/merchant/uploadImg',
        data: this.fileParam,
        method: 'post',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
      }).then(res => {
        // console.log(res);
        alert('上传成功');
      }
      )
    }
  }
}
</script>

<<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
