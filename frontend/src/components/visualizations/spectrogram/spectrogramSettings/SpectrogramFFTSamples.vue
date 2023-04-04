
<script setup>
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/material.css";
import { wavesurfer } from "../../../../functions/waveform";
import { ref } from "vue";
import { trackList } from "../../../../globalStores";

const selectedValue = ref(wavesurfer[props.id].spectrogram.params.fftSamples)
const currentTrackList = trackList()

const values = [128, 256, 512, 1024, 2048, 4096]
const changeNumberFFT = (e) => {
  currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = true
  setTimeout(() => {
    wavesurfer[props.id].spectrogram.params.fftSamples = e
    wavesurfer[props.id].spectrogram.init()
    currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = false
    
  }, 0);
}

const props = defineProps({
    id: Number
})
</script>


<template>
<div class="box p-2 bg-white rounded-md mt-2 flex flex-col items-center">

    <div>
    <div v-for="value in values" :key="value">
      <input type="radio" :name="name" :value="value" v-model="selectedValue" @change="changeNumberFFT(value)" class="cursor-pointer">
      <label class="font-bold text-xs ml-1">{{ value }}</label>
    </div>
  </div>

</div>
</template>