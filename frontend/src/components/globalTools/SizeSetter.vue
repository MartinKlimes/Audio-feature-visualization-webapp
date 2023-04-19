<script setup>
import { wavesurfer } from "../../functions/waveform/waveform";
import { updateRecording } from "../../composables/custom";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/material.css";
import { ref } from "vue";
import { trackList } from "../../stores/globalStores";

const currentTrackList = trackList();

const changeSize = (e) => {
  currentTrackList.selectTrack(props.id)[props.visualization][props.loadingVisualization] = true;
  setTimeout(() => {
    if (props.visualization == "spectrogram") {
      wavesurfer[props.id].spectrogram.params.height = e;
      wavesurfer[props.id].spectrogram.init();
    } else if (props.visualization == "waveform") {
      wavesurfer[props.id].setHeight(e);
    } else if (props.visualization == "pianoroll") {
      currentTrackList.selectTrack(props.id).pianoroll.pianorollHeight = e;
    } else {
      currentTrackList.selectTrack(props.id)[props.visualization][`${props.visualization}Height`] = e;
    }
    updateRecording(props.id, `${props.visualization}Height`, e);
    currentTrackList.selectTrack(props.id)[props.visualization][props.loadingVisualization] = false;
  }, 10);
  //   currentTrackList.selectTrack(props.id).spectrogram.spectrogramHeight = e
};

const props = defineProps({
  id: Number,
  visualization: {
    required: true,
    type: String,
  },
  loadingVisualization: {
    required: true,
    type: String,
  },
  minValue: {
    type: Number,
    default: 100,
  },
  maxValue: {
    type: Number,
    default: 1000,
  },
  interval: {
    type: Number,
    default: 100,
  },
  lazy: {
    type: Boolean,
    default: true,
  },
});
</script>

<template>
  <div class="box p-1 bg-white rounded-md mt-2 flex flex-col items-center min-w-11">
    <vue-slider
      @change="changeSize($event)"
      v-model="currentTrackList.selectTrack(props.id)[props.visualization][`${props.visualization}Height`]"
      :direction="'ttb'"
      :width="6"
      :height="150"
      :min="minValue"
      :max="maxValue"
      :interval="interval"
      :marks="true"
      :lazy="lazy"
      :tooltipStyle="{ backgroundColor: 'Blue' }"
      :processStyle="{ backgroundColor: 'Blue' }"
      :dotStyle="{ backgroundColor: 'Blue' }"
      :railStyle="{ backgroundColor: 'CornflowerBlue' }"
      :stepStyle="{ backgroundColor: 'RoyalBlue	' }"
      :stepActiveStyle="{ backgroundColor: 'black' }"
      :labelActiveStyle="{ backgroundColor: 'CornflowerBlue' }"
      :labelStyle="{ opacity: 0 }"
    ></vue-slider>
    <span class="mt-1 text-xs font-bold"
      >{{ currentTrackList.selectTrack(props.id)[props.visualization][`${props.visualization}Height`] }}px</span
    >
  </div>
</template>
