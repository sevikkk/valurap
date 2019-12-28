import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import store from './store'
import VueSocketIO from 'vue-socket.io';

Vue.config.productionTip = false;
Vue.use(new VueSocketIO({
    debug: true,
    connection: `//${window.location.host}`,
    vuex: {
        store,
        actionPrefix: 'SOCKET_',
        mutationPrefix: 'SOCKET_'
    },
    options: { path: "/socket.io/" } //Optional options
}))

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
