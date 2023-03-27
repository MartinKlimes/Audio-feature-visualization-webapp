<script setup>

import { ref } from "vue";
import { trackIndex } from "../../../globalStores";
import { Icon } from "@iconify/vue";
import { updateRecording } from "../../../../custom";

const props = defineProps({
  track: Object,
});

const fftsamplesSelected = ref(12000);
const globalTrackIndex = trackIndex();

function changeSpectrogramNumberOfSamples(numberOfSamples) {
  wavesurfer[globalTrackIndex.selTrackIndex].spectrogram.params.fftSamples =
    parseInt(numberOfSamples.target.value);
  wavesurfer[globalTrackIndex.selTrackIndex].spectrogram.init();
  fixedSpecLabels();
}
function changeSpectrogramMaxFrequency(maxFrequency) {
  wavesurfer[globalTrackIndex.selTrackIndex].spectrogram.params.frequencyMax =
    parseInt(maxFrequency);
  wavesurfer[globalTrackIndex.selTrackIndex].spectrogram.init();
  fixedSpecLabels();
}
function changeSpectrogramWindow(windowType) {
  wavesurfer[globalTrackIndex.selTrackIndex].spectrogram.params.windowFunc =
    windowType.target.value;
  wavesurfer[globalTrackIndex.selTrackIndex].spectrogram.init();
  fixedSpecLabels();
}

const fixedSpecLabels = () => {
  let label = document.querySelector(".spec-labels");
  label.id = `spec-labels-0`;
};

const removeSpectrogram = (params) => {
  props.track.spectrogram.isSpectrogram = false;
  props.track.spectrogram.isSpectrogramDisplayed = false;
  updateRecording(props.track.id, "isSpectrogram", false);
  updateRecording(props.track.id, "isSpectrogramDisplayed", false);
};
</script>

<template>
  <div
    class="flex flex-col items-center relative h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 shadow-md"
  >
    <button
      title="reload waveform"
      class="mt-4 opacity-50 hover:opacity-100 absolute right-0 bottom-0"
      @click="removeSpectrogram"
    >
      <Icon icon="mingcute:delete-2-line" />
    </button>
  </div>
  <!-- <div class=" bg-blue-900 h-100% w-67 z-5 -mt-9.7rem   rounded-1xl border-1 border-black text-sm">
    <div class="rounded border-b">
        <span class="spec-settings-text">Number of FFT samples:  </span>
        <select id="fftSamples-currentValue" class="spec-settings" @change="changeSpectrogramNumberOfSamples($event)">
            <option value="256">256</option>
            <option value="512">512</option>
            <option selected value="1024">1024</option>
            <option value="2048">2048</option>
        </select>
    </div>
    <div class="rounded border-b m-3  ">
        <span class="spec-settings-text">Max frequency: </span>
        <input type="range" min="1" max="24000" step="100" v-model="fftsamplesSelected" @change="changeSpectrogramMaxFrequency(fftsamplesSelected)" >
        <div class=" border-l border-r border-t rounded px-1 ml-33 pt-1 text-white inline ">
            <input type="number" v-model="fftsamplesSelected" class="mt-1 w-15 bg-blue-900">
            <span>Hz</span>
        </div>
    </div>
    <span class="spec-settings-text m-3">Type of the window: </span>
    <select id="window-currentValue" class="spec-settings" @change="changeSpectrogramWindow($event)">
        <option value="bartlett">bartlett</option>
        <option value="bartlettHann">bartlettHann</option>
        <option value="blackman">blackman</option>
        <option value="cosine">cosine</option>
        <option value="gauss">gauss</option>
        <option value="hamming">hamming</option>
        <option selected value="hann">hann - default</option>
        <option value="lanczoz">lanczoz</option>
        <option value="rectangular">rectangular</option>
        <option value="triangular">triangular</option>
    </select>
    
</div> -->
</template>

<style scoped>
.spec-settings {
  border-radius: inherit;
  margin-bottom: 2px;
}
.spec-settings-text {
  color: white;
  margin-right: 10px;
}
</style>
