import Vue from "vue";
import Router from "vue-router";


import bk from "@/views/bk";
import statistics from "@/views/bk/statistics"
import fbmanager from "@/views/bk/fbmanager.vue";
Vue.use(Router);

export default new Router({
  routes: [

    {
      path: "/",
      name: "bk",
      component: bk
    },
    {
      path: "/bk",
      name: "bk",
      component: bk
    },
    {
      path: "/sc",
      name: "statistics",
      component: statistics
    },
    {
      path: "/manager",
      name: "fbmanager",
      component: fbmanager
    }
  ]
});
