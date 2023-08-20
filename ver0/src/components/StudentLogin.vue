<template>
  <div class="loginbody">
    <div class="logindata">
      <div class="logintext">
        <h2>学生登录</h2>
      </div>
      <div class="formdata">
        <el-form ref="form" :model="form" :rules="rules">
          <el-form-item prop="username">
            <el-input v-model="form.username" clearable placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="form.password" clearable placeholder="请输入密码" show-password></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div class="tool">
        <div>
          <el-checkbox v-model="checked" @change="remember">记住密码</el-checkbox>
        </div>
        <div>
          <span class="shou" @click="forgetpas">忘记密码？</span>
        </div>
      </div>
      <div class="butt">
        <el-button type="primary" @click.native.prevent="login('form')">登录</el-button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "StudentLogin",
  data() {
    return {
      form: {
        password: "",
        username: "",
      },
      checked: false,
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" },
        ],
      },
    };
  },
  mounted() {
    if (localStorage.getItem("news")) {
      this.form = JSON.parse(localStorage.getItem("news"))
      this.checked = true
    }
  },
  methods: {
    login(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          // login(this.form)
          let data = {
            username: this.form.username,
            password: this.form.password,
          };
          console.log(data);
          this.$axios({
            method: "post",
            url: "api/tokens/stu_token",
            auth: data,
            header: {
              'Content-Type': 'application/json'
            }
          })
            .then((res) => {
              // console.log(res);
              if (res.status == 200) {
                localStorage.setItem("status", 1); // 1-stu,2-merchant
                localStorage.setItem("token", res.data.token);
                localStorage.setItem("id", res.data.id);
                localStorage.setItem("name", this.form.username);
                this.$message({
                  message: "登录成功啦",
                  type: "success",
                  showClose: true,
                });
                // this.$router.replace("/merchantlist");
                this.$router.push({ path: "merchantlist" });
              } else {
                this.$message({
                  message: "账户名或密码错误",
                  type: "error",
                  showClose: true,
                });
              }
            })
            .catch((err) => {
              this.$message({
                message: "账户名或密码错误",
                type: "error",
                showClose: true,
              });
            });
        } else {
          return false;
        }
      });
    },
    remember(data) {
      this.checked = data
      if (this.checked) {
        localStorage.setItem("news", JSON.stringify(this.form))
      } else {
        localStorage.removeItem("news")
      }
    },
    forgetpas() {
      this.$message({
        type: "info",
        message: "功能尚未开发额😥",
        showClose: true
      })
    },
    register() { },
  },
};
</script>

<style scoped>
.loginbody {
  width: 100%;
  height: 100%;
  background-image: url("../assets/bg.jpg");
  background-size: cover;
  background-position: center center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  position: absolute;
}

.logintext {
  margin-bottom: 20px;
  line-height: 50px;
  text-align: center;
  font-size: 30px;
  font-weight: bolder;
  color: white;
  text-shadow: 2px 2px 4px #000000;
}

.logindata {
  width: 450px;
  height: 400px;
  background-color: rgba(208, 227, 250, 0.7);
  border-radius: 30px;

  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.formdata {
  padding: 32px;
  position: static;
  bottom: 0;
  width: 100%;
  box-sizing: border-box;
}

.tool {
  display: flex;
  justify-content: space-between;
  color: #606266;
}

.butt {
  margin-top: 10px;
  text-align: center;
}

.shou {
  cursor: pointer;
  color: #606266;
}

/*ui*/
/* /deep/ .el-form-item__label {
  font-weight: bolder;
  font-size: 15px;
  text-align: left;
}

/deep/ .el-button {
  width: 100%;
  margin-bottom: 10px;

} */
</style>

