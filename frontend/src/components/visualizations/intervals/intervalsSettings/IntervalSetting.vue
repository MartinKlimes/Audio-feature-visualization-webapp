<script setup>
import { trackList } from "../../../../stores/globalStores";
import BlueButtons from "../../../buttons/BlueButtons.vue";
import ColorsPicker from "../../../visualizationManager/ColorsPicker.vue";
import { ref, watch} from "vue";
import { Icon } from "@iconify/vue";
import { updateRecording } from "../../../../../custom";
import IntervalAverage from "./IntervalAverage.vue";
import SizeSetter from "../../../tools/SizeSetter.vue";

const currentTrackList = trackList();

const showColorPicker = ref(false);
const showSizeSetter = ref(false);
const selectedIntervalVis = ref(null);
const isInterval = ref(null)
const showAverageSetting = ref(false)
const props = defineProps({
  track: Object,
  selectedVis: Number,
});




const changeColor = (e) => { 
  
  currentTrackList.selectTrack(props.track.id)[selectedIntervalVis.value].graph_color = e;
};

watch(
  () => props.selectedVis,
  () => {
    if(props.selectedVis == 3){
      selectedIntervalVis.value = 'imi_data'
      isInterval.value = 'isIMI'
    } else if (props.selectedVis == 4){
      console.log(selectedIntervalVis.value);
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
  <div class="flex flex-col items-center relative h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 shadow-md">
    <div class="flex gap-1 boxTight rounded-md p-0.5">
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

    <div class="flex gap-1 mt-2 ">
      <BlueButtons
        :disabled="!selectedIntervalVis"
        :is-disabled="!selectedIntervalVis"
        :icon="'ic:outline-color-lens'"
        @click="showColorPicker = !showColorPicker"
        :is-btn-clicked="showColorPicker"
        :icon-class="'ml-0'"
      ></BlueButtons>

      <BlueButtons 
        :icon="'nimbus:size-height'" 
        @click="showSizeSetter = !showSizeSetter" 
        :is-btn-clicked="showSizeSetter" 
        :icon-class="'ml-0'"
        :disabled="!selectedIntervalVis"
        :is-disabled="!selectedIntervalVis"
        class="w-max"
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
    <Transition>
    <IntervalAverage
    v-if="showAverageSetting"
    :id="track.id"
    :selectedIntervalVis="selectedIntervalVis"
    />
  </Transition>

  <Transition>
        <SizeSetter
        v-if="showSizeSetter"
        :id="track.id"
        :visualization="selectedIntervalVis"
        :loading-visualization="'isSpectrogramLoading'"
        :min-value="50"
        :max-value="300"
        :interval="10"
        />
    </Transition>


    <ColorsPicker v-if="showColorPicker" class="h-27 w-full" @update-color="changeColor($event)" :format="'hex'" />

    
    <button v-if="!showColorPicker && !showAverageSetting && !showSizeSetter" title="Delete pianoroll" class="mt-4 opacity-50 absolute bottom-0 right-0 hover:opacity-100" @click="remove()">
      <Icon icon="mingcute:delete-2-line" />
    </button>


  </div>
  
</template>
