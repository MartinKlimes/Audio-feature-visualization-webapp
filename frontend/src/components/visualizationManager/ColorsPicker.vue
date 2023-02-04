<script setup>
import { ref } from 'vue';
import { api } from '../../../custom';
import { wavesurfer } from '../../functions/waveform';

const props = defineProps({
    track: Object,
})

const colors = ['bg-red-400', 'bg-yellow-300', 'bg-lime-500', 'bg-emerald-300', 'bg-cyan-300', 'bg-blue-300', 'bg-violet-300', 'bg-fuchsia-300', 'bg-rose-300','bg-warm-gray-300', 'bg-gray-400', 'bg-white'
        ]




const updateColor = (color) => {

    props.track.backgroundColor = color
    api.get("/change-track-status/backgroundColor/" + props.track.trackName + "/" + color)
    
    // wavesurfer[props.track.id].setBackgroundColor('red')
}
</script>

<template>

<div class="h-27 rounded-md w-full z-10 border border-gray-300 p-1 bg-white absolute top-20 grid grid-cols-4 gap-1 overflow-y-auto">


<div v-for="(color, i) in colors" :key="i">
    <div class="rounded-md w-full border h-full text-xs cursor-pointer shadow-sm shadow-dark-50" :class="[`${color}`, {'shadow-inner shadow-dark-500' : track.backgroundColor == color } ]" @click="updateColor(color)"></div>
</div>


</div>



</template>