<script setup>
import { wavesurfer } from "../../../../functions/waveform/waveform";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/material.css";
import { ref } from "vue";
import { trackList } from "../../../../stores/globalStores";

const props = defineProps({
  id: Number,
});

const frequencyRange = ref([0, 12000]);
const currentTrackList = trackList();

const changeRange = (e) => {
  currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = true;
  setTimeout(() => {
    wavesurfer[props.id].spectrogram.params.frequencyMin = e[0];
    wavesurfer[props.id].spectrogram.params.frequencyMax = e[1];
    wavesurfer[props.id].spectrogram.init();
    currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = false;
  }, 100);
};
</script>

<template>
  <div class="mt-4 mb-4 h-max w-full py-1 px-1 bg-white shadow-dark-900 rounded-md shadow-inner flex flex-col items-center">
    <span class="text-xs mb-1 font-bold">{{ frequencyRange[0] }}Hz - {{ frequencyRange[1] }}Hz</span>
    <vue-slider
      @change="changeRange($event)"
      v-model="frequencyRange"
      :enable-cross="false"
      :min="0"
      :width="120"
      :max="20000"
      :interval="100"
      :minRange="100"
      :tooltipStyle="{ backgroundColor: 'Blue' }"
      :processStyle="{ backgroundColor: 'Blue' }"
      :dotStyle="{ backgroundColor: 'Blue' }"
      :railStyle="{ backgroundColor: 'RoyalBlue' }"
      :stepStyle="{ backgroundColor: 'RoyalBlue' }"
      :labelStyle="{ fontSize: '10px', fontFamily: 'Courier New', fontWeight: 'bold' }"
      :marks="[0, 20000]"
      :lazy="true"
    ></vue-slider>
  </div>
</template>
