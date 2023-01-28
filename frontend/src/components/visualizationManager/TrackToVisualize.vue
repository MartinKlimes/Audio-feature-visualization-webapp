<script setup>
import { Icon } from '@iconify/vue';
import { ref, onMounted } from 'vue';
import { api } from '../../../custom';
import { trackIndex, trackList } from '../../globalStores';
import VisButtons from './VisButtons.vue';
import SelectFiles from './SelectFiles.vue'

const globalTrackIndex = trackIndex()
const currentTrackList = trackList()

const isBarsUploaded = ref(false)
const isMIDIUploaded = ref(false)

onMounted(() => {;
    globalTrackIndex.selTrackIndex = props.track.id
})

const props = defineProps({
    track: Object
})

const selectBars = (event) => {
    api.get("/change-track-status/txtFileName/" + props.track.trackName + "/" + event)
    .then(() => {
        currentTrackList.selectTrack(props.track.id).txtFileName = event
    })
}
const selectMIDI = (event) => {
    api.get("/change-track-status/MIDIFileName/" + props.track.trackName + "/" + event)
    .then(() => {
        currentTrackList.selectTrack(props.track.id).MIDIFileName = event
    })
}
</script>



<template>

<div class="relative h-57 w-full px-1 py-1 flex-col justify-center bg-light-700 rounded-md border border-gray-300  hover:bg-gray-200" :class="{'shadow-md shadow-gray-500  ' : track.id==globalTrackIndex.selTrackIndex}">
    <div class="flex justify-center items-center relative ">
        <button class="absolute left-0 opacity-70 rounded-md hover:opacity-100">
            <Icon icon="ic:outline-color-lens" />
        </button>
        <span class="font-bold font-serif text-gray-500 text-sm max-w-30 text-center h-8 overflow-hidden" :class="{'text-xs': track.trackName.length >20}">{{track.trackName}}</span>
        <div class="w-4 h-4 bg-gray-100 border border-gray-400 hover:bg-gray-400 duration-200 rounded-sm absolute right-0 cursor-pointer" title="Select"></div>
    </div>
    <div class="mt-1 player-buttons h-7 w-full bg-gray-400 flex items-center justify-between px-2 rounded-md">
        <Icon icon="material-symbols:volume-up-outline" width="20" />
        <input type="range" class="slider appearance-none  rounded-lg cursor-pointer w-28">
        <div class="inline-flex rounded-md shadow-sm bg-gray-600 text-white " >
            <button class="w-5 text-sm border-r border-gray-400 rounded-l-md hover:bg-gray-300 hover:text-gray-800 duration-200 ">M</button>
            <button class="w-5 text-sm rounded-r-md hover:bg-gray-300 hover:text-gray-800 duration-200 ">S</button>

        </div>

    </div>
    
    <VisButtons :track="track" />
    
    <Icon icon="mdi:midi-port" width="18" class="w-8 float-right mt-2 shadow-sm shadow-gray-500 rounded-md hover:bg-gray-300 cursor-pointer" :class="{'shadow-inner' : isMIDIUploaded}"  @click="isMIDIUploaded =! isMIDIUploaded, isBarsUploaded = false"/>
    <Icon icon="clarity:bars-line" :rotate="1" width="18" class="w-8 mr-1 float-right mt-2 shadow-sm shadow-gray-500 rounded-md hover:bg-gray-300 cursor-pointer" :class="{'shadow-inner' : isBarsUploaded}" @click="isBarsUploaded = !isBarsUploaded, isMIDIUploaded = false"/>

    <Transition>
        <SelectFiles v-if="isBarsUploaded" :id="track.id" :files="currentTrackList.barsList" @select-file="selectBars($event)"/>
    </Transition>
    <Transition>
        <SelectFiles v-if="isMIDIUploaded" :id="track.id" :files="currentTrackList.midiList" @select-file="selectMIDI($event)"/>
    </Transition>

</div>


</template>

<style scoped>


input[type=range]{
    -webkit-appearance: none;
}

input[type=range]::-webkit-slider-runnable-track {
    width: 300px;
    height: 5px;
    background: #ddd;
    border: none;
    border-radius: 3px;
}

input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    border: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: rgb(63, 63, 63);
    margin-top: -4px;
}

input[type=range]:focus {
    outline: none;
}

input[type=range]:focus::-webkit-slider-runnable-track {
    background: #ccc;
}
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