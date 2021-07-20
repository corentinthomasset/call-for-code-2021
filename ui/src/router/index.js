import Vue from "vue";
import VueRouter from "vue-router";
import Stock from "../views/Stock";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Stock",
    component: Stock,
  },
  /*
  {
    path: "/:ticker",
    name: "Stock",
    component: Stock,
    props: true,
  },
  */
];

const router = new VueRouter({
  routes,
});

export default router;
