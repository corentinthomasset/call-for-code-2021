import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import axios from "axios";
import VueAxios from "vue-axios";
import VueApexCharts from "vue-apexcharts";
import Unicon from 'vue-unicons/dist/vue-unicons-vue2.umd'
import { uniSearch } from 'vue-unicons/dist/icons'

Unicon.add([uniSearch])
Vue.use(Unicon)

Vue.use(VueApexCharts);
Vue.use(VueAxios, axios);

Vue.component("apexchart", VueApexCharts);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
