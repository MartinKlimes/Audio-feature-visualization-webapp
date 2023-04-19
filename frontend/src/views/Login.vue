<script setup>
import LoginForm from "../components/LoginForm.vue";
import LangSwitch from "../components/LangSwitch.vue";
</script>

<template>
  <LangSwitch />

  <div id="login-container">
    <LoginForm />
  </div>
</template>

<style scoped>
#login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

#lang-switch {
  position: absolute;
  right: 0;
}
</style>
