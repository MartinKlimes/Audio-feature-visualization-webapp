<script setup>
import { Icon } from '@iconify/vue';
import PlayBtn from '../buttons/PlayBtn.vue';
import { trackIndex } from '../../stores/globalStores';
import { wavesurfer } from '../../functions/waveform';
import { storeToRefs } from 'pinia';
import { ref, watchEffect } from 'vue';
import VueSlider from 'vue-slider-component';

const globalTrackIndex = trackIndex()
const {selTrackIndex, selTracksToPlay} = storeToRefs(globalTrackIndex) 
const isPlaying = ref([])
const currentTime = ref(0)
const duration = ref(null)
const playbackRate = ref(null)


const getCurrentTime = (id) => {
    countTime()
    const xpos = `${wavesurfer[id].drawer.lastPos - wavesurfer[id].drawer.wrapper.scrollLeft}px`
    const liveCursorSpec = document.getElementById(`spectrogram-liveCursor-${id}`)
    const liveCursorpiano = document.getElementById(`pianoroll-liveCursor-${id}`)

    if (liveCursorSpec) {
        liveCursorSpec.style.left = xpos
    }
    if (liveCursorpiano) {
        liveCursorpiano.style.left = xpos
    }
    
}



const play = (id) => {
    // const pianoroll = document.getElementById(`pianoroll-${id}`)
    // var svg = pianoroll.getElementsByTagName('div')[2].getElementsByTagName('svg')[0];
    // const notes = Array.from(svg.querySelectorAll('.note'));
    // var element = notes[1];
    // var startTime = element.x.baseVal.value
    // var endTime = element.x.baseVal.value + element.width.baseVal.value
    // console.log(startTime,endTime );
    
    // for (var i = 0; i < notes.length; i++) {
    //     // console.log(notes[i].width.baseVal.value);
    //     var element = notes[i];
    //     var startTime = element.x.baseVal.value
    //     var endTime = element.x.baseVal.value + element.width.baseVal.value
    //     // if (wavesurfer[id].drawer.lastPos >= startTime && wavesurfer[id].drawer.lastPos < endTime) {
    //     //     element.classList.add('highlighted');
    //     // } else {
    //     //     element.classList.remove('highlighted');
    //     // }
    // }

    const cursorSpec = document.getElementById(`spectrogram-cursor-${id}`)
    const cursorpiano = document.getElementById(`pianoroll-cursor-${id}`)

    if(cursorSpec){
        cursorSpec.style.visibility = 'hidden'
    }
    if(cursorpiano){
        cursorpiano.style.visibility = 'hidden'
    }


    wavesurfer[id].play()
    isPlaying.value.push(id)
    
    wavesurfer[id].on('audioprocess', getCurrentTime.bind(this, id));
    
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
        
        wavesurfer[id].on('finish', function() {
            isPlaying.value.splice(isPlaying.value.indexOf(id), 1)
        })
        
}
const pause = (id) => {
    const cursorSpec = document.getElementById(`spectrogram-cursor-${id}`)
    const cursorpiano = document.getElementById(`pianoroll-cursor-${id}`)

    if(cursorSpec){
        cursorSpec.style.visibility = ''
    }
    if(cursorpiano){
        cursorpiano.style.visibility = ''
    }

    wavesurfer[id].pause()
    isPlaying.value.splice(isPlaying.value.indexOf(id), 1)
    globalTrackIndex.selTracksToPlay.forEach((id) => {
        isPlaying.value.splice(isPlaying.value.indexOf(id), 1)
        wavesurfer[id].pause()})
}

const stop = (id) => {
    pause(id)
    wavesurfer[id].seekTo(0)
    globalTrackIndex.selTracksToPlay.forEach((id) => {
        wavesurfer[id].seekTo(0)
    })
}

