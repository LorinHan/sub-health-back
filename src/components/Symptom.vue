<template>
    <div>
        <my-table :data="symptoms" :link_url='link_url' :split="split" :column_list="column_list" :detail="detail" :add_type="add_type" :kind="kind"></my-table>
    </div>
</template>
<script>
export default {
    data() {
        return {
            symptoms: [],  // 数据
            link_url: "/#/core?id=",  // 详情页面的url
            split: 0,  // 详情页面的url后面需要拼接上当前点击项的ID，这个split就是ID在每一行中的索引
            column_list: ["症状", "治疗建议"],  // 列名
            detail: true,
            add_type: "symptom",
            kind: 1
        }
    },
    created() {
        if(!this.$route.query.kind) {
            var url = "/api/symptom";
            this.$ajax.get(url).then(res => {
                this.symptoms = res.data;
            })
        } else if(this.$route.query.kind == 2) {
            this.$ajax.get("/api/symptom?kind=2").then(res => {
                if(res.data == "0") return this.$router.push("/login");
                this.symptoms = res.data;
                this.kind = 2;
            })
        }
    },
    watch: {
        $route(to, from) {
            if(to.query.kind == 2) {
                this.$ajax.get("/api/symptom?kind=2").then(res => {
                    this.symptoms = res.data;
                    this.kind = 2;
                })
            }
        }
    },
    methods: {
    }
}
</script>
<style lang="less">
    
</style>
