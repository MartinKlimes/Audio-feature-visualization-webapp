<script setup>
import { Icon } from "@iconify/vue";
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();
</script>

<template>
  <div id="lang-switch" class="text-light-50 pt-1 m-3 flex justify-center items-center h-10 bg-gray-400  border border-gray-100 boxTight bg-opacity-50 blur-sm bg-opacity-50 rounded-md z-30">
    <input type="radio" id="one" class="hidden" value="en" v-model="locale" />
    <label for="one">
      <Icon icon="twemoji:flag-united-kingdom" :inline="true" width="25" class="m-2 cursor-pointer hover:opacity-70 transition" />
    </label>

    <input type="radio" id="two" class="hidden" value="cz" v-model="locale" />
    <label for="two">
      <Icon icon="twemoji:flag-czechia" :inline="true" width="25" class="m-2 cursor-pointer hover:opacity-70 transition" />
    </label>
  </div>
</template>

<style scoped></style>
