<template>
  <div class="loginbody">
    <div class="logindata">
      <div class="logintext">
        <h2>学生注册</h2>
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
          <el-form-item label="性别" prop="gender">
            <el-radio v-model="form.gender" label="M">男</el-radio>
            <el-radio v-model="form.gender" label="F">女</el-radio>
          </el-form-item>
          <el-form-item label="出生日期" prop="birthday">
            <el-date-picker
              v-model="form.birthday"
              type="date"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              placeholder="选择日期"
              @input="$forceUpdate()"
              :picker-options="pickerOptions">
            </el-date-picker>
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
import Vue from 'vue';
import axios from "axios";
Vue.prototype.$axios=axios;

export default {
  name: "StudentRegister",
  data() {
    console.log(this.$route.params);
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
      },
      form: {
        password: "",
        username: "",
        email:"",
        gender:"",
        birthday:"",
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
        email: [
          { required: true, message: '请填写邮箱', trigger: 'blur' },
          { type: 'string',
            message: '邮箱格式不正确',
            trigger: 'blur',
            transform (value) {
              if (!/^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/.test(value)) {
                return true
              }else{
              }
            }
          },
          { type: 'string', message: '长度不能超过30位', trigger: 'blur', max: 30 }
        ],
      },
    };
  },
  mounted() {
    if(localStorage.getItem("news")){
      this.form=JSON.parse(localStorage.getItem("news"))
      this.checked=true
    }
  },
  methods: {
    register() {
      // console.log(this.$route.params.merchantId);
      let data = {
        username: this.form.username,
        password: this.form.password,
        email: this.form.email,
        gender:this.form.gender,
        birthday:this.form.birthday
      };
      console.log(data);
      this.$axios({
        method: "post",
        url: "api/student/insert",
        data: data,
        header:{
          'Content-Type':'application/json'
        }
      }).then(res => {
        console.log("res", res);
        this.$router.push({path: '/stdregisterres', query: {
            status: res.data.status
          }});
        if (res.data.status == 1) {
          console.log("success");
          this.$router.push({path: '/stdregisterres', query: {
              status: res.data.status
            }});
        }
        else {
          console.log("fail");
          // error msg
        }
      });
    },

  },
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
  margin-bottom: 1px;
  text-align: center;
}

.shou {
  cursor: pointer;
  color: rgba(101, 108, 117, 0.7);
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

