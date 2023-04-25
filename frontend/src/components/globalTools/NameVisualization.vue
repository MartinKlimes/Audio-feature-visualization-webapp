<script setup>
import { ref } from "vue";
import { useHideElement } from "../../composables/useHideElement";
import { Icon } from "@iconify/vue";

const showTrackName = ref(true);
const showEye = ref(false);
const { hide } = useHideElement(showEye);

const props = defineProps({
  trackName: String,
});

const trackNameHide = () => {
  showTrackName.value = !showTrackName.value;
};
</script>

<template>
  <!-- <div @mouseenter="hide" class="absolute z-20 left-0 top-0 bg-red-300">{{ trackName }}</div> -->

  <div @mouseenter="hide" class="text-sm absolute gap-1 h-5" :class="!showTrackName ? 'w-20' : 'w-max'">
    <Icon
      v-show="showEye"
      :icon="!showTrackName ? 'mdi:show' : 'mdi:hide'"
      :width="15"
      class="bg-white w-max hover:border hover:border-black rounded-md mt-0.5 z-20 absolute cursor-pointer -left-4"
      @click="trackNameHide()"
      :title="'hide keyboard'"
    />
    {{ showTrackName ? trackName : "" }}
  </div>
</template>
