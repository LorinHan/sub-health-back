<template>
  <div>
    <my-table :data="comps" :link_url='link_url' :split="split" :column_list="column_list" :detail="detail" :add_type="add_type" :getData="getData"></my-table>
  </div>
</template>
<script>
export default {
  data() {
    return {
      comps: [], // 数据
      link_url: "#",  // 详情页面的url
      split: 0,  // 详情页面的url后面需要拼接上当前点击项的ID，这个split就是ID在每一行中的索引
      column_list: ["口语化描述"],  // 列名
      detail: false,
      add_type: "comp_lang"
    }
  },
  methods: {
    getData() {
      this.$ajax.get("/api/comp_lang?id=" + this.$route.query.id).then(res => {
        this.comps = res.data;
      })
    }
  },
  created() {
      this.getData();
  }
}
</script>
<style lang="less">
</style>
