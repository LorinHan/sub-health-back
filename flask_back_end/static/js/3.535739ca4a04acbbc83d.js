webpackJsonp([3],{"85bJ":function(t,e){},o5n3:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("my-table",{attrs:{data:this.comps,link_url:this.link_url,split:this.split,column_list:this.column_list,detail:this.detail,add_type:this.add_type,getData:this.getData}})],1)},staticRenderFns:[]};var n=i("C7Lr")({data:function(){return{comps:[],link_url:"#",split:0,column_list:["口语化描述"],detail:!1,add_type:"comp_lang"}},methods:{getData:function(){var t=this;this.$ajax.get("/api/comp_lang?id="+this.$route.query.id).then(function(e){t.comps=e.data})}},created:function(){this.getData()}},a,!1,function(t){i("85bJ")},null,null);e.default=n.exports}});