const skipForward = (id) => {
    wavesurfer[id].skipForward(wavesurfer[id].getDuration()/100)
    globalTrackIndex.selTracksToPlay.forEach((id) => {wavesurfer[id].skipForward(wavesurfer[id].getDuration()/100)})
    
}
const skipBackward = () => {
    wavesurfer[id].skipBackward(wavesurfer[id].getDuration()/100)
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
watchEffect(() => {
    if(wavesurfer[selTrackIndex.value]){
    duration.value = Math.floor(wavesurfer[selTrackIndex.value].getDuration() / 60).toString().padStart(2, '0') + ':' + (wavesurfer[selTrackIndex.value].getDuration() % 60).toFixed(0).toString().padStart(2, '0') + ':' + (wavesurfer[selTrackIndex.value].getDuration() % 1).toFixed(2).substring(2)

    wavesurfer[selTrackIndex.value].on('interaction', () => {
        setTimeout(() => {
            countTime()
        });
        }, 0);
    }
})
const countTime = () => {
    return currentTime.value = Math.floor(wavesurfer[selTrackIndex.value].getCurrentTime() / 60).toString().padStart(2, '0') + ':' + (wavesurfer[selTrackIndex.value].getCurrentTime() % 60).toFixed(0).toString().padStart(2, '0') + ':' + (wavesurfer[selTrackIndex.value].getCurrentTime() % 1).toFixed(2).substring(2)
}



</script>





<template>

<!-- <div class="flex gap-2 ml-40 mt-0.5 rounded-2xl bg-gray-300 h-9 px-3 items-center justify-center">
    <vue-slider
      @change="changeSize($event)"
      v-model="playbackRate"
     
      :width="100"
      :height="20"
      :min="0.25"
      :max="3"
      :interval="0.25"
      :marks="true"
      :tooltipStyle="{ backgroundColor: 'Blue' , width: '10px', height: '10px'}"
      :processStyle="{ backgroundColor: 'Blue' , width: '10px', height: '10px'}"
      :dotStyle="{ backgroundColor: 'Blue', width: '10px', height: '10px' }"
      :railStyle="{ backgroundColor: '' }"
      :stepStyle="{ backgroundColor: 'RoyalBlue	' , width: '10px', height: '10px'}"
      :stepActiveStyle="{ backgroundColor: 'black' , width: '10px', height: '10px'}"
      :labelActiveStyle ="{ backgroundColor: 'CornflowerBlue' , width: '10px', height: '10px'}"
      :labelStyle="{ opacity: 0 , width: '10px', height: '10px'}"
    ></vue-slider>
</div> -->

<div class="flex gap-2 ml-40 mt-0.5 rounded-2xl bg-gray-300 h-9 px-3 ">

<PlayBtn :icon="'tabler:player-track-prev-filled'" @click="skipBackward(selTrackIndex)"/>
<PlayBtn :icon="'tabler:player-track-next-filled'" @click="skipForward(selTrackIndex)"/>
<PlayBtn v-if="!isPlaying.includes(selTrackIndex)" :icon="'tabler:player-play-filled'" @click="play(selTrackIndex)"/>
<PlayBtn v-if="isPlaying.includes(selTrackIndex)" :icon="'tabler:player-pause-filled'" @click="pause(selTrackIndex)"/>
<PlayBtn :icon="'tabler:player-stop-filled'" @click="stop(selTrackIndex)"/>

<!-- <PlayBtn :icon="'teenyicons:loop-outline'" @click="loop"/>
<PlayBtn :icon="'teenyicons:loop-outline'" @click="stopLoop"/> -->


</div>

<div class="bg-gray-300 rounded-l-2xl px-3 mt-0.5 h-9 flex ml-10 font-bold  items-center text-xl">
    {{ currentTime}}
  
</div>
<div v-if="wavesurfer[selTrackIndex]" class="bg-gray-300 rounded-r-2xl px-3 mt-0.5 h-9 flex ml-1 font-bold  items-center text-xl">
    <!-- {{ wavesurfer[selTrackIndex].getDuration() }}
    {{ wavesurfer[selTrackIndex].getDuration() % 60 }} -->
    {{ duration }}
  

</div>




</template>


<style scoped>
.highlighted {
    background-color: brown;
}


</style>