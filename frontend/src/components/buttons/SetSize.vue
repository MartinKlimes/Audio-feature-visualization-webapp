<script setup>
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";

const props = defineProps({
    defaultSize: Number
});
const emits = defineEmits(["closeSizeSetter", "changeSize"]);

const size = ref(props.defaultSize);
const target = ref(null);

onClickOutside(target, () => {
  setTimeout(() => {
    emits("closeSizeSetter");
  }, 0);
});

</script>

<template>
  <div class="mt-2 h-40 w-10 border rounded-md py-1 flex flex-col items-center box " ref="target">
    <input
      class="transform rotate-90 mt-16"
      type="range"
      @change="$emit('changeSize', parseInt(size))" 
      v-model="size"
      min="100"
      max="1000"
      step="100"
      id="size"
    />
    <span class="mt-16 text-xs font-bold">{{ size }}px</span>
  </div>
</template>
