<script setup>
import { Icon } from "@iconify/vue";

const props = defineProps({
  name: String,
  type: String,
});
const emits = defineEmits(["deleteTrack"]);
</script>

<template>
  <div>
    <div class="border border-gray-200 p-3 mb-4 rounded md:text-2xl hover:bg-gray-200 relative">
      <h4 class="inline-block font-bold">{{ name }}</h4>

      <button
        title="Delete song"
        class="ml-1 mt-1 py-1 px-2 text-xs rounded text-white bg-red-600 float-right hover:bg-red-500"
        @click="$emit('deleteTrack', type + name)"
      >
        <Icon icon="fa:times" />
      </button>
    </div>
  </div>
</template>
