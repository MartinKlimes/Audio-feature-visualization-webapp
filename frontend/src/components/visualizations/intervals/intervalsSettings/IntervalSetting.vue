<script setup>
import { trackList } from "../../../../stores/globalStores";
import BlueButtons from "../../../buttons/BlueButtons.vue";
import { ref, watch} from "vue";
import { Icon } from "@iconify/vue";
import { updateRecording } from "../../../../../custom";
import IntervalAverage from "./IntervalAverage.vue";
import IntervalStyle from "../intervalsStyle/IntervalStyle.vue";
import IntervalHistograms from "./IntervalHistograms.vue";

const currentTrackList = trackList();

const selectedIntervalVis = ref(null);
const isInterval = ref(null)
const showAverageSetting = ref(false)
const showIntervalStyle = ref(false)
const showHistogramSetting = ref(false)

const props = defineProps({
  track: Object,
  selectedVis: Number,
});






watch(
  () => props.selectedVis,
  () => {
    if(props.selectedVis == 3){
      selectedIntervalVis.value = 'imi_data'
      isInterval.value = 'isIMI'
    } else if (props.selectedVis == 4){
   
      selectedIntervalVis.value = 'ioi_data'
      isInterval.value = 'isIOI'
    }else if (props.selectedVis == 5){
      selectedIntervalVis.value = 'ibi_data'
      isInterval.value = 'isIBI'
    }
  }, {immediate: true}
);

const remove = () => {
    currentTrackList.selectTrack(props.track.id)[selectedIntervalVis.value][isInterval.value] = false
    currentTrackList.selectTrack(props.track.id)[selectedIntervalVis.value][isInterval.value + 'Displayed'] = false
    updateRecording(props.track.id, isInterval.value, false);
    updateRecording(props.track.id, isInterval.value + 'Displayed', false);


}
</script>

<template>
  <div class="flex flex-col items-center relative h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 shadow-md gap-2">
    <div class="flex gap-1 boxTight rounded-md p-1">
      <BlueButtons
        @click="selectedIntervalVis = 'imi_data', selectedVis = 3"
        :is-btn-clicked="selectedVis == 3 && track.imi_data.isIMI"
        :is-disabled="!track.imi_data.isIMI"
        :disabled="!track.imi_data.isIMI"
        >IMI</BlueButtons
      >

      <BlueButtons
        @click="selectedIntervalVis = 'ioi_data', selectedVis = 4"
        :is-btn-clicked="selectedVis == 4 && track.ioi_data.isIOI"
        :is-disabled="!track.ioi_data.isIOI"
        :disabled="!track.ioi_data.isIOI"
        >IOI</BlueButtons
      >

      <BlueButtons
        @click="selectedIntervalVis = 'ibi_data', selectedVis = 5"
        :is-btn-clicked="  selectedVis == 5 && track.ibi_data.isIBI"
        :is-disabled="!track.ibi_data.isIBI"
        :disabled="!track.ibi_data.isIBI"
        >IBI</BlueButtons
      >
    </div>
    <div class="flex gap-1">
      <BlueButtons
        :icon="'game-icons:histogram'"
        @click="showHistogramSetting = !showHistogramSetting"
        :is-btn-clicked="showHistogramSetting"
        :icon-class="'ml-0'"
        :disabled="!selectedIntervalVis"
        :is-disabled="!selectedIntervalVis"
      ></BlueButtons>

      <BlueButtons
        :icon="'carbon:chart-average'"
        @click="showAverageSetting = !showAverageSetting"
        :is-btn-clicked="showAverageSetting"
        :icon-class="'ml-0'"
        :disabled="!selectedIntervalVis"
        :is-disabled="!selectedIntervalVis"
      ></BlueButtons>

    </div>

    <BlueButtons
    class=" flex"
    @click="showIntervalStyle = !showIntervalStyle"
    :icon="'dashicons:admin-appearance'"
    :icon-class="'ml-0'"
    :is-btn-clicked="showIntervalStyle"
    title="interval style"
    />
    

  <Transition>
    <IntervalStyle
    v-if="showIntervalStyle"
    :id="track.id"
    :selectedIntervalVis="selectedIntervalVis"
    
    />
  </Transition>

    <Transition>
    <IntervalAverage
    v-if="showAverageSetting"
    :id="track.id"
    :selectedIntervalVis="selectedIntervalVis"
    />
  </Transition>

    <Transition>
    <IntervalHistograms
    v-if="showHistogramSetting"
    :id="track.id"
    :selectedIntervalVis="selectedIntervalVis"
    />
  </Transition>

 

    
    <button v-if="!showIntervalStyle && !showHistogramSetting && !showAverageSetting" title="Delete pianoroll" class="mt-4 opacity-50 absolute bottom-0 right-0 hover:opacity-100" @click="remove()">
      <Icon icon="mingcute:delete-2-line" />
    </button>


  </div>
  
</template>
