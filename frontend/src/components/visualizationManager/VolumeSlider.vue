<script setup>
import { Icon } from '@iconify/vue';
import { ref, watch } from 'vue';
import { wavesurfer } from '../../functions/waveform/waveform';
import { trackIndex } from '../../stores/globalStores';

const props = defineProps({
    id: Number,
    isWaveformReady: Boolean
})

const globalTrackIndex  = trackIndex()
const isMuted = ref(false)
const isSolo = ref(false)
const volumeValue = ref(0.5)

const changeVolume = (e) => {
    wavesurfer[props.id].setVolume(e.target.value)
    volumeValue.value = e.target.value
    isMuted.value = false

}
const mute = () => {
    wavesurfer[props.id].toggleMute();
    isMuted.value = !isMuted.value
    isSolo.value = false
}
const solo = () => {
    globalTrackIndex.selTracksToPlay.forEach((id) => {
      wavesurfer[id].toggleMute();
     });

     if(wavesurfer[props.id].getMute()){
        wavesurfer[props.id].toggleMute();
     }
    isSolo.value = !isSolo.value
    isMuted.value = false
}
</script>



<template>
    
<div class="mt-1 player-buttons h-7 w-full bg-white border border-gray-300 flex items-center justify-between px-2 rounded-md">
      <Icon @click="mute()" class="cursor-pointer" :icon="volumeValue > 0.75 ? 'fluent-mdl2:volume-3' : volumeValue > 0.5 ?'fluent-mdl2:volume-2' : volumeValue > 0 ? 'fluent-mdl2:volume-1' : isMuted ? 'fluent-mdl2:volume-0' : 'fluent-mdl2:volume-0'" width="20" />
      <input type="range" v-model="volumeValue" min="0" max="1" step="0.01" @input="changeVolume($event)"  class="slider appearance-none rounded-lg cursor-pointer w-28" />
      <div class="inline-flex rounded-md shadow-sm bg-gray-600 text-white">
        <button @click="mute()" :class="{'shadow-inner shadow-dark-100 bg-yellow-200 text-black hover:bg-yellow-100' : isMuted}" class="w-5 text-sm border-r border-gray-400 rounded-l-md hover:bg-gray-300 hover:text-gray-800 duration-200">M</button>
        <button @click="solo()" :class="{'shadow-inner shadow-dark-100 bg-green-400 text-black hover:bg-green-300' : isSolo}" class="w-5 text-sm rounded-r-md hover:bg-gray-300 hover:text-gray-800 duration-200">S</button>
      </div>
    </div>


</template>