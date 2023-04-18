<script setup>
import { ref } from 'vue';
import BlueButtons from '../../../buttons/BlueButtons.vue';
import SizeSetter from '../../../tools/SizeSetter.vue';
import ColorsPicker from '../../../visualizationManager/ColorsPicker.vue';
import { trackList } from '../../../../stores/globalStores';
import { updateRecording } from '../../../../composables/custom';
const showColorPicker = ref(false);
const showSizeSetter = ref(false);
const currentTrackList = trackList()
const chartType = ref(currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].graph_type)


const props = defineProps({
    id: Number,
    selectedIntervalVis: String,

})
const changeColor = (e) => { 
  currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].graph_color = e;
  updateRecording(props.id,'graph_color', e, props.selectedIntervalVis)
};

const changeChartType = () => {
  if(chartType.value == 'bar'){
    chartType.value = 'line'
  }else{
    chartType.value = 'bar'
  }
  setTimeout(() => {
    currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].graph_type = chartType.value
  updateRecording(props.id,'graph_type', chartType.value, props.selectedIntervalVis)
    
  }, 0);
}

</script>


<template>

 <div class="flex flex-col bg-white box rounded-md py-2 px-1  w-full items-center  gap-1" >
    <div class="flex  gap-1">
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
        :icon="currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].graph_type == 'line' ? 'mdi:graph-bell-curve-cumulative' :'ep:histogram'" 
        @click="changeChartType()" 
        :icon-class="'ml-0'"
        class="w-max"
        ></BlueButtons> 

    </div>

    <Transition>
        <SizeSetter
        v-if="showSizeSetter"
        :id="id"
        :visualization="selectedIntervalVis"
        :loading-visualization="'isSpectrogramLoading'"
        :min-value="50"
        :max-value="300"
        :interval="10"
        />
    </Transition>


    <ColorsPicker v-if="showColorPicker" :selected-color="currentTrackList.selectTrack(props.id)[props.selectedIntervalVis].graph_color" class="h-27 w-full" @update-color="changeColor($event)" :format="'hex'" />

 </div>



</template>