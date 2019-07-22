import Vue from 'vue'
import Router from 'vue-router';
const Comp_lang = r => require.ensure([], () => r(require('@/components/Comp_lang.vue')), 'chunkname0')
const Core = r => require.ensure([], () => r(require('@/components/Core.vue')), 'chunkname1')
const Symptom = r => require.ensure([], () => r(require('@/components/Symptom.vue')), 'chunkname2')
const Login = r => require.ensure([], () => r(require('@/components/Login.vue')), 'chunkname3')

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'symptom',
      component: Symptom
    },
    {
      path: "/core",
      name: "Core",
      component: Core
    },
    {
      path: "/comp_lang",
      name: "Comp_lang",
      component: Comp_lang
    }
  ]
})
