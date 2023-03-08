<script setup>
import 'html-midi-player'
import {ref, onMounted } from 'vue';
import { wavesurfer } from '../functions/waveform';
import Cursor from '../components/Cursor.vue'
import { api } from '../../custom';
import {createVerticalKeyboard} from '../functions/useMidiPianoroll'
// import '@magenta/music/node/music_vae'

// console.log(core);
const pianoroll = ref(null)
const pianorollSrc = ref(null)

const props = defineProps({
    track: Object
})

// api.get('/get-file/' + props.track.MIDIFileName)
// .then((response) => {
//     const url = window.URL.createObjectURL(new Blob([response.data]));
//     pianorollSrc.value = url
// })
   
onMounted(() => {
    
    // pianoroll.value.getElementsByTagName('div')[2].addEventListener('scroll', (e) => {
    //     if(wavesurfer[props.track.id]){
    //         wavesurfer[props.track.id].drawer.wrapper.scrollLeft = e.target.scrollLeft
    //     }
    // });
   
    // pianoroll.value.getElementsByTagName('div')[2].addEventListener('mousemove', (e) => {
    //     const wave = wavesurfer[props.track.id].drawer.wrapper
    //     const x = wave.scrollLeft + e.clientX - pianoroll.value.getBoundingClientRect().left
    //     const waveformCursor =document.getElementById(`waveform-cursor-${props.track.id}`)
    //     if(waveformCursor){
    //         waveformCursor.style.left = `${x }px`
    //     }
    //     const spectrogramCursor = document.getElementById(`spectrogram-cursor-${props.track.id}`)
    //     if(spectrogramCursor){
    //         spectrogramCursor.style.left = `${x - wavesurfer[props.track.id].drawer.wrapper.scrollLeft }px`
    //     }
    //     document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left = `${x - wavesurfer[props.track.id].drawer.wrapper.scrollLeft}px`

    // });

  
    setTimeout(() => {
        createVerticalKeyboard(props.track.id)
        
        // setInterval(() => {
        //     for (var i = 0; i < notes.length; i++) {
        //         var element = notes[i];
              
        //         var startTime = element.x.baseVal.value
        //         var endTime = element.x.baseVal.value + element.width.baseVal.value
        //         if (wavesurfer[props.track.id].drawer.lastPos >= startTime && wavesurfer[props.track.id].drawer.lastPos < endTime) {
        //             element.setAttributeNS(null, 'stroke', 'red');
        //             element.setAttributeNS(null, 'stroke-width', '2');

        //         } else {
        //             element.removeAttributeNS(null, 'stroke');
        //         }
        //     }   
        // }, 500)

    }, 2000);
})
const setInstrumentColor = (notes, instruments, numberOfInstrument, color) => {
    notes.forEach((element, id) => {
        if(instruments[id] == numberOfInstrument){
            element.setAttributeNS(null, 'fill', color)
        }
    });
}


  //po kliknutí na spektrogram a umístí kurzor na danou pozici a provede seek na odpovídající pozici ve zvukovém souboru.
  const positionCursor = ($e) => {
  const waveWidth = wavesurfer[props.track.id].drawer.width
  wavesurfer[props.track.id].seekTo((parseInt(document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left, 10) + wavesurfer[props.track.id].drawer.wrapper.scrollLeft) / waveWidth)
}



</script>





<template>
    nbbhb
<div class="relative">

    <midi-player :id="`pianoroll-player-${track.id}`" src="chopin_02.mid" class="hidden" >UpUpAndAway</midi-player>
    <midi-visualizer type="piano-roll" src="chopin_02.mid" :id="`pianoroll-${track.id}`"  ref="pianoroll" @click="positionCursor">
        <Cursor :id="`pianoroll-cursor-${track.id}`" :color="'gray-500'" :width="3" style="pointer-events: none;"/>
        <Cursor :id="`pianoroll-liveCursor-${track.id}`" :color="'dark-800'"/>
        
    </midi-visualizer>
    <div :id="`keyboard-${track.id}`" class="absolute top-0"></div>
    <div :id="`timeline-${track.id}`"></div>
</div>
</template>

<style>

.piano-roll-visualizer {
   
}

.highlighted {
  fill: red;
}
</style>