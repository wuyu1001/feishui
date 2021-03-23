import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Axios from 'axios'



Vue.use(ElementUI, { size: 'small' })
Vue.config.productionTip = false
Vue.prototype.$axios = Axios

new Vue({
  router,
  store,
  el: '#app',
  render: h => h(App)
}).$mount('#app')
