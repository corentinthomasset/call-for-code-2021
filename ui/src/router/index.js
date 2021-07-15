import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Stock from "../views/Stock";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/:ticker",
    name: "Stock",
    component: Stock,
    props: true,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
