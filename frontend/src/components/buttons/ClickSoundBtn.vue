<script setup>
import { Icon } from "@iconify/vue";
import { ref, onMounted, onUnmounted, watch } from "vue";
import SelectFiles from "./SelectFiles.vue";
import { wavesurfer } from "../../functions/waveform/waveform";
import { api } from "../../composables/custom";

let clickOnBarLineIndex = 0;
const selectedClickSound = ref();
const clickAudioList = ref([]);

const emits = defineEmits(["closeModal", "selectAudio"]);

const props = defineProps({
  id: Number,
  markersList: Array,
  selectedSound: String,
});

onMounted(() => {
  api.get("/get-files-list/clickSound").then(function (response) {
    clickAudioList.value = response.data;
  });
  wavesurfer[props.id].backend.on("audioprocess", clickSound);

  wavesurfer[props.id].on("interaction", clearLineIndex);
});

watch(
  () => props.selectedSound,
  () => {
    if (props.selectedSound) {
      api.get("/get-click-audio/" + props.selectedSound).then(function (response) {
        selectedClickSound.value = new Audio(response.request.responseURL);
        selectedClickSound.value.play()
      });
    }
  },
  { immediate: true }
);

onUnmounted(() => {
  wavesurfer[props.id].backend.un("audioprocess", clickSound);
  wavesurfer[props.id].un("interaction", clearLineIndex);
});

const clearLineIndex = () => {
  clickOnBarLineIndex = 0;
};

const clickSound = (id) => {
  if(selectedClickSound.value){

  if (wavesurfer[props.id].isPlaying()) {
    if (id > props.markersList[clickOnBarLineIndex]) {
      selectedClickSound.value.play();
      clickOnBarLineIndex += 1;
    }
  }
}

};

</script>

<template>
  <div >
    <!-- <div class="absolute bg-red-400">
      <Icon
        v-if="!playSoundClick"
        @click="playSoundOnMarker(), (playSoundClick = !playSoundClick)"
        icon="clarity:volume-mute-line"
        class="rounded-md hover:opacity-80 p-0.5 cursor-pointer"
        width="20"
        :class="backgroundColor"
      />
      <Icon
        v-if="playSoundClick"
        @click="muteSoundOnMarker(), (playSoundClick = !playSoundClick)"
        icon="clarity:volume-up-line"
        class="p-0.5 rounded-md shadow-inner shadow-dark-500 cursor-pointer"
        width="20"
        :class="backgroundColor"
      />
      <Icon
        icon="material-symbols:arrow-right"
        class="text-lg cursor-pointer rounded-md hover:opacity-60"
        @click="selectSoundClick = !selectSoundClick"
        :class="{ 'opacity-60 shadow-inner shadow-dark-400': selectSoundClick }"
      />
    </div> -->

    <SelectFiles
      :files="clickAudioList"
      :id="id"
      @select-file="$emit('selectAudio', $event)"
      :selected-file="selectedSound"
      class="z-10"
    />
  </div>
</template>

<style scoped>
.sound-enter-active,
.sound-leave-active {
  transition: all 0.1s ease-out;
}

.sound-enter-from,
.sound-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}
</style>
