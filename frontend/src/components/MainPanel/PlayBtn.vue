<script setup>
import { Icon } from "@iconify/vue";
const props = defineProps({
  icon: String,
});
</script>

<template>
  <button><Icon :icon="icon" :inline="true" width="30" class="rounded-md flex hover:text-gray-500" /></button>
</template>
