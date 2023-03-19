<script setup>
import BlueButtons from '../../buttons/BlueButtons.vue';
import { Icon } from '@iconify/vue';
import { ref } from 'vue'

const props = defineProps({
    trackName: String,
    id: Number,
    txtFileName: String,
    backgroundColor: String
})
const showOnsets = ref(false)
const showBeats = ref(false)
const onsetLoading = ref(false)
const beatsLoading = ref(false)
const showSetting = ref(false)
const componentProps = ref({})
</script>





<template>
<div class="w-max h-20 bg-white border border-dark-300">
    
    <BlueButtons @click="showSetting =! showSetting, componentProps = {dataType : 'bars'}" :is-btn-clicked="isBtnClicked" :icon="(isBtnClicked ? 'mdi:eye-outline' : 'mdi:eye-off-outline')" @mouseover="track.showFileInfo=true" @mouseleave="track.showFileInfo=false"  :class="{'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-transparent'  : !txtFileName}">Bars</BlueButtons>


    <Transition>
        <div v-if="showFileInfo && txtFileName" class="absolute bg-blue-300 z-1 rounded-md  text-xs px-1 py-0.5 shadow-inner shadow-gray-500 mt-9 ">{{txtFileName}}</div>
    </Transition>

    <ClickSoundBtn v-if="isBtnClicked" :id="id" :backgroundColor="backgroundColor" :markers-list="bars"/>
    <div class="flex mb-4">
          <BlueButtons title="IOI" class="mt-3" 
          :is-btn-clicked="showOnsets"  
          :icon="(onsetLoading ? 'fa:spinner' : (showOnsets ? 'mdi:eye-outline' : 'mdi:eye-off-outline'))"  
          :icon-class="(onsetLoading ? 'spin' : '')" 
          @click="showOnsets = ! showOnsets, showBeats = false" 
          >Onset</BlueButtons>
      
          <BlueButtons title="IOI" class="mt-3" 
          :is-btn-clicked="showBeats"  
          :icon="(beatsLoading ? 'fa:spinner' : (showBeats ? 'mdi:eye-outline' : 'mdi:eye-off-outline'))"  
          :icon-class="(beatsLoading ? 'spin' : '')" 
          @click="showBeats = ! showBeats, showOnsets =false" 
          >Beats</BlueButtons>

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
        :dataType="'beats'"
 
        />
    </Transition>


</div>
</template>