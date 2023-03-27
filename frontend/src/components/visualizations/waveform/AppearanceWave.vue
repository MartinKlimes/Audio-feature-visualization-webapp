<script setup>
import ColorWaveform from "./ColorWaveform.vue";
import BlueButtons from "../../buttons/BlueButtons.vue";
import SetSize from "../../buttons/SetSize.vue"
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { wavesurfer } from "../../../functions/waveform";
import { trackList } from "../../../globalStores";
import { updateRecording } from "../../../../custom";

const showColorPicker = ref(false);
const sizeSet = ref(false);
const target = ref(null);
const currentTrackList = trackList()

const emits = defineEmits(['closeModal'])


const props = defineProps({
  trackName: String,
  id: Number,
  waveformColor: String,
  waveformHeight: Number
});

onClickOutside(target, () => {
  setTimeout(() => {
    emits("closeModal");
  }, 0);
});

const changeSize = (e) => {
    wavesurfer[props.id].setHeight(e)
    updateRecording(props.id,'waveformHeight', e)
    currentTrackList.selectTrack(props.id).waveform.waveformHeight = e

}
</script>

<template>
  <div class="flex flex-col bg-white box rounded-md p-2 mt-1 w-full items-center" ref="target">
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
        @click="sizeSet = !sizeSet" 
        :is-btn-clicked="sizeSet" 
        :icon-class="'ml-0'"

        >
        </BlueButtons>
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
       
      <SetSize
        v-if="sizeSet"
        :default-size="waveformHeight"
        @change-size="changeSize($event)"
      />
    </Transition>
  </div>
</template>
