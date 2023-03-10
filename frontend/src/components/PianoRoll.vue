<script setup>
import 'html-midi-player'

import {ref, onMounted, watchEffect, watch } from 'vue';
import { wavesurfer } from '../functions/waveform';
import Cursor from '../components/Cursor.vue'
import { api } from '../../custom';
import {trackCursorPosition, createVerticalKeyboard, setInstrumentColor} from '../functions/useMidiPianoroll'
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js';


const pianoroll = ref(null)
const pianorollSrc = ref(null)

const props = defineProps({
    track: Object,
})

const setPianorollCurrentPosition = (params) => {
    trackCursorPosition(wavesurfer[props.track.id].drawer.lastPos, props.track.id, props.track.pianoroll.dynamicNames)
}




const loadMidiFile = async (fileName) => {
  const response = await api.get('/get-file/' + fileName, {responseType: 'blob'});
  const url = window.URL.createObjectURL(new Blob([response.data]));
  pianorollSrc.value = url
};
const scrollListener = () => {
    pianoroll.value.getElementsByTagName('div')[2].addEventListener('scroll', (e) => {
    if(wavesurfer[props.track.id]){
        wavesurfer[props.track.id].drawer.wrapper.scrollLeft = e.target.scrollLeft
        }
    });
}
const mousemoveListener = () => {
    pianoroll.value.getElementsByTagName('div')[2].addEventListener('mousemove', (e) => {
    const wave = wavesurfer[props.track.id].drawer.wrapper
    const x = wave.scrollLeft + e.clientX - pianoroll.value.getBoundingClientRect().left
    const waveformCursor =document.getElementById(`waveform-cursor-${props.track.id}`)
    if(waveformCursor){
        waveformCursor.style.left = `${x }px`
    }
    const spectrogramCursor = document.getElementById(`spectrogram-cursor-${props.track.id}`)
    if(spectrogramCursor){
        spectrogramCursor.style.left = `${x - wavesurfer[props.track.id].drawer.wrapper.scrollLeft }px`
    }
    document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left = `${x - wavesurfer[props.track.id].drawer.wrapper.scrollLeft}px`

});
}
watchEffect(() => {
    loadMidiFile(props.track.MIDIFileName)

})


watch(() => props.track.waveform.isWaveformReady,() => {
    scrollListener()
    mousemoveListener()
    const width = wavesurfer[props.track.id].drawer.width / wavesurfer[props.track.id].getDuration()
    const paddingRight = (wavesurfer[props.track.id].getDuration() - document.getElementById(`pianoroll-player-${props.track.id}`).duration) * width

    let colors
    if(props.track.pianoroll.pianorollColor){
        colors = props.track.pianoroll.pianorollColor.slice(1, -1).split(',').map(color => color.replace(/"/g, ''))
        
    }
    watchEffect(() =>{
        props.track.pianoroll.isPianorollLoading = createVerticalKeyboard(props.track.id,props.track.pianoroll.pianorollHeight, width, paddingRight, colors)               
    })
    watch(
        () => props.track.MIDIFileName,
        () =>  {
            setTimeout(() => {
            props.track.pianoroll.isPianorollLoading = createVerticalKeyboard(props.track.id,props.track.pianoroll.pianorollHeight, width, paddingRight, colors)               
        }, 1000);
    })

    wavesurfer[props.track.id].on('interaction', () => {
        if(props.track.pianoroll.isPianorollDisplayed){
            setTimeout(() =>trackCursorPosition(wavesurfer[props.track.id].drawer.lastPos, props.track.id, props.track.pianoroll.dynamicNames), 0);
        }   
    })

    let trackCursor
    wavesurfer[props.track.id].on('play', () => {
        if(props.track.pianoroll.isPianorollDisplayed){
            trackCursor = setInterval(setPianorollCurrentPosition, 100)
        }   
    })

    wavesurfer[props.track.id].on('pause', () => {  
        clearInterval(trackCursor)
    })

    wavesurfer[props.track.id].addPlugin(TimelinePlugin.create({
        container: `#timeline-pianoroll-${props.track.id}`,
    })).initPlugin('timeline')
})

  const positionCursor = ($e) => {
  const waveWidth = wavesurfer[props.track.id].drawer.width
  wavesurfer[props.track.id].seekTo((parseInt(document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left, 10) + wavesurfer[props.track.id].drawer.wrapper.scrollLeft) / waveWidth)
}

</script>





<template>

<div class="relative" >

    <midi-player :id="`pianoroll-player-${track.id}`" :src="pianorollSrc"  class="hidden" >UpUpAndAway</midi-player>
    <midi-visualizer  type="piano-roll" :src="pianorollSrc" :id="`pianoroll-${track.id}`"  ref="pianoroll" @click="positionCursor">
        <Cursor :id="`pianoroll-cursor-${track.id}`" :color="'gray-500'" :width="3" style="pointer-events: none;"/>
        <Cursor :id="`pianoroll-liveCursor-${track.id}`" :color="'dark-800'"/>
        
    </midi-visualizer>
    <div :id="`keyboard-${track.id}`" class="absolute top-0"></div>
    <div :id="`timeline-pianoroll-${track.id}`" :class="props.track.backgroundColor"></div>
</div>
</template>

<style>
.white-background {
  background-color: white;
}
.black-background {
  background-color: black;
}
.red-background {
  background-color: red;
}
.piano-roll-visualizer {
   
}

.highlighted {
  fill: red;
}
</style>