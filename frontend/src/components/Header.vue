<template>
  <div class="menu-header">
    <div class="menu-header-left">
      <img class="logo" src="@/assets/study.png" alt />
      <span class="xueba">学吧</span>
    </div>
    <el-menu router :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect"
      text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="/" v-if="(status == null)">首页</el-menu-item>
      <el-menu-item index="/aboutxueba" v-if="(status == null)">关于学吧</el-menu-item>
      <el-menu-item index="/contactus" v-if="(status == null)">联系我们</el-menu-item>
      <el-menu-item index="/merchantlist" v-if="(status == 1)">自习室预约</el-menu-item>
      <el-menu-item index="/reservartionrecord" v-if="(status == 1)">我的预约记录</el-menu-item>
      <el-menu-item index="/rankinglist" v-if="(status == 1)">用户积分榜</el-menu-item>
      <el-menu-item index="/studentpage" v-if="(status == 1)">学生个人空间</el-menu-item>
      <el-menu-item index="/merchantmanage" v-if="(status == 2)">商户管理空间</el-menu-item>
      <el-menu-item index="/merchantrecord" v-if="(status == 2)">查看预约记录</el-menu-item>
      <!--      <el-menu-item index="/uploadmerchantprofile" v-if="status==2">上传商家图片</el-menu-item>-->
      <!--      <el-menu-item index="/merchantsetting" v-if="status==2">设置信息</el-menu-item>-->
      <!-- <el-menu-item index="/newroom" v-if="status==2"
      :route="{
        name: 'newroom',
        query: {
          merchantId: id
        }
      }">创建自习室</el-menu-item> -->
    </el-menu>

    <span class="demonstration" style="float:right;padding-top:0px;margin-right:2%">
      <el-dropdown v-if="id == null" trigger="click">
        <span class="el-dropdown-link">
          登录<i class="el-icon-caret-bottom el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="stdlog()">学生登录</el-dropdown-item>
          <el-dropdown-item @click.native="merlog()">商家登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-dropdown v-if="id == null" trigger="click">
        <span class="el-dropdown-link">
          注册<i class="el-icon-caret-bottom el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="stdreg()">学生注册</el-dropdown-item>
          <el-dropdown-item @click.native="merreg()">商家注册</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <!-- 增加用户名 -->
      <span  v-if="id != null" class="el-dropdown-link">尊敬的</span>
      <span v-if="id != null" class="el-dropdown-link-avatar">{{ name }}</span>
      <el-dropdown v-if="id != null" trigger="click">
        <span class="el-dropdown-link">
          欢迎登录<i class="el-icon-caret-bottom el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="logout()">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </span>
  </div>
</template>

<script>


export default {
  name: "Header",
}
</script>
<script>
export default {
  data() {
    return {
      id: localStorage.getItem("id"),
      status: localStorage.getItem("status"),
      name: localStorage.getItem("name"),
      activeIndex: this.$route.path,
    };
  },
  watch: {
    $route(to, from) {
      // console.log("catch route change");
      this.status = localStorage.getItem("status");
      this.id = localStorage.getItem("id");
      this.name = localStorage.getItem("name");
      // console.log("id",this.id,"status",this.status);
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      this.activeIndex = key;
      // console.log(key, keyPath);
    },
    stdlog() {
      localStorage.clear();
      this.$router.push({ path: '/studentlogin' });
    },
    stdreg() {
      localStorage.clear();
      this.$router.push({ path: '/studentregister' });
    },
    merlog() {
      localStorage.clear();
      this.$router.push({ path: '/merchantlogin' });
    },
    merreg() {
      localStorage.clear();
      this.$router.push({ path: '/merchantregister' });
    },
    logout() {
      this.id = null;
      localStorage.clear();
      this.$router.push({ path: '/' });
    }
  }
}
</script>
<style scoped>
.el-col {
  border-radius: 4px;
}

.menu-header {
  display: flex;
  justify-content: space-between;
  background-color: black;
  padding: 0;
}

.menu-header-left {
  height: 100%;
  display: flex;
  align-items: center;
}

.logo {
  width: 40px;
  margin-left: 10px;
}

.xueba {
  padding-left: 8px;
  font-size: 20px;
  font-weight: bolder;
  color: white;
  text-shadow: 2px 2px 4px #000000;
}

.el-menu {
  background-color: transparent;
  text-align: center;
}

.el-menu-item {
  color: '#7f8488';
  background-color: '#7f8488';
  font-size: 16px;
}

.el-menu-item:hover {
  background-color: rgb(47, 47, 47);
}

.el-dropdown-link {
  color: white;
  font-size: 16px;
  text-shadow: 2px 2px 4px #000000;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.el-menu--horizontal>.el-menu-item:hover,
.el-menu--horizontal>.el-menu-item:focus {
  background-color: rgb(47, 47, 47);
}

.el-dropdown-link-avatar {
  margin-right: 5px;
  height: 30px;
  margin-top: 15px;
  color: #ffd04b;
  font-size: 16px;
  text-shadow: 2px 2px 4px #000000;
}
</style>
