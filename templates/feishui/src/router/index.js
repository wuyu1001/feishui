import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {path:'/',component:  resolve => require(['../components/HelloWorld1'], resolve)},
  {path:'/ywsj',component:  resolve => require(['../components/HelloWorld1'], resolve)},
  {path:'/yscsj',component:  resolve => require(['../components/HelloWorld2'], resolve)},
  {path:'/cysj',component:  resolve => require(['../components/HelloWorld3'], resolve)},
  {path:'/upload',component:  resolve => require(['../components/HelloWorld4'], resolve)},

]

const router = new VueRouter({
  routes
})

export default router
