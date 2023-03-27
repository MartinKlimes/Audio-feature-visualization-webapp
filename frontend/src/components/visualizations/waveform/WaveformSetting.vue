<script setup>
import { Icon } from "@iconify/vue";
import { ref, shallowRef } from "vue";
import BarSelection from "./BarSelection.vue";
import TimeSelection from "./TimeSelection.vue";
import ColorWaveform from "./ColorWaveform.vue";
import { wavesurfer, marker } from "../../../functions/waveform";
import { api } from "../../../../custom";
import { trackIndex, trackList } from "../../../globalStores";
import BlueButtons from "../../buttons/BlueButtons.vue";
import { updateRecording } from "../../../../custom";
import IOI from "./IOI.vue";
import LinesVisualizations from "./LinesVisualizations.vue";
import { getCookie } from "../../../cookieHandling";

const currentSetting = shallowRef();
const loading = ref(false);
const currentTrackList = trackList();
const showColorPicker = ref(false);
const isBtnClicked = ref(false);
const bars = ref();
const showLinesVis = ref(false);

const props = defineProps({
  track: Object,
});

const removeWaveform = () => {
  props.track.waveform.isWaveform = false;
  props.track.waveform.isWaveformDisplayed = false;
  updateRecording(props.track.id, "isWaveform", false);
  updateRecording(props.track.id, "isWaveformDisplayed", false);
};

// const showBars = () => {
//     if(!props.track.txtFileName){
//         showAlert('First select the text file!');
//         setTimeout(closeAlert, 1500);
//     } else {
//         isBtnClicked.value = true
//     }
// }
const showBarsToSelect = () => {
    if(document.querySelector(`#bars-marker-${props.track.id}`)){
        
    currentSetting.value === BarSelection ? (currentSetting.value = "") : (currentSetting.value = BarSelection);
       
        console.log(wavesurfer[props.track.id].backend);



    }

   


//   if (!isBtnClicked.value) {
//     showBars();
//   }
//   if (props.track.txtFileName) {
    // currentSetting.value === BarSelection ? (currentSetting.value = "") : (currentSetting.value = BarSelection);

}

const trimAudio = (event) => {
  loading.value = true;
  const record_name = props.track.trackName
  const start = event[0]
  const end = event[1]
  const fromBar = event[2]
  const toBar = event[3]
  api.post('/trim-audio', {
    record_name,
    start,
    end,
    fromBar,
    toBar
  }, {
  headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      'Content-Type': 'multipart/form-data'
  }
  })
  .then(response => {
  currentTrackList.fetchRecordings().then(() => {
    currentTrackList.selectTrack(response.data.id).waveform.isWaveform = true
    currentTrackList.selectTrack(response.data.id).waveform.isWaveformDisplayed = true
    loading.value = false;
  })
  
  
  })
  // api
  //   .get("/trim-audio/" + props.track.trackName + "/" + event[0] + "/" + event[1] + "/" + event[2] + "/" + event[3])
  //   .then((response) => {
  //     // console.log(response.data);
  //     currentTrackList.fetchRecordings();
  //     loading.value = false;
  //   });
};

const splitChannels = () => {
  props.track.waveform.splitChannels = !props.track.waveform.splitChannels;
  props.track.waveform.isWaveform = false;
  api.get("/change-track-status/splitChannels/" + props.track.trackName + "/''");
  setTimeout(() => {
    props.track.waveform.isWaveform = true;
  }, 500);
};
</script>

<template>
  <div
    class="flex flex-col items-center relative h-max w-full py-2 bg-gray-200 rounded-md border border-gray-300 shadow-md"
  >
    <!-- <Icon  class="absolute left-1 top-1 rounded"  :class="track.backgroundColor" icon="mdi:waveform" /> -->

    <BlueButtons
      :is-btn-clicked="showLinesVis"
      :icon="'material-symbols:add-circle-outline'"
      @click="showLinesVis = !showLinesVis"
      >Add</BlueButtons
    >

    <Transition>
      <keep-alive>
        <LinesVisualizations
          v-if="showLinesVis"
          :track-name="track.trackName"
          :id="track.id"
          :txt-file-name="track.txtFileName"
          :background-color="track.backgroundColor"
        />
      </keep-alive>
    </Transition>

    <button v-if="!isBtnClicked" class="absolute top-0 right-1 opacity-50 hover:opacity-100">
      <Icon icon="entypo:export" @click="wavesurfer[track.id].exportImage()" />
    </button>

    <span class="text-xs opacity-50 mt-3">Select part</span>
    <div class="flex border border-dashed border-gray-400 rounded-md p-1 justify-center items-center">
      <BlueButtons
        class="mr-1"
        @click="showBarsToSelect()"
        :class="{ 'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-transparent': !track.txtFileName }"
        :icon="'material-symbols:content-cut-rounded'"
        :is-btn-clicked="currentSetting === BarSelection"
        >Bars</BlueButtons
      >
      <BlueButtons
        @click="currentSetting === TimeSelection ? (currentSetting = '') : (currentSetting = TimeSelection)"
        :icon="'material-symbols:content-cut-rounded'"
        :is-btn-clicked="currentSetting === TimeSelection"
        >Time</BlueButtons
      >
    </div>
    <transition>
      <KeepAlive>
        <component
          :is="currentSetting"
          :trackName="track.trackName"
          :id="track.id"
          :loading="loading"
          @trim-audio="trimAudio($event)"
        />
      </KeepAlive>
    </transition>

    <BlueButtons
      :icon="'ic:outline-color-lens'"
      @click="showColorPicker = !showColorPicker"
      :is-btn-clicked="showColorPicker"
      class="mt-3"
      >Color</BlueButtons
    >

    <Transition>
      <ColorWaveform
        v-if="showColorPicker"
        :id="track.id"
        :trackName="track.trackName"
        :waveformColor="track.waveform.waveformColor"
        @close-waveform-color-picker="showColorPicker = false"
      />
    </Transition>

    <BlueButtons
      title="Split channels"
      class="mt-3 items-center opacity-90"
      :is-btn-clicked="track.splitChannels"
      @click="splitChannels()"
      :icon-class="'ml-0 '"
      :rotate="1"
      :icon="'carbon:split-screen'"
    ></BlueButtons>

    <button
      title="reload waveform"
      class="mt-4 opacity-50 hover:opacity-100 absolute right-0 bottom-0"
      @click="removeWaveform"
    >
      <Icon icon="mingcute:delete-2-line" />
    </button>
    <!-- <Transition>
    <div v-if="showColorPicker"  class="flex flex-col w-10 p-1  rounded-md gap-1 bg-white absolute z-5 -bottom-51 -right-2">
        <BlueButtons :icon="'material-symbols:line-end-arrow-notch'" class="items-center justify-center h-4" 
        :is-btn-clicked="setWaveformColor == 'setProgressColor'" 
        @click="setWaveformColor = 'setProgressColor'"></BlueButtons>

        <BlueButtons :icon="'material-symbols:line-start-arrow-notch'"  class="items-center justify-center h-4 " 
        :is-btn-clicked="setWaveformColor == 'setWaveColor'" 
        @click="setWaveformColor = 'setWaveColor'"></BlueButtons>
    </div>
    </Transition> -->
  </div>
</template>

<style scoped></style>
