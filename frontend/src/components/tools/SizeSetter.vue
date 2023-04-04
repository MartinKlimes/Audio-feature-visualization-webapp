<script setup>
import { wavesurfer } from '../../functions/waveform';
import { updateRecording } from '../../../custom';
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/material.css";
import { ref } from 'vue';
import { trackList } from '../../globalStores';

const currentTrackList = trackList()
const value = ref(currentTrackList.selectTrack(props.id)[props.visualization][`${props.visualization}Height`])

const changeSize = (e) => {
  currentTrackList.selectTrack(props.id)[props.visualization][props.loadingVisualization] = true
  setTimeout(() => {

    if(props.visualization == 'spectrogram'){
        wavesurfer[props.id].spectrogram.params.height = e
        wavesurfer[props.id].spectrogram.init();
    } else if (props.visualization == 'waveform'){
        wavesurfer[props.id].setHeight(e)
    } else{
        currentTrackList.selectTrack(props.id).pianoroll.pianorollHeight = e;
    }
    updateRecording(props.id,`${props.visualization}Height`, e)
    currentTrackList.selectTrack(props.id)[props.visualization][props.loadingVisualization] = false

  }, 10);
//   currentTrackList.selectTrack(props.id).spectrogram.spectrogramHeight = e
}

const props = defineProps({
    id: Number,
    visualization: {
        required: true,
        type: String
    },
    loadingVisualization: {
        required: true,
        type: String
    }
})

</script>



<template>

    <!-- <SetSize
    :default-size="wavesurfer[id].spectrogram.params.height"
    @change-size="changeSize($event)"
    /> -->
    <div class="box p-1 bg-white rounded-md mt-2 flex flex-col items-center">

   
    <vue-slider
      @change="changeSize($event)"
      v-model="value"
      :direction="'ttb'"
      :width="6"
      :height="150"
      :min="100"
      :max="1000"
      :interval="100"
      :marks="true"
      :lazy="true"
      :tooltipStyle="{ backgroundColor: 'Blue' }"
      :processStyle="{ backgroundColor: 'Blue' }"
      :dotStyle="{ backgroundColor: 'Blue' }"
      :railStyle="{ backgroundColor: 'CornflowerBlue' }"
      :stepStyle="{ backgroundColor: 'RoyalBlue	' }"
      :stepActiveStyle="{ backgroundColor: 'black' }"
      :labelActiveStyle ="{ backgroundColor: 'CornflowerBlue' }"
      :labelStyle="{ opacity: 0 }"

    ></vue-slider>
    <span class="mt-1 text-xs font-bold">{{ value }}px</span>

  </div>
</template>