import { createApp } from "vue";
import { createI18n } from "vue-i18n";

import router from "./router.js";
import App from "./App.vue";
import "virtual:windi.css";

import { createPinia } from "pinia";

// load localization yml files
const messages = Object.fromEntries(
  Object.entries(import.meta.globEager("../locales/*.y(a)?ml")).map(([key, value]) => [
    key
      .split("/")
      .at(-1)
      ?.replace(/\.ya?ml$/, ""),
    value.default,
  ])
);

// create i18n instance for localization
const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages,
});

// create app
createApp(App).use(router).use(i18n).use(createPinia()).mount("#app");
