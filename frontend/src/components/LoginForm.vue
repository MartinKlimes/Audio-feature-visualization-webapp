<script setup>
import { useI18n } from "vue-i18n";

import { reactive } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";
import { showAlert, closeAlert } from "../composables/alerts";

import { api } from "../composables/custom";

// import Vue router for redirects
import router from "../router.js";

// localization
const { t, locale } = useI18n();

// validation
const formData = reactive({
  username: "",
  password: "",
});

const rules = {
  username: { required, lengthCheck: minLength(3) },
  password: { required, lengthCheck: minLength(6) },
};

const v$ = useVuelidate(rules, formData);

function loginUser(data) {
  api.post("login", data)
    .then(function (response) {
      if (response.data.message === "login successful") {
        // if the login was successful, redirect user to the main page
        showAlert("Login was successful.");
        setTimeout(closeAlert, 1500);
        router.push("/");
      }
      if (response.data.message === "wrong password") {
        showAlert(t("alert.wrongpassword"));
        setTimeout(closeAlert, 1500);
      }
      if (response.data.message === "user does not exist") {
        showAlert(t("alert.wrongusername"));
        setTimeout(closeAlert, 1500);
      }
    })
    .catch(function (error) {
      // handle login error
      showAlert(error.message + ".");
      setTimeout(closeAlert, 1500);
    });
}
</script>

<template>
  <form
    class="w-full bg-dark-500 bg-opacity-50 blur-sm pl-25 pr-25 pt-5 pb-5 text-white"
    id="login-form"
  >
    <span class="text-3xl mb-5">{{ t("form.login") }}</span>

    <input
      v-model="v$.username.$model"
      type="text"
      class="input-field"
      :placeholder="t('form.username')"
      autocomplete="username"
    />
    <input
      v-model="v$.password.$model"
      type="password"
      class="input-field"
      :placeholder="t('form.pswd')"
      autocomplete="password"
    />

    <div v-if="!v$.username.$invalid && !v$.password.$invalid">
      <button @click="loginUser(formData)" type="button" class="btn btn-blue">
        {{ t("button.signin") }}
      </button>
    </div>
    <div v-else>
      <button type="button" class="btn btn-disabled">
        {{ t("button.signin") }}
      </button>
    </div>

    <div class="text-white mt-10 font-semibold">
      {{ t("login.notregistered") }}
      <router-link
        :to="{ path: '/signup' }"
        class="text-green-400 hover:text-white"
        >{{ t("login.goregister") }}</router-link
      >
    </div>
  </form>

  <!-- <NavBar/> -->
</template>

<style scoped>
#login-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#navbar {
  position: absolute;
  top: 0;
}

input:focus {
  outline: 2px solid rgba(255, 255, 255, 0.2);
}
</style>
