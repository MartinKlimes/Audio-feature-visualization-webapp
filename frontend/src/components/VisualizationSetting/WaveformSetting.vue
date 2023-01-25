<script setup>
import { Icon } from '@iconify/vue';
import { ref, shallowRef } from 'vue';
import BarSelection from '../MainPanel/BarSelection.vue';
import TimeSelection from '../MainPanel/TimeSelection.vue';
import { wavesurfer } from '../../functions/waveform';
import { api } from '../../../custom';
const showTimeSelection = ref(false)
const showBarSeletion = ref(false)

const currentSetting = shallowRef()

const props = defineProps({
    track: Object,
})

const removeWaveform = () => {
    wavesurfer[props.track.id].destroy()
    props.track.isWaveform = false
    props.track.isWaveformDisplayed = false
    api.get("/change-track-status/isWaveform/" + props.track.trackName)
    api.get("/change-track-status/isWaveformDisplayed/" + props.track.trackName)
}

</script>




<template>
<div class=" flex flex-col items-center relative">
  
   
    <div class="flex mt-2">
        <button class="p-1 buttons btn-hover-cursor font-semibold w-max  shadow-sm shadow-dark-100 flex">Bars <Icon icon="mdi:eye-off-outline" class="mt-1 ml-1"/></button>
        <span class="text-xs opacity-50 ml-3">Name of file</span>
    </div>
    <span class="text-xs opacity-50 mt-3">Select part</span>
    <div class="flex  border border-dashed border-gray-400 rounded-md p-1 justify-center items-center" >
        <button class=" p-1 btn-hover-cursor font-semibold w-max shadow-sm shadow-dark-100 flex" @click="currentSetting === BarSelection ? currentSetting = '' : currentSetting = BarSelection">Bars<Icon icon="material-symbols:content-cut-rounded" class="mt-1 ml-1" /></button>
        <button class="p-1 btn-hover-cursor font-semibold w-max shadow-sm shadow-dark-100 flex ml-3" @click="currentSetting === TimeSelection ? currentSetting = '' : currentSetting = TimeSelection">Time<Icon icon="material-symbols:content-cut-rounded" class="mt-1 ml-1" /></button>
        
    </div>
    <transition>
        <KeepAlive>
            <component :is="currentSetting" :trackName="track.trackName" :id="track.id"/>
        </KeepAlive>
    </transition>
    <!-- <TimeSelection v-if="showTimeSelection" :trackName="trackName" :id="id"/> -->
    <!-- <transition>
        <BarSelection v-if="showBarSeletion"/>
    </transition> -->
    


    <button class="p-1 btn-hover-cursor font-semibold w-max shadow-sm shadow-dark-100 flex mt-3">Color<Icon icon="ic:outline-color-lens" class="mt-1 ml-1"/></button>

    <button title="reload waveform" class="absolute right-0 bottom-0 opacity-50 hover:opacity-100" @click="removeWaveform"> <Icon icon="mingcute:delete-2-line" /> </button>
   


<label for="added-textFile" class="hover:cursor-pointer" >
<div id="add-files-btn" class="btn-hover">Upload bars</div>
</label>
<input id="added-textFile" type="file" class="hidden" accept=".txt" multiple 
@change="addTxtFilesToUpload(globalTrackIndex.selTrackIndex, trackFromStart[globalTrackIndex.selTrackIndex][0]); hideBars = !hideBars">




   
</div>



</template>

<style scoped>

.v-enter-active,
.v-leave-active {
    transition: all 0.2s;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: scale(0.5);
}


</style>