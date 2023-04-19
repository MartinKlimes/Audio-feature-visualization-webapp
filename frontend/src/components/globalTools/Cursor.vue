<script setup>
import { ref, watchEffect, toRef } from "vue";

const props = defineProps({
  marginLeft: Number,
  color: String,
  id: String,

  width: {
    type: Number,
    default: 1,
  },
});

const cursor = ref(null);
const color = toRef(props, "color");
const width = toRef(props, "width");

watchEffect(() => {
  if (cursor.value) {
    cursor.value.style.width = `${width.value}px`;
    cursor.value.style.backgroundColor = `${color.value})`;
  }
});
</script>

<template>
  <div class="h-full absolute z-10" :class="[`bg-${color}`, `w-${width}`]" ref="cursor" :id="id" data-html2canvas-ignore="true"></div>
</template>
