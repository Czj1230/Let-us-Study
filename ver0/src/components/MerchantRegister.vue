<template>
  <div class="loginbody">
    <div class="logindata">
      <div class="logintext">
        <h2>商户注册</h2>
      </div>
      <div class="formdata">
        <el-form ref="form" :model="form" :rules="rules">
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              clearable
              placeholder="请输入用户名"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              clearable
              placeholder="请输入密码"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="form.email"
              clearable
              placeholder="请输入邮箱"
              show-mail
            ></el-input>
          </el-form-item>
          <el-form-item label="联系方式" prop="phone_number">
            <el-input
              v-model="form.phone_number"
              placeholder="请输入手机号"
              type="number"
              maxlength="11"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div class="butt">
        <el-button class="shou" @click="register">注册</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MerchantRegister",
  data() {
    return {
      form: {
        password: "",
        username: "",
        email: "",
        phone_number: ""
      },
      checked: false,
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" }
        ],
        email: [
          { required: true, message: "请填写邮箱", trigger: "blur" },
          {
            type: "string",
            message: "邮箱格式不正确",
            trigger: "blur",
            transform(value) {
              if (
                !/^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/.test(
                  value
                )
              ) {
                return true;
              } else {
              }
            }
          },
          {
            type: "string",
            message: "长度不能超过30位",
            trigger: "blur",
            max: 30
          }
        ],
        phone_number: [
          { required: false, message: "请输入密码", trigger: "blur" },
          { max: 11, min: 11, message: "请输入有效的手机号", trigger: "blur" }
        ]
      }
    };
  },
  mounted() {
    if (localStorage.getItem("news")) {
      this.form = JSON.parse(localStorage.getItem("news"));
      this.checked = true;
    }
  },
  methods: {
    register(form) {
      let data = {
        username: this.form.username,
        password: this.form.password,
        email: this.form.email,
        phone_number: this.phone_number
      };
      console.log(data);
      this.$axios({
        method: "post",
        url: "api/merchant/insert",
        data: data,
        header: {
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("res", res);
        this.$router.push({
          path: "/merregisterres",
          query: {
            status: res.data.status
          }
        });
      });
    }
  }
};
</script>

<style scoped>
.loginbody {
  width: 100%;
  height: 100%;
  background-image: url("../assets/bg.jpg");
  background-size: cover ;
  background-position: center center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  position: absolute;
}

.logintext {
  margin-top: 5px;
  line-height: 0px;
  text-align: center;
  font-size: 30px;
  font-weight: bolder;
  color: white;
  text-shadow: 2px 2px 4px #000000;
}

.logindata {
  width: 450px;
  height: 610px;
  background-color: rgba(208, 227, 250, 0.7);
  border-radius: 30px;

  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.formdata {
  top: 0;
  padding: 32px;
  position: static;

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
