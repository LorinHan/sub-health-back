webpackJsonp([2],{U7I6:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("h2",{staticClass:"title"},[t._v("二次问诊")]),t._v(" "),i("my-table",{attrs:{data:t.questions,link_url:t.link_url,split:t.split,column_list:t.questions_column_list,detail:!1,add_type:"question",getData:t.getQuestions}}),t._v(" "),i("h2",{staticClass:"title"},[t._v("核心指标")]),t._v(" "),i("my-table",{attrs:{data:t.cores,link_url:t.link_url,split:t.split,column_list:t.column_list,detail:t.detail,add_type:t.add_type,getData:t.getData}})],1)},staticRenderFns:[]};var a=i("C7Lr")({data:function(){return{cores:[],questions:[],link_url:"/#/comp_lang?id=",split:0,column_list:["核心指标"],questions_column_list:["题目"],detail:!0,add_type:"core"}},created:function(){this.getData(),this.getQuestions()},methods:{getData:function(){var t=this;this.$ajax.get("/api/core?id="+this.$route.query.id).then(function(e){t.cores=e.data})},getQuestions:function(){var t=this;this.$ajax.get("/api/question?id="+this.$route.query.id).then(function(e){t.questions=e.data})}}},s,!1,function(t){i("df17")},"data-v-19ab4b6b",null);e.default=a.exports},df17:function(t,e){}});