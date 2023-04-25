<script setup>
import { onClickOutside } from "@vueuse/core";
import { ref, computed } from "vue";
import { Icon } from "@iconify/vue";

const props = defineProps({
  selectedColor: String,
  format: String,
});
const selectedColorbar = ref(0);
const target = ref(null);
const emits = defineEmits(["closeColorPicker"], ["updateColor"]);

const selectedColorList = computed(() => {
  return props.format == "hex" ? colorsHex[selectedColorbar.value] : colors[selectedColorbar.value];
});

const colors = [
  [
    "bg-red-300",
    "bg-orange-300",
    "bg-yellow-300",
    "bg-lime-300",
    "bg-green-300",
    "bg-gray-300",
    "bg-cyan-300",
    "bg-sky-300",
    "bg-indigo-300",
    "bg-purple-300",
    "bg-pink-300",
    "bg-rose-300",
  ],
  [
    "bg-red-600",
    "bg-orange-600",
    "bg-yellow-500",
    "bg-lime-600",
    "bg-green-600",
    "bg-gray-600",
    "bg-cyan-600",
    "bg-sky-600",
    "bg-indigo-600",
    "bg-purple-600",
    "bg-pink-600",
    "bg-rose-600",
  ],
];
const colorsHex = [
  ["#FCA5A5", "#FCD34D", "#FDE68A", "#A3E635", "#6EE7B7", "#CBD5E0", "#22D3EE", "#4F46E5", "#7C3AED", "#D53F8C", "#FECACA", "#F9A8D4"],
  ["#DC2626", "#EA580C", "#D97706", "#84CC16", "#059669", "#6B7280", "#0891B2", "#1D4ED8", "#7C3AED", "#C026D3", "#DB2777", "#F43F5E"],
];

onClickOutside(target, () => {
  setTimeout(() => {
    emits("closeColorPicker");
  }, 0);
});
</script>

<template>
  <div>
  <div class="relative h-27" ref="target">
    <div class="h-full rounded-md z-10 p-1 bg-white grid grid-cols-4 gap-1 overflow-y-auto">
      <div v-for="(color, i) in colors[selectedColorbar]" :key="i">
        <div
          class="rounded-md w-full border h-full text-xs cursor-pointer"
          :class="[color, selectedColor == selectedColorList[i] ? 'shadow-inner shadow-dark-800' : 'shadow-sm shadow-dark-50']"
          @click="$emit('updateColor', selectedColorList[i])"
        ></div>
      </div>
    </div>

    <Icon
      class="rounded absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 opacity-70 bg-white w-5 max-h-4 hover:opacity-100 hover:bg-white cursor-pointer"
      icon="humbleicons:exchange-horizontal"
      @click="selectedColorbar == 0 ? (selectedColorbar = 1) : (selectedColorbar = 0)"
    />
  </div>
</div>
</template>
