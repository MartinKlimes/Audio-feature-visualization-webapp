<script setup>
import 'html-midi-player'
import { onMounted } from 'vue';
import { wavesurfer } from '../functions/waveform';

// import '@magenta/music/node/music_vae'

// console.log(core);

const props = defineProps({
    track: Object
})

onMounted(() => {
    const visualizer = document.getElementById('myVisualizer')
    // const player = document.getElementById('myPlayer')
    // player.addVisualizer(document.getElementById('myVisualizer'));
    visualizer.config = {pixelsPerTimeStep: 20.8971}
    // console.log(visualizer.note);
  
    setTimeout(() => {
        const notes = document.querySelectorAll('.note')
        // notes.setAttributeNS(null, 'fill', '#f06')
        
        notes.forEach((note) => {
            // note.setAttributeNS(null, 'fill', '#f06')
            // console.log(note.getAttributeNS(null, 'x',));

        })
    }, 500);
    

    
 
})


</script>





<template>

    <!-- <midi-player id="myPlayer" src="chopin_02.mid" ></midi-player> -->
    <midi-visualizer  src="chopin_02.mid" type="piano-roll" id="myVisualizer" class="relative">
        <div id="cursor-piano-roll" 
        class="h-full w-1 bg-black absolute bottom-5"

        >
    </div></midi-visualizer>
</template>

<style>
svg rect.note.active {
  stroke: black;
  stroke-width: 5;
  stroke-opacity: 0.5;
}

.piano-roll-visualizer {
   
}
</style>