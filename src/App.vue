<template>
  <div id="app">
    <el-container>
      <el-aside width="200px">
        <el-row class="tac">
          <el-col>
            <el-menu
              default-active="1"
              :default-openeds="['1']"
              class="el-menu-vertical-demo"
              background-color="#20222A"
              text-color="#fff"
              active-text-color="#ffd04b">
              <el-submenu index="1">
                <template slot="title">
                  <i class="el-icon-location"></i>
                  <span>类别</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="1-1"><a href="/">成人</a></el-menu-item>
                  <el-menu-item index="1-2"><a href="/#/?kind=2">儿童</a></el-menu-item>
                </el-menu-item-group>
              </el-submenu>
            </el-menu>
          </el-col>
        </el-row>
      </el-aside>
    <el-container>
      <el-header>
      <el-page-header @back="goBack" :content="path"></el-page-header>
      <el-button type="info" @click="logout" icon="el-icon-error" size="small" class="header_btn">退出</el-button>
      <el-button type="primary" @click="islogin" icon="el-icon-setting" size="small" class="header_btn">修改密码</el-button>
    </el-header>
      <el-main>
        <router-view ref="child"/>
      </el-main>
    </el-container>
  </el-container>

  <el-dialog title="提示" :visible.sync="show" width="30%">
            <p class="label">请输入原密码：</p>
            <el-input placeholder="原密码" v-model="old_pwd"></el-input>
            <p class="label">请输入新密码：</p>
            <el-input placeholder="新密码" v-model="new_pwd"></el-input>
            <p class="label">确认新密码：</p>
            <el-input placeholder="新密码" v-model="sure_new_pwd"></el-input>
            <span slot="footer" class="dialog-footer">
            <el-button @click="show = false">取 消</el-button>
            <el-button type="primary" @click="change_pwd">确认修改</el-button>
            </span>
        </el-dialog>

  </div>
</template>

<script>
import Qs from 'qs'
export default {
  name: 'App',
  data() {
    return {
        activeIndex: '1',
        activeIndex2: '1',
        path: "症状",
        show: false,
        old_pwd: "",
        new_pwd: "",
        sure_new_pwd: ""
    }
  },
  methods: {
    islogin() {
      if(window.localStorage.getItem("islogin") != 1) return window.alert("请先登录")
      this.show = true
    },
    logout() {
      window.localStorage.setItem("token", "");
      window.localStorage.setItem("islogin", 0);
      this.$router.push("/login");
    },
    goBack() {
      window.history.back(-1);
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    change_pwd() {
      if(this.sure_new_pwd != this.new_pwd) return window.alert("新密码与确认密码不一致")
      this.$ajax.post("/api/update_password", Qs.stringify({"username": window.localStorage.getItem("username"), "password": this.new_pwd, "old_pwd": this.old_pwd})).then(res => {
        switch(res.data){
          case "pwd_err": {window.alert("原密码错误");break;}
          case "err": {window.alert("服务端错误");break;}
          case "ok": {window.localStorage.setItem("token", "");window.alert("修改成功，请重新登录");this.$router.push("/login");this.show = false;window.localStorage.setItem("islogin", 0);}
        }

      })
    }
  },
  watch:{
    $route(to,from){
      if(to.path == "/login") {
        document.getElementsByTagName("aside")[0].style.display = 'none'
        document.getElementsByTagName("header")[0].style.display = 'none'
      } else {
        document.getElementsByTagName("aside")[0].style.display = 'block'
        document.getElementsByTagName("header")[0].style.display = 'block'
      }
      if(to.path == '/') return this.path = "症状";
      else if(to.path == '/login') return this.path = "登陆";
      else if(to.path == '/core') return this.path = "症状 / 核心指标";
      else if(to.path == "/comp_lang") this.path = "症状 / 核心指标 / 口语化描述";
    }
  }
}
</script>

<style>
* {margin: 0; padding: 0;}
html, body, #app, .el-container{height:100%;}
.link{display: block; width:100%;height:100%;padding: 0 20px; text-decoration: none;}
.el-menu-item{padding: 0;}
.label{margin: 20px 0; font-weight: 600;}
.new{margin: 10px; float: right;}
.el-header{border-bottom: 1px solid #ddd;}
.el-main{background-color: #f2f2f2;}
.el-page-header{width:50%;height:100%; line-height: 60px;float: left;}
.el-row{height: 100%;background-color: #20222A;}
a{text-decoration: none;color: #f2f2f2;}
.header_btn{float: right; z-index: 999; margin-top: 14px; margin-left: 15px;}
</style>
