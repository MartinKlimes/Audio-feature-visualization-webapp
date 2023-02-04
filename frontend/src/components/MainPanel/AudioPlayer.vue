<script setup>
import { Icon } from '@iconify/vue';
import PlayBtn from '../buttons/PlayBtn.vue';
import { trackIndex } from '../../globalStores';
import { wavesurfer } from '../../functions/waveform';
import { storeToRefs } from 'pinia';
import { ref, computed } from 'vue';

const globalTrackIndex = trackIndex()
const {selTrackIndex, selTracksToPlay} = storeToRefs(globalTrackIndex) 
const isPlaying = ref([])

const isPlay = computed(() => {
    // if(wavesurfer[globalTrackIndex.selTrackIndex].isPlaying()){
    //     isPlaying.value = true

    // }


  
})





const play = () => {
    wavesurfer[globalTrackIndex.selTrackIndex].play()
    isPlaying.value.push(globalTrackIndex.selTrackIndex)
    globalTrackIndex.selTracksToPlay.forEach((id) => {
        isPlaying.value.push(id)
        wavesurfer[id].play()})
}
const pause = () => {
    wavesurfer[globalTrackIndex.selTrackIndex].pause()
    isPlaying.value.splice(isPlaying.value.indexOf(globalTrackIndex.selTrackIndex), 1)
    globalTrackIndex.selTracksToPlay.forEach((id) => {
        isPlaying.value.splice(isPlaying.value.indexOf(globalTrackIndex.selTrackIndex), 1)
        wavesurfer[id].pause()})
}

const stop = () => {
    pause()
    wavesurfer[globalTrackIndex.selTrackIndex].seekTo(0)
    globalTrackIndex.selTracksToPlay.forEach((id) => {
        wavesurfer[id].seekTo(0)
    })
}
const skipForward = (params) => {
    wavesurfer[globalTrackIndex.selTrackIndex].skipForward(5)
    globalTrackIndex.selTracksToPlay.forEach((id) => {wavesurfer[id].skipForward(5)})
}


</script>





<template>
<div class="flex gap-2 ml-40 mt-0.5 rounded-2xl bg-gray-200 h-9 px-3 ">

<PlayBtn :icon="'tabler:player-track-prev-filled'"/>
<PlayBtn :icon="'tabler:player-track-next-filled'" @click="skipForward"/>
<PlayBtn v-if="!isPlaying.includes(selTrackIndex)" :icon="'tabler:player-play-filled'" @click="play"/>
<PlayBtn v-if="isPlaying.includes(selTrackIndex)" :icon="'tabler:player-pause-filled'" @click="pause"/>
<PlayBtn :icon="'tabler:player-stop-filled'" @click="stop"/>
<PlayBtn :icon="'teenyicons:loop-outline'"/>


</div>





</template>