<template>
    <div>
        <h2 class="title">二次问诊</h2>
        <my-table :data="questions" :link_url='link_url' :split="split" :column_list="questions_column_list" :detail="false" :add_type="'question'"></my-table>
        <h2 class="title">核心指标</h2>
        <my-table :data="cores" :link_url='link_url' :split="split" :column_list="column_list" :detail="detail" :add_type="add_type"></my-table>
    </div>
</template>
<script>
export default {
    data() {
        return {
            cores: [], // 数据
            questions: [],
            link_url: "/#/comp_lang?id=",  // 详情页面的url
            split: 0,  // 详情页面的url后面需要拼接上当前点击项的ID，这个split就是ID在每一行中的索引
            column_list: ["核心指标"],  // 列名
            questions_column_list: ["题目"],
            detail: true,
            add_type: "core"
        }
    },
    created() {
         this.$ajax.get("/api/core?id=" + this.$route.query.id).then(res => {
             this.cores = res.data;
         })
         this.$ajax.get("/api/question?id=" + this.$route.query.id).then(res => {
             this.questions = res.data;
         })
    },
    methods: {
    }
}
</script>
<style lang="less" scoped>
    .title{text-align: center; margin: 10px 0;}
</style>
