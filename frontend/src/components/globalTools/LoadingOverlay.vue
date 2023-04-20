<script setup>
import { Icon } from "@iconify/vue";

const props = defineProps({
  color: {
    type: String,
    default: "black",
  },
  loading: {
    type: Boolean,
    default: true,
  },
  height: {
    type: String,
    default: "35px",
  },
  width: {
    type: String,
    default: "4px",
  },
});
</script>

<template>

  <div class="absolute w-full h-full bg-white z-20 opacity-80 flex items-center justify-center border-4 border-gray-400 rounded-xs">
    <Icon class="spin " width="40" icon="icomoon-free:spinner10" />
    <!-- <scale-loader :loading="loading" :color="color" :height="height" :width="width"></scale-loader> -->
  </div>
</template>
