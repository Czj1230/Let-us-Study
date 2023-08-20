import Vue from 'vue'
import VueRouter from "vue-router"

// 导入组件
import MerchantList from "../components/MerchantList";
import MerchantSetting from "../components/MerchantSetting";
import ReservationRecord from "../components/ReservationRecord";
import Main from "../components/Main";
import UploadMerchantProfile from "../components/UploadMerchantProfile";
import SelectSeat from "../components/SelectSeat";
import NewRoom from "../components/NewRoom";
import SelectReturn from "../components/SelectReturn";
import NewRoomRes from "../components/NewRoomRes";
import MerchantSettingReturn from "../components/MerchantSettingReturn";
import MerchantRecord from "../components/MerchantRecord";
import Home from "../components/Home";
import StudentLogin from "../components/StudentLogin";
import StudentRegister from "../components/StudentRegister";
import MerchantLogin from "../components/MerchantLogin";
import MerchantRegister from "../components/MerchantRegister";
import StdLoginRes from "../components/StdLoginRes";
import StdRegisterRes from "../components/StdRegisterRes";
import MerLoginRes from "../components/MerLoginRes";
import MerRegisterRes from "../components/MerRegisterRes";
import StudentPage from "../components/StudentPage";
import MerchantManage from "../components/MerchantManage";
import EditRoom from "../components/EditRoom";
import AboutXueba from "../components/AboutXueba";
import ContactUs from "../components/ContactUs";
import RankingList from "../components/RankingList";

// 安装路由
Vue.use(VueRouter);

// 配置导出路由
export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/studentlogin',
      name: 'studentlogin',
      component: StudentLogin
    },
    {
      path: '/studentregister',
      name: 'studentregister',
      component: StudentRegister
    },
    {
      path: '/stdloginres',
      name: 'stdloginres',
      component: StdLoginRes
    },
    {
      path: '/stdregisterres',
      name: 'stdregisterres',
      component: StdRegisterRes
    },
    {
      path: '/merchantlogin',
      name: 'merchantlogin',
      component: MerchantLogin
    },
    {
      path: '/merchantregister',
      name: 'merchantregister',
      component: MerchantRegister
    },
    {
      path: '/merloginres',
      name: 'merloginres',
      component: MerLoginRes
    },
    {
      path: '/merregisterres',
      name: 'merregisterres',
      component: MerRegisterRes
    },
    {
      path: '/merchantlist',
      name: 'merchantlist',
      component: MerchantList
    },
    {
      path: '/merchantsetting',
      name: 'merchantsetting',
      component: MerchantSetting,
    },
    {
      path: '/merchantsettingreturn',
      name: 'merchantsettingreturn',
      component: MerchantSettingReturn,
    },
    {
      path: '/reservartionrecord',
      name: 'reservartionrecord',
      component: ReservationRecord,
    },
    {
      path: '/merchantrecord',
      name: 'merchantrecord',
      component: MerchantRecord,
    },
    {
      path: '/uploadmerchantprofile',
      name: 'uploadmerchantprofile',
      component: UploadMerchantProfile,
    },
    {
      path: '/selectseat',
      name: 'selectseat',
      component: SelectSeat,
    },
    {
      path: '/newroom',
      name: 'newroom',
      component: NewRoom
    },
    {
      path: '/selectreturn',
      name: 'return',
      component: SelectReturn
    },
    {
      path: '/newroomres',
      name: 'newroomres',
      component: NewRoomRes
    },
    {
      path: '/studentpage',
      name: 'studentpage',
      component: StudentPage
    },
    {
      path: '/merchantmanage',
      name: 'merchantmanage',
      component: MerchantManage
    },
    {
      path: '/editroom',
      name: 'editroom',
      component: EditRoom
    },
    {
      path: '/aboutxueba',
      name: 'aboutxueba',
      component: AboutXueba
    },
    {
      path: '/contactus',
      name: 'contactus',
      component: ContactUs
    },
    {
      path: '/rankinglist',
      name: 'rankinglist',
      component: RankingList
    }
  ]
})

