<script setup>
import { Icon } from '@iconify/vue';
import { ref, shallowRef } from 'vue';
import BarSelection from '../MainPanel/BarSelection.vue';
import TimeSelection from '../MainPanel/TimeSelection.vue';
import { wavesurfer } from '../../functions/waveform';
import { api } from '../../../custom';
import { trackIndex, trackList } from '../../globalStores';
import { marker } from '../../functions/waveform';

const showTimeSelection = ref(false)
const showBarSeletion = ref(false)
const showFileInfo = ref(false)
const globalTrackIndex = trackIndex()
const currentSetting = shallowRef()
const currentTrackList = trackList()

const props = defineProps({
    track: Object,
})

const removeWaveform = () => {
    wavesurfer[props.track.id].destroy()
    props.track.isWaveform = false
    props.track.isWaveformDisplayed = false
    api.get("/change-track-status/isWaveform/" + props.track.trackName + "/''")
    api.get("/change-track-status/isWaveformDisplayed/" + props.track.trackName + "/''")
}
const showBars = () => {

  api.get('/get-file/' + currentTrackList.selectTrack(props.track.id).txtFileName)
    .then((response) => {
      let bars = response.data.split('\n');
      marker(response.data.split('\n'), globalTrackIndex.selTrackIndex);
    }
  )
}
const fn = (params) => {
    console.log(wavesurfer[props.track.id].markers.markers[0].color)
    wavesurfer[props.track.id].markers.markers[0].color = 'red'
    console.log(wavesurfer[props.track.id].markers)
}
</script>




<template>
<button @click="fn">dfs</button>
<div class=" flex flex-col items-center relative">
  
   
    <div class="flex flex-col items-center " >

        <button 
        class="p-1 buttons btn font-semibold w-max   flex" 
        :class="{'bg-yellow-100 shadow-sm shadow-dark-100 hover:bg-yellow-200' : currentTrackList.selectTrack(track.id).txtFileName}" @mouseover="showFileInfo=true" 
        @mouseleave="showFileInfo=false" 
        @click="showBars">
        Bars <Icon icon="mdi:eye-off-outline" class="mt-1 ml-1" />
        </button>
    </div>
    <Transition>
    <div v-if="showFileInfo && currentTrackList.selectTrack(track.id).txtFileName" class="absolute bg-yellow-200 z-1 rounded-md  text-xs px-1 py-0.5 shadow-inner shadow-gray-500 mt-9 ">{{currentTrackList.selectTrack(track.id).txtFileName}}</div>
    </Transition>
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