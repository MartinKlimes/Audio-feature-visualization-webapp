<script setup>
import RegisterForm from "../components/RegisterForm.vue";
import LangSwitch from "../components/LangSwitch.vue";
</script>

<template>
  <LangSwitch />

  <div id="register-container">
    <RegisterForm />
  </div>
</template>

<style scoped>
#register-container {
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
