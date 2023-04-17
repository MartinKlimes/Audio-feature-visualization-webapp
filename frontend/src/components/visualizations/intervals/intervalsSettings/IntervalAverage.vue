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
  <div class="boxTight mt-2 w-full h-max bg-gray-100 rounded-md flex items-start pt-1 flex-col justify-center">

    <div>
      <input id="horizontal-average" type="checkbox"  @change="toggleHorizontalAverage" class="cursor-pointer ml-2" :checked="currentTrackList.selectTrack(id)[selectedIntervalVis].showHorizontalAverage" />
      <label for="horizontal-average" class="font-bold text-xs ml-1">Average (line)</label>
    </div>
    <div>
      <input id="moving-average" type="checkbox"  @change="toggleMovingAverage" class="cursor-pointer ml-2"  :checked="currentTrackList.selectTrack(id)[selectedIntervalVis].showMovingAverage" />
      <label for="moving-average" class="font-bold text-xs ml-1">Moving Average</label>
    </div>

    <div v-if="currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].showMovingAverage" class="mt-2 flex flex-col items-center  rounded-md py-1 ">
        <span class="text-sm opacity-40 font-bold boxTight p-1 rounded-md">window size: {{ windowSize }}</span>
    

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
