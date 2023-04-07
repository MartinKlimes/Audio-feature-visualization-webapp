<script setup>
import VueSlider from "vue-slider-component";
import { trackList } from "../../../../stores/globalStores";
import { ref } from "vue";

const currentTrackList = trackList();
const windowSize = ref(20)

const props = defineProps({
  id: Number,
  selectedIntervalVis: String,
});
const changeWindowSize = (e) => {
  currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].movingAverageWindowSize = e;
};

const toggleHorizontalAverage = () => {
  currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].showHorizontalAverage =! currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].showHorizontalAverage
    
}
const toggleMovingAverage = () => {
    currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].showMovingAverage =! currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].showMovingAverage
    
}
</script>

<template>
  <div class="boxTight mt-2 w-full h-max rounded-md flex items-start pt-1 flex-col justify-center">

    <div>
      <input type="checkbox"  @change="toggleHorizontalAverage" class="cursor-pointer ml-2" :checked="currentTrackList.selectTrack(id)[selectedIntervalVis].showHorizontalAverage" />
      <label class="font-bold text-xs ml-1">Average (line)</label>
    </div>
    <div>
      <input type="checkbox"  @change="toggleMovingAverage" class="cursor-pointer ml-2"  :checked="currentTrackList.selectTrack(id)[selectedIntervalVis].showMovingAverage" />
      <label class="font-bold text-xs ml-1">Moving Average</label>
    </div>

    <div v-if="currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].showMovingAverage" class="mt-2 flex flex-col items-center boxTight rounded-md py-1">
        <span class="text-sm opacity-40 font-bold">window size: {{ windowSize }}</span>
    

    <vue-slider
    v-model="windowSize"
    @change="changeWindowSize($event)"
    :min="0"
    :width="130"
    :max="200"
    :tooltipStyle="{ backgroundColor: 'Blue' }"
    :processStyle="{ backgroundColor: 'Blue' }"
    :dotStyle="{ backgroundColor: 'Blue' }"
    :railStyle="{ backgroundColor: 'RoyalBlue' }"
    :stepStyle="{ backgroundColor: 'RoyalBlue' }"
    :labelStyle="{ fontSize: '10px', fontFamily: 'Courier New', fontWeight: 'bold' }"
    ></vue-slider>
    </div>
  </div>
</template>
