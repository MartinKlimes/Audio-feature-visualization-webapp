<script setup>
import WaveformSetting from "./visualizations/waveform/WaveformSetting.vue";
import PianorollSetting from "./visualizations/pianoroll/PianorollSetting.vue";
import SpectrogramSetting from "./visualizations/spectrogram/SpectrogramSetting.vue";
import IntervalSetting from "./visualizations/intervals/intervalsSettings/IntervalSetting.vue";
import BlueButttons from "./buttons/BlueButtons.vue";
import { shallowRef, watch, ref, watchEffect } from "vue";
import { Icon } from "@iconify/vue";
import { trackIndex } from "../stores/globalStores";

const currentTrackSetting = shallowRef();
const globalTrackIndex = trackIndex();

const visualizations = [
  [WaveformSetting, "mdi:waveform", 'waveform settings'],
  [SpectrogramSetting, "icon-park:music-rhythm", 'spectrogram settings'],
  [PianorollSetting, "ph:piano-keys-thin", 'pianoroll settings'],
  [IntervalSetting, "mdi:graph-areaspline", 'intervals settings']
]

const list = ref([]);

watchEffect(() => {
  list.value[0] = props.track.waveform.isWaveform;
  list.value[1] = props.track.spectrogram.isSpectrogram;
  list.value[2] = props.track.pianoroll.isPianoroll;
  list.value[3] = props.track.imi_data.isIMI || props.track.ioi_data.isIOI || props.track.ibi_data.isIBI

  for (let i = 0; i < list.value.length; i++) {
    if (list.value[i]) {
      currentTrackSetting.value = visualizations[i][0];
      break;
    }
  }
});

watchEffect(() => {
  if(props.selectedVis < 4){
    currentTrackSetting.value = visualizations[props.selectedVis][0];
  } else {
    currentTrackSetting.value = visualizations[3][0]
  }
});


const props = defineProps({
  track: Object,
  isSelected: Boolean,
  selectedVis: Number,
});
</script>

<template>
  <div v-show="isSelected" class="h-full p-1 rounded-md flex flex-col gap-1 items-center overflow-auto" :class="track.backgroundColor">
    <span class="max-w-37 overflow-x-auto whitespace-nowrap font-serif text-sm font-bold opacity-60 rounded-md overflow-hidden">
      {{ track.trackName }}
    </span>

    <div class="min-w-38 border-2 rounded-md border-gray">
      <div class="flex overflow-x-auto gap-1 mb-1 max-w-37">
        <div
          v-for="(visualization, i) in visualizations"
          :key="i"
          v-show="list[i]"
          class="cursor-pointer p-0.5  text-sm items-center flex justify-center min-w-6"
          @click="currentTrackSetting = visualization[0]"
          :title="visualization[2]"
          :class="[
            currentTrackSetting === visualization[0]
              ? ' bg-gray-100 shadow-inner shadow-dark-200 '
              : 'bg-transparent hover:opacity-70 boxTight',
            { 'rounded-b-none rounded-l-md ': i === 0 },
             { 'rounded-b-none rounded-r-md ': i === list.length-1 }
          ]"
        >
        <template v-if="visualization[1].includes(':')">
            <Icon :icon="visualization[1]" width="22"/>
        </template>
        <template v-else>
            {{ visualization[1] }}
        </template>
      
        </div>
      </div>

      <KeepAlive>
        <component :is="currentTrackSetting" :track="track" :selectedVis="selectedVis"/>
      </KeepAlive>

    </div>
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 4px;
  height: 10px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
<style>
.box {
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
}
.boxTight {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
}
</style>
