<script setup>
import BlueButttons from "../buttons/BlueButtons.vue";
import { updateRecording } from "../../../custom";
import { showAlert, closeAlert } from "../../alerts";

const props = defineProps({
  track: Object,
});

const createVisualization = (visualization, isVisualization, isVisualizationDisplayed) => {
  updateRecording(props.track.id, isVisualizationDisplayed, !visualization[isVisualizationDisplayed]);

  if (!visualization[isVisualization]) {
    // visualization[isVisualization + 'Loading'] = true
    visualization[isVisualization] = true;
    visualization[isVisualizationDisplayed] = true;
    updateRecording(props.track.id, isVisualization, true);
  } else {
    visualization[isVisualizationDisplayed] = !visualization[isVisualizationDisplayed];
  }
};

const createPianoroll = () => {
  if (props.track.MIDIFileName) {
    createVisualization(props.track.pianoroll, "isPianoroll", "isPianorollDisplayed");
  } else {
    showAlert("First select MIDI file!");
    setTimeout(closeAlert, 1500);
  }
};

const createIMI = () => {
  if (props.track.txtFileName) {
    createVisualization(props.track.imi_data, "isIMI", "isIMIDisplayed");
  } else {
    showAlert("First select text file!");
    setTimeout(closeAlert, 1500);
  }
}
</script>

<template>
  <div class="h-[47%] w-full mt-5 p-2 border boxTight border-gray-500 rounded-md bg-white ">
    <div class="grid grid-cols-2 gap-2 ">
      <!-- <button class="btn-hover-cursor font-semibold w-22 shadow-sm shadow-dark-100" :class="{'bg-lime-500 hover:bg-lime-400': track.isWaveformDisplayed && !track.isWaveformLoading, 
            'bg-yellow-100 hover:bg-yellow-50' : track.isWaveform && !track.isWaveformDisplayed || track.isWaveformLoading,
         }" @click="createWaveform">Waveform <Icon
            v-if="track.isWaveformLoading == true"
            icon="fa:spinner"
            class="spin"
            :inline=true
            
           />
        </button> -->

      <BlueButttons
        :is-btn-clicked="track.waveform.isWaveformDisplayed"
        :isDisabled="!track.waveform.isWaveform"
        icon-class="hidden"
        @click="createVisualization(track.waveform, 'isWaveform', 'isWaveformDisplayed')"
        class="h-6"
        >Waveform</BlueButttons
      >

      <BlueButttons
        :is-btn-clicked="track.spectrogram.isSpectrogramDisplayed"
        :isDisabled="!track.spectrogram.isSpectrogram"
        @click="createVisualization(track.spectrogram, 'isSpectrogram', 'isSpectrogramDisplayed')"
        class="h-6"
        >Spectrogram</BlueButttons
      >

      <!-- <BlueButttons   @click="createSpectrogram()" class="h-6">Spectrogram</BlueButttons> -->

      <BlueButttons
        :is-btn-clicked="track.pianoroll.isPianorollDisplayed"
        :isDisabled="!track.pianoroll.isPianoroll"
        @click="createPianoroll"
        class="h-6"
      >
        Pianoroll</BlueButttons
      >

      <div class="flex w-22 h-max gap-1">
        <BlueButttons
        :is-btn-clicked="track.imi_data.isIMIDisplayed"
        :isDisabled="!track.imi_data.isIMI"
        @click="createIMI()"
        class="h-6 rounded-r-none px-0.8"
      >IMI</BlueButttons>
        <BlueButttons
        :is-btn-clicked="track.ioi_data.isIOIDisplayed"
        :isDisabled="!track.ioi_data.isIOI"
        @click="createVisualization(track.ioi_data, 'isIOI', 'isIOIDisplayed')"
      
        class="h-6 rounded-x-none"
      >IOI</BlueButttons>
        <BlueButttons
        :is-btn-clicked="track.ibi_data.isIBIDisplayed"
        :isDisabled="!track.ibi_data.isIBI"
        @click="createVisualization(track.ibi_data, 'isIBI', 'isIBIDisplayed')"
        
        class="h-6 rounded-l-none"
      >IBI</BlueButttons>

        <!-- <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-r-none" @click="">IOI</button>
        <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-l-none">IBI</button> -->
      </div>

      <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Tempo</button>
      <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">RMS</button>
    </div>
  </div>
</template>
