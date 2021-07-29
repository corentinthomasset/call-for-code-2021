import Vue from "vue";
import VueRouter from "vue-router";
import Stock from "../views/Stock";
import Portfolio from "@/views/Portfolio";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Portfolio",
    component: Portfolio,
    meta: {
      transition: "portfolio",
    },
  },
  {
    path: "/:ticker",
    name: "Stock",
    component: Stock,
    props: true,
    meta: {
      transition: "stock",
    },
  },
];

const router = new VueRouter({
  routes,
});

export default router;
