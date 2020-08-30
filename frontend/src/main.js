import Vue from 'vue'
import store from './store'
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './routes'

// import home from './pages/home.vue'
// import news from './pages/news.vue'

import './styles/app.css';

Vue.use(VueRouter);

// Vue.component('home', home)
// Vue.component('news', news)

new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App),
})
