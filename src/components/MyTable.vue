<template>
    <div>
        <el-alert v-if="post_ok" title="添加成功！" type="success" show-icon>
        </el-alert>
        <el-button @click="edit_new" type="primary" class="new" icon="el-icon-circle-plus-outline">新 增</el-button>
        <el-table
            :data="data"
            border
            style="width: 100%">
            <!-- <el-table-column
            prop="0"
            label="ID">
            </el-table-column> -->
            <el-table-column
            prop="1"
            :label="column_list[0]">
            </el-table-column>
            <el-table-column
            v-if="column_list.length >= 2"
            prop="2"
            :label="column_list[1]">
            </el-table-column>
            <el-table-column
            width="300px"
            label="操作">
            <template slot-scope="scope">
                <el-button type="info" round plain icon="el-icon-info" size="mini" @click="link(scope.row)">详 情</el-button>
                <el-button type="primary" round icon="el-icon-edit" size="mini" @click="edit(scope.row)">修 改</el-button>
            <el-button type="danger" round size="mini" icon="el-icon-delete" @click="del(scope.row)">删 除</el-button>
            </template>
            </el-table-column>
        </el-table>

        <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
            <p class="label">{{column_list[0]}}：</p>
            <el-input :placeholder="column_list[0]" v-model="edit_list[1]"></el-input>
            <p v-if="column_list.length >= 2" class="label">{{column_list[1]}}：</p>
            <el-input v-if="column_list.length >= 2" type="textarea" :rows="4" :placeholder="column_list[1]" v-model="edit_list[2]"></el-input>
            <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="change">修 改</el-button>
            </span>
        </el-dialog>

        <el-dialog title="提示" :visible.sync="dialogVisible2" width="30%">
            <p class="label">{{column_list[0]}}：</p>
            <el-input :placeholder="column_list[0]" v-model="new_data[0]"></el-input>
            <p v-if="column_list.length >= 2" class="label">{{column_list[1]}}：</p>
            <el-input v-if="column_list.length >= 2" type="textarea" :rows="4" placeholder="治疗建议" v-model="new_data[1]"></el-input>
            <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible2 = false">取 消</el-button>
            <el-button type="primary" @click="change2">添 加</el-button>
            </span>
        </el-dialog>

        <el-dialog title="提示" :visible.sync="dialogVisible3" width="30%">
            <p class="label">确定要删除吗？</p>
            <p v-if="is_core" class="label">这将会删除掉<span class="red">所有与 <strong>{{core_name}}</strong> 相关的口语化描述。</span></p>
            <p v-if="is_symptom" class="label">这将会删除掉<span class="red">所有与 <strong>{{symptom_name}}</strong> 相关的数据，包括相关的核心指标、二次问诊题目以及口语化描述。</span></p>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible3 = false">取 消</el-button>
                <el-button type="primary" @click="change3">删 除</el-button>
            </span>
        </el-dialog>
    </div>
</template>
<script>
import Qs from 'qs'  // 这个库是用来..em..反正axios发送post请求就用这个库把数据转换一下，然后修改headers才能成功
export default {
    name: 'MyTable',
    props: ["data", "link_url", "split", "column_list", "detail", "add_type", "kind", "getData"],
    data() {
        return {
            dialogVisible: false,   // 修改业务的弹出框
            dialogVisible2: false,  // 添加业务的弹出框
            dialogVisible3: false,  // 删除业务的弹出框
            edit_list: [],
            new_data: ["", ""],
            post_ok: false,    // 用来管理添加成功的提示条是否显示
            del_id: 0,
            is_core: false,
            is_symptom: false,
            core_name: "",
            symptom_name: ""
        }
    },
    created() {
    },
    methods: {
        link(row) {
            if(!this.$props.detail) return;
            window.location.href = this.$props.link_url + row[this.$props.split];
        },
        change() {
            this.dialogVisible = false;
            var data = {
                "id": this.edit_list[0], 
                "type": this.$props.add_type, 
                "value": this.edit_list[1]
            }
            if(data.type == "symptom") data.value2 = this.edit_list[2]
            this.$ajax.post("/api/update", Qs.stringify(data), {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res => {
                if(res.data == "ok") window.location.reload();
            }).then(err => {console.log(err)})
        },
        change2() {
            this.dialogVisible2 = false;
            this.new_one();
        },
        change3() {
            this.dialogVisible3 = false;
            var url = "/api/del";
            var type = "";
            switch(this.$props.add_type) {
                case "symptom": {
                    type = "symptom";
                    break;
                }
                case "core": {
                    type = "core";
                    break;
                }
                case "comp_lang": {
                    type = "comp_lang";
                    break;
                }
                case "question": {
                    type = "question";
                    break;
                }
            }
            this.$ajax.post(url, Qs.stringify({"id": this.del_id, "type": type}), {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res => {
                if(res.data == "ok") window.location.reload();
            })
        },
        del(row) {
            this.dialogVisible3 = true;
            this.del_id = row[0];
            if(this.$route.path == '/core') {
                if(this.$props.add_type == "question") return;
                this.is_core = true;
                this.core_name = row[1];
            } else if(this.$route.path == '/') {
                this.is_symptom = true;
                this.symptom_name = row[1];
            }
        },
        edit_new() {
            this.new_data = ["", ""];
            this.dialogVisible2 = true;
        },
        edit(row) {
            this.dialogVisible = true;
            this.edit_list = row;
        },
        new_one(url) {
            var type = this.$props.add_type;
            if(type == "symptom") {
                this.$ajax.post(
                    "/api/add_symptom", 
                    Qs.stringify({"symptom": this.new_data[0], "kind": this.$props.kind, "advice": this.new_data[1]}), 
                    {headers:{'Content-Type':'application/x-www-form-urlencoded'}}
                ).then(res => {
                    if(res.data == 'ok') {
                        this.post_ok = true;
                        this.$props.getData();
                    }
                })
            } else if(type == "core") {
                this.$ajax.post(
                    "/api/add_core", 
                    Qs.stringify({"core": this.new_data[0], "symptom_id": this.$route.query.id}), 
                    {headers:{'Content-Type':'application/x-www-form-urlencoded'}}
                ).then(res => {
                    if(res.data == 'ok') {
                        this.post_ok = true;
                        this.$props.getData();
                    }
                })
            } else if(type == "comp_lang") {
                this.$ajax.post(
                    "/api/add_comp_lang", 
                    Qs.stringify({"desc": this.new_data[0], "core_id": this.$route.query.id}), 
                    {headers:{'Content-Type':'application/x-www-form-urlencoded'}}
                ).then(res => {
                    if(res.data == 'ok') {
                        this.post_ok = true;
                        this.$props.getData();
                    }
                })
            } else if(type == "question") {
                 this.$ajax.post(
                    "/api/add_question", 
                    Qs.stringify({"question": this.new_data[0], "symptom_id": this.$route.query.id}), 
                    {headers:{'Content-Type':'application/x-www-form-urlencoded'}}
                ).then(res => {
                    if(res.data == 'ok') {
                        this.post_ok = true;
                        this.$props.getData();
                    }
                })
            }
        }
    }
}
</script>
<style lang="less" scoped>
    .el-alert{margin-top: 20px;}
    .red{color: red;}
</style>
