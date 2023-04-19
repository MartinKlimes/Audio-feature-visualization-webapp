<script setup>
import "vue-slider-component/theme/material.css";
import { wavesurfer } from "../../../../functions/waveform/waveform";
import { ref } from "vue";
import { trackList } from "../../../../stores/globalStores";
import { updateRecording } from "../../../../composables/custom";
const selectedValue = ref(wavesurfer[props.id].spectrogram.params[props.parametr]);
const currentTrackList = trackList();

const changeParametr = (e) => {
  currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = true;
  setTimeout(() => {
    wavesurfer[props.id].spectrogram.params[props.parametr] = e;
    wavesurfer[props.id].spectrogram.init();
    currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = false;
    updateRecording(props.id, props.parametr, e);
  }, 0);
};

const props = defineProps({
  id: Number,
  values: Array,
  parametr: String,
});
</script>

<template>
  <div class="box p-2 bg-white rounded-md mt-2 flex flex-col items-center">
    <div>
      <div v-for="value in values" :key="value">
        <input type="radio" :value="value" v-model="selectedValue" @change="changeParametr(value)" class="cursor-pointer" />
        <label class="font-bold text-xs ml-1">{{ value }}</label>
      </div>
    </div>
  </div>
</template>
