<script setup>
import BlueButtons from "../../buttons/BlueButtons.vue";
import IOI from "./IOI.vue";
import { Icon } from "@iconify/vue";
import { ref } from "vue";

const props = defineProps({
  trackName: String,
  id: Number,
  txtFileName: String,
  backgroundColor: String,
});
const showOnsets = ref(false);
const showBeats = ref(false);
const showBars = ref(false);
const onsetLoading = ref(false);
const beatsLoading = ref(false);
const showSetting = ref(false);
const showFileInfo = ref(false);
const dataType = ref("");


const toggleEye = (e) => {
  console.log(e);
  if (e[1] == 'bars') {
    showBars.value = e[0]
  } else if(e[1] == 'beats'){
    showBeats.value = e[0]
  } else {
    showOnsets.value = e[0]
  }
}


</script>

<template>
  <div class="w-full h-max bg-white border border-dark-300 rounded-md p-1 flex flex-col items-center mt-2">
    <div class="flex flex-col border border-dashed border-gray-400 rounded-md p-1 justify-center items-center">
      <BlueButtons
        @click="dataType == 'bars' ? (showSetting = !showSetting) : (showSetting = true), (dataType = 'bars')"
        :is-btn-clicked="showSetting && dataType == 'bars'"
        :icon="showBars ? 'mdi:eye-outline' : 'mdi:eye-off-outline'"
        @mouseover="showFileInfo = true"
        @mouseleave="showFileInfo = false"
        class="w-17"
        :class="{
          'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-transparent': !txtFileName,
        }"
        >Bars</BlueButtons
      >

      <Transition>
        <div
          v-if="showFileInfo && txtFileName"
          class="absolute bg-blue-300 z-1 rounded-md text-xs px-1 py-0.5 shadow-inner shadow-gray-500 mt-9"
        >
          {{ txtFileName }}
        </div>
      </Transition>

      <!-- <ClickSoundBtn v-if="isBtnClicked" :id="id" :backgroundColor="backgroundColor" :markers-list="bars"/> -->

      <BlueButtons
        title="IOI"
        class="mt-1 w-17"
        :is-btn-clicked="dataType == 'onset' && showSetting"
        :icon="onsetLoading ? 'fa:spinner' : showOnsets ? 'mdi:eye-outline' : 'mdi:eye-off-outline'"
        :icon-class="onsetLoading ? 'spin' : ''"
        @click="dataType == 'onset' ? (showSetting = !showSetting) : (showSetting = true), (dataType = 'onset')"
        >Onset</BlueButtons
      >

      <BlueButtons
        title="IOI"
        class="mt-1 w-17"
        :is-btn-clicked="dataType == 'beats' && showSetting"
        :icon="beatsLoading ? 'fa:spinner' : showBeats ? 'mdi:eye-outline' : 'mdi:eye-off-outline'"
        :icon-class="beatsLoading ? 'spin' : ''"
        @click="dataType == 'beats' ? (showSetting = !showSetting) : (showSetting = true), (dataType = 'beats')"
        >Beats</BlueButtons
      >
    </div>
    <!-- <Transition>
        <IOI v-if="showOnsets" 
        :track-name="trackName" 
        :id="id"
        :dataType="'onset'"
        @toggle-loading="onsetLoading = !onsetLoading"
        />
    </Transition> -->

    <!-- <Transition>
        <IOI v-if="showBeats" 
        :track-name="trackName" 
        :id="id"
        :dataType="'beats'"
        @toggle-loading="beatsLoading = !beatsLoading"
        />
    </Transition> -->
      <Transition>

        <IOI v-if="showSetting" 
        :track-name="trackName" 
        :id="id" 
        :dataType="dataType" 
        :txtFileName="txtFileName"
        @toggle-eye="toggleEye($event)"
         />

      </Transition>
    
  </div>
</template>
