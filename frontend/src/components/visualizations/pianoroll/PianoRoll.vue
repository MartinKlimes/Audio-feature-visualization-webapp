<script setup>
import 'html-midi-player'
import {ref, onMounted, watchEffect, watch } from 'vue';
import { wavesurfer } from '../../../functions/waveform';
import Cursor from '../../tools/Cursor.vue'
import { api } from '../../../../custom';
import {trackCursorPosition, createVerticalKeyboard, setInstrumentColor, getsaturationValues} from '../../../functions/pianoroll/useMidiPianoroll'
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js';
import LoadingOverlay from '../../tools/LoadingOverlay.vue';


import { trackList } from '../../../stores/globalStores';
import { q } from 'plotly.js-dist';
import PianorollKeyboardSettings from './PianorollKeyboardSettings.vue';

const pianoroll = ref(null)
const pianorollSrc = ref(null)
const currentTrackList = trackList()

const props = defineProps({
    track: Object,
})

const setPianorollCurrentPosition = (params) => {
    trackCursorPosition(wavesurfer[props.track.id].drawer.lastPos + props.track.pianoroll.scrollLeft, props.track.id, props.track.pianoroll.dynamicNames, props.track.pianoroll.ActiveNotesColor)
}


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

watch(()=> props.track.MIDIFileName, () =>{
    props.track.pianoroll.isPianorollLoading = true

    api.get('/get-file/' + props.track.MIDIFileName, {responseType: 'blob'})
    .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        pianorollSrc.value = url       
           setTimeout(() => {
            editPianoroll()
           }, 2000)
    })
}, {immediate: true})

// setTimeout(() => {
//     const formData = new FormData();
//     formData.append('file_name', props.track.MIDIFileName);
//     formData.append('start_time', 5);
//     formData.append('end_time', 10);

//     api.post('/trim_midi', formData, {
//             headers: {
//                 "X-CSRF-TOKEN": getCookie("csrf_access_token"),
//                 'Content-Type': 'multipart/form-data'
                
//     }}).then((response) => {
//         console.log(response);
//     })
   
// }, 1000);
    // určení počátečního a koncového času


//     


const countWidthWaveform = () => {
    const width = wavesurfer[props.track.id].drawer.width / wavesurfer[props.track.id].getDuration()
    const paddingRight = (wavesurfer[props.track.id].getDuration() - document.getElementById(`pianoroll-player-${props.track.id}`).duration) * width
    return {width, paddingRight}
}

const editTrimmedPianoroll = () => {
    currentTrackList.selectTrack(props.track.id).pianoroll.scrollLeft =  props.track.start * countWidthWaveform().width
    pianoroll.value.getElementsByTagName('div')[2].style.overflow = "hidden";
    pianoroll.value.getElementsByTagName('div')[2].scrollLeft = props.track.start * countWidthWaveform().width
}

const editPianoroll = () => {
    watch(() => props.track.waveform.isWaveformReady, () => {
   
        if(props.track.waveform.isWaveformReady){   
        
        getsaturationValues(props.track.id) //save saturation for colors
    
        //if track is trimmed
        if(props.track.start){ 
            editTrimmedPianoroll()

        }else{
            currentTrackList.selectTrack(props.track.id).pianoroll.scrollLeft = 0
            scrollListener()
        }

        mousemoveListener()

        
        let colors
        if(props.track.pianoroll.pianorollColor){
            colors = props.track.pianoroll.pianorollColor.slice(1, -1).split(',').map(color => color.replace(/"/g, ''))
            
        }

        const {width, paddingRight} = countWidthWaveform()
        watchEffect(() =>{
            console.log(props.track.pianoroll.dynamicNames);
            props.track.pianoroll.isPianorollLoading = createVerticalKeyboard(props.track.id,props.track.pianoroll.pianorollHeight, width, paddingRight, colors, props.track.pianoroll.dynamicNames)               
        })
        watch(
            () => props.track.MIDIFileName,
            () =>  {
                setTimeout(() => {
                    if(props.track.start){ 
                        editTrimmedPianoroll()  
                    }
                props.track.pianoroll.isPianorollLoading = createVerticalKeyboard(props.track.id,props.track.pianoroll.pianorollHeight, width, paddingRight, colors)               
            }, 1000);
        })

        wavesurfer[props.track.id].on('interaction', () => {
            if(props.track.pianoroll.isPianorollDisplayed){
                setTimeout(() =>trackCursorPosition(wavesurfer[props.track.id].drawer.lastPos +  props.track.pianoroll.scrollLeft, props.track.id, props.track.pianoroll.dynamicNames, props.track.pianoroll.ActiveNotesColor), 0);
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

        wavesurfer[props.track.id].on('zoom', () => {
            const {width, paddingRight} = countWidthWaveform()
            if(props.track.start){ 
                editTrimmedPianoroll()  
            }
            createVerticalKeyboard(props.track.id,props.track.pianoroll.pianorollHeight, width, paddingRight, colors)  
        })
        }
    }, {immediate: true})
}


  const positionCursor = ($e) => {
  const waveWidth = wavesurfer[props.track.id].drawer.width
  wavesurfer[props.track.id].seekTo((parseInt(document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left, 10) + wavesurfer[props.track.id].drawer.wrapper.scrollLeft) / waveWidth)
}

</script>





<template>

<div class="relative" >
    <LoadingOverlay v-if="track.pianoroll.isPianorollLoading" />
    <PianorollKeyboardSettings :id="track.id"/>

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