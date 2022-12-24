<script setup>
import HelloWorld from '../components/HelloWorld.vue'

import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n();

</script>

<template>
  <HelloWorld msg="Hello Vue 3 + Vite" />

<input type="radio" id="one" value="en" v-model="locale" />
<label for="one">EN</label>

<input type="radio" id="one" value="cz" v-model="locale" />
<label for="two">CZ</label>


</template>

<style>

</style>
