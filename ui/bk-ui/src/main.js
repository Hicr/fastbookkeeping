// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";
import Element from "element-ui"; //element - 1
import HighchartsVue from 'highcharts-vue'
Vue.use(HighchartsVue)

import "element-ui/lib/theme-chalk/index.css"; // element -2
// 引入axios
import axios from "axios";
// axios.defaults.baseURL = "/api";
Vue.prototype.$request = axios; // s使用 this.$request即可进行请求
import Vuex from "vuex";
Vue.config.productionTip = false;
import store from "./store/store";
Vue.use(Vuex);
import "./assets/style/reset.css";
import "./assets/style/border.css";

Vue.use(Element); // element - 3
/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  store,
  components: { App },
  template: "<App/>"
  //   render: c => c(App)
});
