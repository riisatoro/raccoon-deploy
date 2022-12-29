import {createApp} from "vue";
import App from "./App.vue";
import {createPinia} from "pinia";

const pinia = createPinia();

import "@/style/index.css";
import router from "./router";
import "./interceptors/axios";

const app = createApp(App);
app.use(router);
app.use(pinia);
app.mount("#app");
