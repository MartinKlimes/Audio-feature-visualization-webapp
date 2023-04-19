<script setup>
import { Icon } from "@iconify/vue";
import { ref, shallowRef } from "vue";
import BarSelection from "./BarSelection.vue";
import TimeSelection from "./TimeSelection.vue";
import { api } from "../../../../composables/custom";
import { trackIndex, trackList, alertState } from "../../../../stores/globalStores";
import BlueButtons from "../../../buttons/BlueButtons.vue";
import ExportBtn from "../../../buttons/ExportBtn.vue";
import { updateRecording } from "../../../../composables/custom";
import { getCookie } from "../../../../composables/cookieHandling";
import { showAlert, closeAlert } from "../../../../composables/alerts";
import MarkersVis from "./MarkersVis.vue";
import WaveformStyle from "../waveformStyle/WaveformStyle.vue";
const alertGlobalState = alertState();

const currentSetting = shallowRef();
const loading = ref(false);
const currentTrackList = trackList();

const showLinesVis = ref(false);
const showAppearance = ref(false);

const props = defineProps({
  track: Object,
});

const removeWaveform = () => {
  props.track.waveform.isWaveform = false;
  props.track.waveform.isWaveformDisplayed = false;
  updateRecording(props.track.id, "isWaveform", false);
  updateRecording(props.track.id, "isWaveformDisplayed", false);
};

const showBarsToSelect = () => {
  if (document.querySelector(`#bars-marker-${props.track.id}`)) {
    currentSetting.value === BarSelection ? (currentSetting.value = "") : (currentSetting.value = BarSelection);
  } else {
    showAlert("First display bars!");
    setTimeout(closeAlert, 1500);
  }
};

const trimAudio = (event) => {
  loading.value = true;
  const record_name = props.track.trackName;
  const start = event[0];
  const end = event[1];
  const fromBar = event[2] || false;
  const toBar = event[3] || false;
  api
    .post(
      "/trim-audio",
      {
        record_name,
        start,
        end,
        fromBar,
        toBar,
      },
      {
        headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token"),
          "Content-Type": "multipart/form-data",
        },
      }
    )
    .then((response) => {
      currentTrackList.fetchRecordings().then(() => {
        const track = currentTrackList.selectTrack(response.data.id);
        track.waveform.isWaveform = true;
        track.waveform.isWaveformDisplayed = true;
        loading.value = false;
        currentSetting.value = null;
      });
    });
};
</script>

<template>
  <div class="flex flex-col items-center relative h-max w-full py-2 bg-gray-200 rounded-md border border-gray-300 shadow-md">
    <!-- <Icon  class="absolute left-1 top-1 rounded"  :class="track.backgroundColor" icon="mdi:waveform" /> -->

    <BlueButtons
      :is-btn-clicked="showLinesVis"
      :icon="'material-symbols:add-circle-outline'"
      @click="showLinesVis = !showLinesVis"
      :class="{ blink: alertGlobalState.message.includes('bars') }"
      >Add</BlueButtons
    >

    <Transition>
      <keep-alive>
        <MarkersVis
          v-if="showLinesVis"
          :track-name="track.trackName"
          :id="track.id"
          :txt-file-name="track.txtFileName"
          :background-color="track.backgroundColor"
        />
      </keep-alive>
    </Transition>

    <ExportBtn :id="track.id" :track-name="track.trackName" :visualization="'waveform'" class="absolute top-0 right-0" />

    <span class="text-xs opacity-50 mt-2">Select part</span>
    <div class="flex border border-dashed border-gray-400 rounded-md p-1 justify-center items-center mb-1">
      <BlueButtons
        class="mr-1"
        @click="showBarsToSelect()"
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
        <component :is="currentSetting" :trackName="track.trackName" :id="track.id" :loading="loading" @trim-audio="trimAudio($event)" />
      </KeepAlive>
    </transition>

    <BlueButtons
      class="mt-2 flex"
      @click="showAppearance = !showAppearance"
      :icon="'dashicons:admin-appearance'"
      :icon-class="'ml-0'"
      :is-btn-clicked="showAppearance"
      title="Appearance"
    ></BlueButtons>
    <transition>
      <WaveformStyle
        v-if="showAppearance"
        :track-name="track.trackName"
        :id="track.id"
        :waveform-color="track.waveformColor"
        :waveform-height="track.waveform.waveformHeight"
        :split-channels="track.waveform.splitChannels"
        @close-modal="showAppearance = false"
      />
    </transition>

    <button
      v-if="!showAppearance"
      title="delete waveform"
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

<style scoped>
overflow {
  overflow: visible;
}
</style>
