<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { wavesurfer } from "../../../../functions/waveform/waveform";
import { api } from "../../../../composables/custom";
import SelectFiles from "../../../globalTools/SelectFiles.vue";


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
        selectedClickSound.value.play();
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
  if (selectedClickSound.value) {
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
  <div>
    <SelectFiles :files="clickAudioList" :id="id" @select-file="$emit('selectAudio', $event)" :selected-file="selectedSound" class="z-10" />
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
