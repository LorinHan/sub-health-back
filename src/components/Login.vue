<template>
    <div class="login">
        <h2 class="title">数据管理系统</h2>
        <el-input prefix-icon="el-icon-menu" type="text" v-model="username" placeholder="请输入用户名"></el-input>
        <el-input prefix-icon="el-icon-menu" type="password" v-model="password" placeholder="请输入密码" @keyup.enter.native="login" auto-complete="off"></el-input>
        <el-button type="primary" id="login" @click="login">登 录</el-button>
    </div>
</template>
<script>
import Qs from 'qs'
export default {
    data() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        login() {
            this.$ajax.post("/api/token", Qs.stringify({"username": this.username, "password": this.password}), {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res => {
                if(res.data == "300") return window.alert("用户名或密码错误")
                window.localStorage.setItem("token", res.data);
                window.localStorage.setItem("username", this.username);
                window.localStorage.setItem("islogin", 1);
                this.$router.push("/")
            })
        }
    }
}
</script>
<style lang="less" scoped>
.title{text-align: center; margin-bottom: 40px;}
.login{ width: 30%; margin: 100px auto;}
.el-input{margin: 10px 0;}
.el-button{display: block; margin: 20px auto;}
</style>
