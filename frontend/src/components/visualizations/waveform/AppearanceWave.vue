<script setup>
import ColorWaveform from "./ColorWaveform.vue";
import BlueButtons from "../../buttons/BlueButtons.vue";
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { wavesurfer } from "../../../functions/waveform/waveform";
import { trackList } from "../../../stores/globalStores";
import { updateRecording } from "../../../composables/custom";
import SizeSetter from "../../tools/SizeSetter.vue";

const showColorPicker = ref(false);
const showSizeSetter = ref(false);
const target = ref(null);
const currentTrackList = trackList()

const emits = defineEmits(['closeModal'])


const props = defineProps({
  trackName: String,
  id: Number,
  waveformColor: String,
  waveformHeight: Number,
  splitChannels: Boolean
});

onClickOutside(target, () => {
  setTimeout(() => {
    emits("closeModal");
  }, 0);
});


const split= () => {
  if(!props.splitChannels){
    wavesurfer[props.id].params.splitChannels = true
    currentTrackList.selectTrack(props.id).waveform.splitChannels = true
    updateRecording(props.id, "splitChannels", true);
  } else{
    wavesurfer[props.id].params.splitChannels = false
    currentTrackList.selectTrack(props.id).waveform.splitChannels = false
    updateRecording(props.id, "splitChannels", false);
    wavesurfer[props.id].setHeight(props.waveformHeight)
  }
  wavesurfer[props.id].drawBuffer()

};

</script>

<template>
  <div class="flex flex-col bg-white box rounded-md p-2 mt-1 w-full  items-center" ref="target">
    <div class="flex gap-1">
        <BlueButtons
        :icon="'ic:outline-color-lens'"
        @click="showColorPicker = !showColorPicker"
        :is-btn-clicked="showColorPicker"
        :icon-class="'ml-0'"
        
        >
        </BlueButtons>

        <BlueButtons 
        :icon="'nimbus:size-height'" 
        @click="showSizeSetter = !showSizeSetter" 
        :is-btn-clicked="showSizeSetter" 
        :icon-class="'ml-0'"

        >
        </BlueButtons>

        <BlueButtons
        title="Split channels"
        :is-btn-clicked="splitChannels"
       
        @click="split()"
        :icon-class="'ml-0'"
        :rotate="1"
        :icon="'carbon:split-screen'"
        ></BlueButtons>

    </div>

    <Transition>
      <ColorWaveform
        v-if="showColorPicker"
        :id="id"
        :trackName="trackName"
        :waveformColor="waveformColor"
      />
    </Transition>


    <Transition>
        <SizeSetter
        v-if="showSizeSetter"
        :id="id"
        :visualization="'waveform'"
        :loading-visualization="'isWaveformLoading'"
        />
    </Transition>
  </div>
</template>
