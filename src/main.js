import Vue from 'vue';
import http from './router/http.js';
import App from './App'
import router from './router'
import { Button, Table, TableColumn, PageHeader, Menu, MenuItem, Submenu, Dialog, Input, Alert, Row, Col, MenuItemGroup, Header, Aside, Main, Container } from 'element-ui';
import MyTable from "./components/MyTable";


Vue.prototype.$ajax = http
Vue.config.productionTip = false
Vue.use(Button)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Menu)
Vue.use(MenuItem)
Vue.use(Submenu)
Vue.use(Dialog)
Vue.use(Input)
Vue.use(PageHeader)
Vue.use(Alert)
Vue.use(Row)
Vue.use(Col)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Container)
Vue.use(MenuItemGroup)
Vue.component('my-table', MyTable)

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
