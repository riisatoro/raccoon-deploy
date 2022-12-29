import {createRouter, createWebHistory} from "vue-router";
import UserEta from "../components/UserEta";
import UserLogin from "../components/UserLogin";
import OpenedEta from "../components/OpenedEta";

const routes = [
  {
    path: "/",
    name: "My ETA",
    component: UserEta,
  },
  {
    path: "/login",
    name: "UserLogin",
    component: UserLogin,
  },
  {
    path: "/opened",
    name: "OpenedEta",
    component: OpenedEta,
  }
];


const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
