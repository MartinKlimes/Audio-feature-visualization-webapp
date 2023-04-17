<script setup>
import { trackList } from "../../../../stores/globalStores";
import BlueButtons from "../../../buttons/BlueButtons.vue";
import { ref, watch} from "vue";
import { Icon } from "@iconify/vue";
import { updateRecording } from "../../../../../custom";
import IntervalAverage from "./IntervalAverage.vue";
import IntervalStyle from "../intervalsStyle/IntervalStyle.vue";
import IntervalHistograms from "./IntervalHistograms.vue";
import ExportBtn from "../../../buttons/ExportBtn.vue";
import VueSlider from "vue-slider-component";

const currentTrackList = trackList();

const selectedIntervalVis = ref(null);
const isInterval = ref(null);
const showAverageSetting = ref(false);
const showIntervalStyle = ref(false);
const showHistogramSetting = ref(false);
const frames = ref(null)

const props = defineProps({
  track: Object,
  selectedVis: Number,
});

watch(
  () => props.selectedVis,
  () => {
    if (props.selectedVis == 3) {
      selectedIntervalVis.value = "imi_data";
      isInterval.value = "isIMI";
    } else if (props.selectedVis == 4) {
      selectedIntervalVis.value = "ioi_data";
      isInterval.value = "isIOI";
    } else if (props.selectedVis == 5) {
      selectedIntervalVis.value = "ibi_data";
      isInterval.value = "isIBI";
    }else if (props.selectedVis == 6) {
      showHistogramSetting.value = false
      selectedIntervalVis.value = "Tempo_data";
      isInterval.value = "isTempo";
    }else if (props.selectedVis == 7) {
      showHistogramSetting.value = false
      selectedIntervalVis.value = "RMS_data";
      isInterval.value = "isRMS";
    }
    frames.value = props.track[selectedIntervalVis.value].numOfFrames
  },
  { immediate: true }
);

const remove = () => {
  currentTrackList.selectTrack(props.track.id)[selectedIntervalVis.value][isInterval.value] = false;
  currentTrackList.selectTrack(props.track.id)[selectedIntervalVis.value][isInterval.value + "Displayed"] = false;
  updateRecording(props.track.id, isInterval.value, false, selectedIntervalVis.value);
  updateRecording(props.track.id, isInterval.value + "Displayed", false, selectedIntervalVis.value);
};

const changeNumOfFrames = (e) => {
  currentTrackList.selectTrack(props.track.id)[selectedIntervalVis.value].numOfFrames = e
  updateRecording(props.track.id,'numOfFrames', e, selectedIntervalVis.value)

}
</script>

<template>
  <div class="flex flex-col items-center relative h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 shadow-md gap-2">
    <ExportBtn 
    :id="track.id" 
    :track-name="track.trackName" 
    :visualization="selectedVis == 3 ? 'measure' : selectedVis == 4 ? 'onset' : selectedVis == 5 ? 'beats' : selectedVis == 6 ? 'Tempo' : 'RMS'" 
    class="absolute top-0 right-0" />

    <div class="flex  boxTight rounded-md p-1 flex-col items-center  ">
      <div class="flex my-1 gap-1">
      <BlueButtons
        @click="(selectedIntervalVis = 'imi_data'), (selectedVis = 3)"
        :is-btn-clicked="selectedVis == 3 && track.imi_data.isIMI"
        :is-disabled="!track.imi_data.isIMI"
        :disabled="!track.imi_data.isIMI"
        >IMI</BlueButtons
      >

      <BlueButtons
        @click="(selectedIntervalVis = 'ioi_data'), (selectedVis = 4)"
        :is-btn-clicked="selectedVis == 4 && track.ioi_data.isIOI"
        :is-disabled="!track.ioi_data.isIOI"
        :disabled="!track.ioi_data.isIOI"
        >IOI</BlueButtons
      >

      <BlueButtons
        @click="(selectedIntervalVis = 'ibi_data'), (selectedVis = 5)"
        :is-btn-clicked="selectedVis == 5 && track.ibi_data.isIBI"
        :is-disabled="!track.ibi_data.isIBI"
        :disabled="!track.ibi_data.isIBI"
        >IBI</BlueButtons
      >
    </div>

    <BlueButtons
      v-if="track.Tempo_data.isTempoDisplayed"
      @click="(selectedIntervalVis = 'Tempo_data'), (selectedVis = 6)"
      :is-btn-clicked="selectedVis == 6 && track.Tempo_data.isTempo"
      :is-disabled="!track.Tempo_data.isTempo"
      :disabled="!track.Tempo_data.isTempo"
      class="w-15 mb-1"
      >Tempo</BlueButtons
    >
    <BlueButtons
      v-if="track.RMS_data.isRMSDisplayed"
        @click="(selectedIntervalVis = 'RMS_data'), (selectedVis = 7)"
        :is-btn-clicked="selectedVis == 7 && track.RMS_data.isRMS"
        :is-disabled="!track.RMS_data.isRMS"
        :disabled="!track.RMS_data.isRMS"
      class="w-15 mb-1"

        >RMS</BlueButtons
      >
    </div>
    <div v-if="['Tempo_data', 'RMS_data'].includes(selectedIntervalVis)" class=" flex flex-col items-center  rounded-md py-1 ">
        <span class="text-sm opacity-40 font-bold boxTight p-1 rounded-md">frames: {{ frames }}</span>
    
    <vue-slider
    
    v-model="frames"
    @change="changeNumOfFrames($event)"
    :lazy="true"
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

    <div class="flex gap-1 mt-1">
      <BlueButtons
        v-if="['ioi_data', 'ibi_data', 'imi_data'].includes(selectedIntervalVis)"
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
      <BlueButtons
        class="flex"
        @click="showIntervalStyle = !showIntervalStyle"
        :icon="'dashicons:admin-appearance'"
        :icon-class="'ml-0'"
        :is-btn-clicked="showIntervalStyle"
        title="interval style"
      />
    </div>

    <Transition>
      <IntervalStyle v-if="showIntervalStyle" :id="track.id" :selectedIntervalVis="selectedIntervalVis" />
    </Transition>

    <Transition>
      <IntervalAverage v-if="showAverageSetting" :id="track.id" :selectedIntervalVis="selectedIntervalVis" />
    </Transition>

    <Transition>
      <IntervalHistograms v-if="showHistogramSetting" :id="track.id" :selectedIntervalVis="selectedIntervalVis" />
    </Transition>

    <button
      v-if="!showIntervalStyle && !showHistogramSetting && !showAverageSetting"
      title="Delete pianoroll"
      class="mt-4 opacity-50 absolute bottom-0 right-0 hover:opacity-100"
      @click="remove()"
    >
      <Icon icon="mingcute:delete-2-line" />
    </button>
  </div>
</template>
