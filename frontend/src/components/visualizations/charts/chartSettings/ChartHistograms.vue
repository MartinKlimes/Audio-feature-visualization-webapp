<script setup>
import VueSlider from "vue-slider-component";
import { trackList } from "../../../../stores/globalStores";
import { onUnmounted, ref, watch } from "vue";

const currentTrackList = trackList();
const windowSize = ref(20);
const values = ["Time frame", "Lenght frame"];
const selectedValue = ref();
const props = defineProps({
  id: Number,
  selectedIntervalVis: String,
});

const changeFrameSize = () => {
  if (selectedValue.value == "Time frame") {
    currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].histogramLengthFrameSize = 0;
    setTimeout(() => {
      currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].histogramTimeFrameSize = windowSize.value;
    }, 0);
  } else {
    currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].histogramTimeFrameSize = 0;
    setTimeout(() => {
      currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].histogramLengthFrameSize = windowSize.value;
    }, 0);
  }
};
onUnmounted(() => {
  currentTrackList.selectTrack(props.id)[props.selectedIntervalVis][`${props.selectedIntervalVis}Height`] =
    currentTrackList.selectTrack(props.id)[props.selectedIntervalVis][`${props.selectedIntervalVis}Height`] - 1;
});
</script>

<template>
  <div class="box p-2 w-full bg-white rounded-md mt-2 flex flex-col items-center">
    <div>
      <div v-for="value in values" :key="value">
        <input :id="value" type="radio" :value="value" v-model="selectedValue" @change="changeFrameSize()" class="cursor-pointer" />
        <label :for="value" class="font-bold text-xs ml-1">{{ value }}</label>
      </div>
    </div>

    <div class="mt-2 flex flex-col items-center boxTight rounded-md py-1">
      <span class="text-sm opacity-40 font-bold px-1">Frame size: {{ windowSize }}</span>
    </div>

    <vue-slider
      v-model="windowSize"
      @change="changeFrameSize($event)"
      :min="0"
      :width="112"
      :max="200"
      :tooltipStyle="{ backgroundColor: 'Blue' }"
      :processStyle="{ backgroundColor: 'Blue' }"
      :dotStyle="{ backgroundColor: 'Blue' }"
      :railStyle="{ backgroundColor: 'RoyalBlue' }"
      :stepStyle="{ backgroundColor: 'RoyalBlue' }"
      :labelStyle="{ fontSize: '10px', fontFamily: 'Courier New', fontWeight: 'bold' }"
    ></vue-slider>
  </div>
</template>
