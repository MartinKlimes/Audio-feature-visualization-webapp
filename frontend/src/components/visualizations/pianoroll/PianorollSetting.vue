<script setup>
import { ref, onMounted } from "vue";
import BlueButttons from "../../buttons/BlueButtons.vue";
import PianorollStyle from "./pianorollStyle/PianorollStyle.vue";
import { Icon } from "@iconify/vue";
import { updateRecording } from "../../../../custom";
import ExportBtn from "../../buttons/ExportBtn.vue";
import { trackList } from "../../../globalStores";
import { ColorPicker } from "vue-accessible-color-picker";

const showPianorollStyle = ref(false);
const showColorPicker = ref(false)
const currentTrackList = trackList()
const props = defineProps({
  track: Object,
});

const removePianoroll = () => {
  props.track.pianoroll.isPianoroll = false;
  props.track.pianoroll.isPianorollDisplayed = false;
  updateRecording(props.track.id, "isPianoroll", false);
  updateRecording(props.track.id, "isPianorollDisplayed", false);
};

const dynamicNames = () => {
  currentTrackList.selectTrack(props.track.id).pianoroll.dynamicNames =!  currentTrackList.selectTrack(props.track.id).pianoroll.dynamicNames
}

const changeColor = (e) => {

  currentTrackList.selectTrack(props.track.id).pianoroll.ActiveNotesColor = e
}

onMounted(() => {
  currentTrackList.selectTrack(props.track.id).pianoroll.dynamicNames = false
})



</script>

<template>
  <div class="flex flex-col items-center relative h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 shadow-md">
    <ExportBtn :id="track.id" :track-name="track.trackName" :visualization="'pianoroll'" class="absolute top-0 right-0" />

    <BlueButttons
      class="mt-2 flex"
      @click="showPianorollStyle = !showPianorollStyle"
      :icon="'dashicons:admin-appearance'"
      :icon-class="'ml-0'"
      :is-btn-clicked="showPianorollStyle"
      title="pianoroll style"
    />

    <transition>
      <PianorollStyle v-if="showPianorollStyle" :track-name="track.trackName" :id="track.id" @close-modal="showPianorollStyle = false" />
    </transition>

    <div class="flex gap-1">
      <BlueButttons
        :is-btn-clicked="track.pianoroll.dynamicNames"
        @click="dynamicNames()"
        class="mt-2"
        :icon-class="'ml-0'"
        :icon="'game-icons:piano-keys'"
        title="dynamic keys"
      ></BlueButttons>
      <BlueButttons
        @click="showColorPicker =! showColorPicker"
        :is-btn-clicked="showColorPicker"
        class="mt-2"
        :icon-class="'ml-0'"
        :icon="'material-symbols:format-color-fill'"
        title="dynamic keys"
      ></BlueButttons>



    </div>
    <Transition>
      <div  v-if="showColorPicker">
        <ColorPicker  @color-change="changeColor($event.cssColor)" default-format="hex" class= " overflow-hidden max-h-60 rounded-md z-20 mt-2"  alpha-channel="hide"  />
        <div class="bg-white w-10 h-11 rounded-md absolute bottom-2 right-2 z-20"></div>
      </div>
    </Transition>

    <button v-if="!showColorPicker" title="Delete pianoroll" class="mt-4 opacity-50 absolute bottom-0 right-0 hover:opacity-100" @click="removePianoroll">
      <Icon icon="mingcute:delete-2-line" />
    </button>
    <!-- <button @click="changeInstColor">změn</button> -->
  </div>
</template>
