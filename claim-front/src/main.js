import Vue from 'vue'
import App from './components/app'
import store from './store'

Vue.config.productionTip = true

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
