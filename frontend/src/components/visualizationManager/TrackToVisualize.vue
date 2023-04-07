<script setup>
import { Icon } from "@iconify/vue";
import { ref, onMounted, reactive, computed } from "vue";
import { api } from "../../../custom";
import { trackIndex, trackList, alertState } from "../../stores/globalStores";
import VisButtons from "./VisButtons.vue";
import SelectFiles from "../buttons/SelectFiles.vue";
import { wavesurfer } from "../../functions/waveform";
import ColorsPicker from "./ColorsPicker.vue";
import { storeToRefs } from "pinia";
import { updateRecording } from "../../../custom";

const globalTrackIndex = trackIndex();
const alertGlobalState = alertState();
const { selTrackIndex, selTracksToPlay } = storeToRefs(globalTrackIndex);
const currentTrackList = trackList();
const showColors = ref(false);
const isBarsUploaded = ref(false);
const isMIDIUploaded = ref(false);

onMounted(() => {
  globalTrackIndex.changeIndex(props.track.id);
});

const props = defineProps({
  track: Object,
  isSelected: Boolean,
});
const smallLetters = computed(() => {
  return props.track.trackName.length > 20;
});

const selectBars = (event) => {
  updateRecording(props.track.id, "txtFileName", event);
  currentTrackList.selectTrack(props.track.id).txtFileName = event;
};
const selectMIDI = (event) => {
  updateRecording(props.track.id, "MIDIFileName", event);
  currentTrackList.selectTrack(props.track.id).MIDIFileName = event;
};

const updateBackgroundColor = (color) => {
  currentTrackList.selectTrack(props.track.id).backgroundColor = color;
  updateRecording(props.track.id, "backgroundColor", color);
};
</script>

<template>
  <div
    :id="`trackToVisualize-${track.id}`"
    class="relative h-57 w-full px-1 py-1 flex-col justify-center rounded-md border border-gray-300"
    :class="[
      { 'shadow-md shadow-gray-500  ': isSelected },
      currentTrackList.selectTrack(props.track.id).backgroundColor,
    ]"
  >
    <div class="flex justify-center items-center relative">
      <button
        class="absolute left-0 bg-white px-1 rounded-md hover:opacity-100"
        :class="{ 'shadow-inner shadow-dark-100': showColors }"
        @click="showColors = !showColors"
      >
        <Icon icon="ic:outline-color-lens" :inline="true" />
      </button>
      <Transition>
        <ColorsPicker
          class="h-27 top-20"
          v-if="showColors"
          :selected-color="currentTrackList.selectTrack(props.track.id).backgroundColor"
          @close-color-picker="showColors = false"
          @update-color="updateBackgroundColor($event)"
        />
      </Transition>

      <span
        class="font-bold font-serif text-gray-500 text-sm max-w-30 text-center h-8 overflow-hidden"
        :class="{ 'text-xs': smallLetters }"
        >{{ track.trackName }}</span
      >
      <div
        class="w-4 h-4 bg-white border border-gray-400 hover:bg-gray-400 duration-200 rounded-sm absolute right-0 cursor-pointer"
        :class="{ 'shadow-inner bg-gray-500 shadow-dark-400 duration-0': selTracksToPlay.includes(track.id) }"
        title="Select"
        @click="
          !selTracksToPlay.includes(track.id)
            ? selTracksToPlay.push(track.id)
            : selTracksToPlay.splice(selTracksToPlay.indexOf(track.id), 1)
        "
      ></div>
    </div>
    <div
      class="mt-1 player-buttons h-7 w-full bg-white border border-gray-300 flex items-center justify-between px-2 rounded-md"
    >
      <Icon icon="material-symbols:volume-up-outline" width="20" />
      <input type="range" class="slider appearance-none rounded-lg cursor-pointer w-28" />
      <div class="inline-flex rounded-md shadow-sm bg-gray-600 text-white">
        <button
          class="w-5 text-sm border-r border-gray-400 rounded-l-md hover:bg-gray-300 hover:text-gray-800 duration-200"
        >
          M
        </button>
        <button class="w-5 text-sm rounded-r-md hover:bg-gray-300 hover:text-gray-800 duration-200">S</button>
      </div>
    </div>

    <VisButtons :track="track" />

    <Icon
      icon="mdi:midi-port"
      width="18"
      class="w-8 float-right mt-2 shadow-sm shadow-gray-500 rounded-md bg-white hover:bg-gray-300 cursor-pointer"
      :class="{ 'shadow-inner': isMIDIUploaded, blink: alertGlobalState.message.includes('MIDI') && isSelected }"
      @click="(isMIDIUploaded = !isMIDIUploaded), (isBarsUploaded = false)"
    />

    <Icon
      icon="clarity:bars-line"
      :rotate="1"
      width="18"
      class="w-8 mr-1 float-right mt-2 shadow-sm shadow-gray-500 rounded-md bg-white hover:bg-gray-300 cursor-pointer"
      :class="{ 'shadow-inner': isBarsUploaded, blink: alertGlobalState.message.includes('text') && isSelected }"
      @click="(isBarsUploaded = !isBarsUploaded), (isMIDIUploaded = false)"
    />

    <Transition>
      <SelectFiles
        v-if="isBarsUploaded"
        class="right-1 bottom-8 absolute w-[97%] h-[47%]"
        :id="track.id"
        :files="currentTrackList.barsList"
        :selected-file="currentTrackList.selectTrack(track.id).txtFileName"
        @select-file="selectBars($event)"
      @close-modal="isBarsUploaded = false"

      />
    </Transition>
    <Transition>
      <SelectFiles
        v-if="isMIDIUploaded"
        class="right-1 bottom-8 absolute w-[97%] h-[47%]"
        :id="track.id"
        :files="currentTrackList.midiList"
        :selected-file="currentTrackList.selectTrack(track.id).MIDIFileName"
        @select-file="selectMIDI($event)"
      @close-modal="isMIDIUploaded = false"

      />
    </Transition>
  </div>
</template>

<style >
input[type="range"] {
  -webkit-appearance: none;
  cursor: pointer;


}

input[type="range"]::-webkit-slider-runnable-track {
  width: 300px;
  height: 5px;
  background: #c0bebe;
  border: none;
  border-radius: 3px;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  border: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: rgb(63, 63, 63);
  margin-top: -5px;
}

input[type="range"]:focus {
  outline: none;
}

input[type="range"]:focus::-webkit-slider-runnable-track {
  background: #747474;
}

@keyframes blink {
  0% {
    background-color: red;
  }
  50% {
    background-color: #1d4ed8
  }
  51% {
    background-color: red;
  }
  100% {
    background-color: #1d4ed8
  }
}

.blink {
  animation: blink 1.65s infinite;
}
</style>
