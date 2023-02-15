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
const currentTime = ref(0)


const getCurrentTime = () => {
    currentTime.value = wavesurfer[globalTrackIndex.selTrackIndex].getCurrentTime()
    
}



const play = (index) => {
    const player = document.getElementById('myPlayer')
    player.start()
    player.volume = 0

    wavesurfer[index].play()
    isPlaying.value.push(index)
    
    wavesurfer[index].on('audioprocess', getCurrentTime);
    
    globalTrackIndex.selTracksToPlay.forEach((id) => {
        if(!isPlaying.value.includes(id)){
            console.log(wavesurfer);
            wavesurfer[id].play()
            isPlaying.value.push(id)
            // wavesurfer[id].on('finish', function() {
                //     isPlaying.value.splice(isPlaying.value.indexOf(id), 1)
                // })
            }
            
            
        })
        
        wavesurfer[index].on('finish', function() {
            isPlaying.value.splice(isPlaying.value.indexOf(index), 1)
        })
        
}
const pause = () => {
    const player = document.getElementById('myPlayer')

    player.stop()
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

const skipForward = () => {
    wavesurfer[globalTrackIndex.selTrackIndex].skipForward(wavesurfer[globalTrackIndex.selTrackIndex].getDuration()/100)
    globalTrackIndex.selTracksToPlay.forEach((id) => {wavesurfer[id].skipForward(wavesurfer[id].getDuration()/100)})
    
}
const skipBackward = () => {
    wavesurfer[globalTrackIndex.selTrackIndex].skipBackward(wavesurfer[globalTrackIndex.selTrackIndex].getDuration()/100)
    globalTrackIndex.selTracksToPlay.forEach((id) => {wavesurfer[id].skipBackward(wavesurfer[id].getDuration()/100)})
}

// const loop = () => {
//     wavesurfer[globalTrackIndex.selTrackIndex].on('finish', activeLoop)
//     globalTrackIndex.selTracksToPlay.forEach((id) => {
//         wavesurfer[id].on('finish', function() {
//             wavesurfer[id].seekTo(0)
//             wavesurfer[id].play()})
//     })
        
// }
// const stopLoop = () => {
//     wavesurfer[globalTrackIndex.selTrackIndex].un('finish', activeLoop)
// }

// const activeLoop = (params) => {
//     wavesurfer[globalTrackIndex.selTrackIndex].seekTo(0)
//     play()
// }
// const activeLoops = (params) => {
    
// }

</script>





<template>

<div class="flex gap-2 ml-40 mt-0.5 rounded-2xl bg-gray-300 h-9 px-3 ">

<PlayBtn :icon="'tabler:player-track-prev-filled'" @click="skipBackward"/>
<PlayBtn :icon="'tabler:player-track-next-filled'" @click="skipForward"/>
<PlayBtn v-if="!isPlaying.includes(selTrackIndex)" :icon="'tabler:player-play-filled'" @click="play(selTrackIndex)"/>
<PlayBtn v-if="isPlaying.includes(selTrackIndex)" :icon="'tabler:player-pause-filled'" @click="pause"/>
<PlayBtn :icon="'tabler:player-stop-filled'" @click="stop"/>

<!-- <PlayBtn :icon="'teenyicons:loop-outline'" @click="loop"/>
<PlayBtn :icon="'teenyicons:loop-outline'" @click="stopLoop"/> -->


</div>

<div class="bg-gray-300 rounded-l-2xl px-3 mt-0.5 h-9 flex ml-10 font-bold  items-center text-xl">
    {{(currentTime>60 ? (currentTime/60).toFixed(0) : '0') +  'm' }} 
    {{(currentTime>60 ? (currentTime % 60).toFixed(2) : (currentTime).toFixed(2)) + 's'}}
  

</div>
<div v-if="wavesurfer[selTrackIndex]" class="bg-gray-300 rounded-r-2xl px-3 mt-0.5 h-9 flex ml-1 font-bold  items-center text-xl">
    <!-- {{ wavesurfer[selTrackIndex].getDuration() }}
    {{ wavesurfer[selTrackIndex].getDuration() % 60 }} -->
    {{(wavesurfer[selTrackIndex].getDuration()>60 ? (wavesurfer[selTrackIndex].getDuration()/60).toFixed(0) : '0') +  'm' }} 
    {{(wavesurfer[selTrackIndex].getDuration()>60 ? (wavesurfer[selTrackIndex].getDuration() % 60).toFixed(2) : (wavesurfer[selTrackIndex].getDuration()).toFixed(2)) + 's'}}
  

</div>




</template>