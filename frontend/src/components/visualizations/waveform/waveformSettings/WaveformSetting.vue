<script setup>
import { Icon } from "@iconify/vue";
import { ref } from "vue";
import {alertState } from "../../../../stores/globalStores";
import BlueButtons from "../../../buttons/BlueButtons.vue";
import ExportBtn from "../../../buttons/ExportBtn.vue";
import { updateRecording } from "../../../../composables/custom";
import WaveformMarkers from "./WaveformMarkers.vue";
import WaveformStyle from "../waveformStyle/WaveformStyle.vue";
import WaveformTrim from "./WaveformTrim.vue";
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();

const alertGlobalState = alertState();



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




</script>

<template>
  <div class="flex flex-col items-center relative h-max w-full py-2 bg-gray-200 rounded-md border border-gray-300 shadow-md">
    <!-- <Icon  class="absolute left-1 top-1 rounded"  :class="track.backgroundColor" icon="mdi:waveform" /> -->

    <BlueButtons
      :is-btn-clicked="showLinesVis"
      :icon="'material-symbols:add-circle-outline'"
      @click="showLinesVis = !showLinesVis"
      :class="{ blink: alertGlobalState.message.includes('bars') }"
      >{{t('Visualization.add')}}</BlueButtons
    >

    <Transition>
      <keep-alive>
        <WaveformMarkers
          v-if="showLinesVis"
          :track-name="track.trackName"
          :id="track.id"
          :txt-file-name="track.txtFileName"
          :background-color="track.backgroundColor"
        />
      </keep-alive>
    </Transition>

    <ExportBtn :id="track.id" :track-name="track.trackName" :visualization="'waveform'" class="absolute top-0 right-0" />

    <WaveformTrim
    :id="track.id"
    :track-name="track.trackName"
    />
    
  
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
