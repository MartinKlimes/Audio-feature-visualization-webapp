<script setup>
import { trackList } from "../../globalStores";
import { Icon } from "@iconify/vue";
const currentTrackList = trackList();

const props = defineProps({
  files: Array,
  id: Number,
  selectedFile: String,
  isDivClass: Boolean,
});

const emits = defineEmits(["selectFile"]);
</script>

<template>
  <div class="absolute w-[97%] h-[47%] bg-white border border-black rounded-md overflow-y-auto">
    <div
      class="min-h-6 flex items-center justify-center bg-light-blue-400 border border-black m-1 p-0.5 text-sm font-bold rounded-md hover hover:border-gray-400 cursor-pointer shadow-md shadow-gray-700"
      :class="{ 'shadow-inner shadow-dark-500 bg-light-blue-300 hover:border-black': selectedFile == file }"
      v-for="file in files"
      @click="$emit('selectFile', file)"
    >
      <div v-if="!isDivClass">
        {{ file }}
      </div>
      <div v-if="isDivClass" class="" :class="file"></div>
    </div>
  </div>
</template>
