import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import "./tailwind.css";

import App from "./App.vue";
import { routes } from "./routes.ts";

const app = createApp(App);

const router = createRouter({
  history: createWebHistory(),
  routes,
});

app.use(router);
app.mount("#app");
