<script setup>
import { Icon } from '@iconify/vue';
import { onMounted, reactive, ref } from 'vue';
import {showVolume,hideVolume, playAll, pauseAll, stopAll, muteAll, showIOIBtnIBIBtn} from '../../filesFunctions'
import { makeWaveform, wavesurfer, trackFromStart} from '../../Waveform';
import { trackList, trackIndex } from '../../globalStores';
import { api } from '../../../custom';
import {getCookie} from '../../cookieHandling'



import InterMeasureInterval from './InterMeasureInterval.vue';
import OnsetBeatsIntervals from './OnsetBeatsIntervals.vue';
import MIDI from './MIDI.vue';

const globalTrackIndex = trackIndex()

onMounted(() => {
    window.eventBus.on('select', event => selectTrack(event))   
    window.eventBus.on('stopBarSelection', event => hideBars.value = true)
})

const emits = defineEmits(['showWaveform'],['showSpectrogram'], ['showPianoroll'])

const isSpectrogramHidden = ref(true)
const isWaveformHidden = ref(false)
const isPianorollHidden = ref(true)

const hideBars = ref(true)
const showBars = ref(true)
const showIMI = ref(false)
const showIOI = ref(false)
const isIMIvisible = ref(false)

let selectedTimeAnnotation = ref([])
let selectedOnsetDetection = ref([])




/////WHEN REFRESH PAGE, LOAD WAVEFORMS
let trackNameStorage = JSON.parse(localStorage.getItem('trackName'))
let timeAnnotationStorage = JSON.parse(localStorage.getItem('timeAnnotation'))


if (trackNameStorage){
    let i = -1
    
    loadWaveforms(i)
}
function loadWaveforms(i){
    i++
    if(i < trackNameStorage.length){
        let prefixOfCuttedTrack 
        let nameOfCuttedTrack = trackNameStorage[i][0]
        let start = trackNameStorage[i][1]
        let end = trackNameStorage[i][2]
        let fromBar = trackNameStorage[i][3]
        let toBar = trackNameStorage[i][4]
        if(start && end){
            if(fromBar && toBar){
                prefixOfCuttedTrack = ' - bars (' + fromBar + ' - ' + toBar + ')'
            } else{
                prefixOfCuttedTrack = ' - trimmed (' + start.toFixed(2) + 's - ' + end.toFixed(2) + 's)'       
            }
            api.get('/get-trimmed-audio/' + prefixOfCuttedTrack + ' - '+ nameOfCuttedTrack.split(' ')[0])
            .then((response) => { 
                let audio = new Audio(response.request.responseURL)
                if(fromBar && toBar){
                    makeWaveform(audio,nameOfCuttedTrack ,start, end, fromBar, toBar )
                } else{
                    makeWaveform(audio,nameOfCuttedTrack ,start, end )
                }
                loadWaveforms(i)
            })
        } else {
            api.get('/get-audio-file/'+nameOfCuttedTrack)
            .then((response) => {  
                    
                let audio = new Audio(response.request.responseURL);
                makeWaveform(audio,nameOfCuttedTrack)  
                loadWaveforms(i)
                // marker(selectedTimeAnnotation[0][1], selectedTrackIndex)
            })
        }
    } 
}

function selectTrack(id){
    showIMI.value = false
    showIOI.value = false
    hideBars.value = true
    showBars.value = true
    

    let onset_detection = JSON.parse(localStorage.getItem('onset_detection'))
    selectedOnsetDetection.value = onset_detection.filter(onset => onset[0] == trackFromStart.value[id][0])

    if(selectedOnsetDetection.value.length != 0){  
        showIOI.value = true
        showIOIBtnIBIBtn(id)
    }
   
    timeAnnotationStorage = JSON.parse(localStorage.getItem('timeAnnotation'))
    if(timeAnnotationStorage){
        
        selectedTimeAnnotation.value = timeAnnotationStorage.filter(oneAnnotation => oneAnnotation[0] == trackFromStart.value[id][0])
        if(selectedTimeAnnotation.value.length != 0){
            if(wavesurfer[id].regions.list[1] != null){
                hideBars.value = false
            }else{  
                showBars.value = false
            }
            if(document.getElementById(`myChart-${id}`).style.display == 'block'){
                isIMIvisible.value = true
            }else{        
                isIMIvisible.value = false
            }
            showIMI.value = true         

        }
    }
    ///SPECTROGRAM CURSOR
    

    let specCursor = document.getElementById(`spectCursor-${id}`)
    let pianorollCursor = document.getElementById(`pianoroll-cursor-${id}`)
    if(specCursor){
        specCursor.style.marginLeft = `${wavesurfer[id].cursor.cursor.style.left.replace(/px/g, "") - wavesurfer[id].drawer.wrapper.scrollLeft}px`
    }
    if(pianorollCursor){
        pianorollCursor.style.marginLeft = `${wavesurfer[id].cursor.cursor.style.left.replace(/px/g, "") - wavesurfer[id].drawer.wrapper.scrollLeft}px`
    }
    
   
   
    wavesurfer[id].on('scroll', function () {
        let pianoroll = document.getElementById(`IMGpianoroll-${globalTrackIndex.selTrackIndex}`)
        pianoroll.style.marginLeft= `-${wavesurfer[id].drawer.wrapper.scrollLeft}px`
        let specLabels = document.getElementById(`spec-labels-${id}`)
        specLabels.style.marginLeft = `${wavesurfer[id].drawer.wrapper.scrollLeft}px`
        if(!wavesurfer[id].isPlaying()){
            specCursor.style.marginLeft = '0px'
            pianorollCursor.style.marginLeft = '0px'
            
    }})

    if(!isSpectrogramHidden.value){
        wavesurfer[id].backend.on('audioprocess', showSpectCursor)
    }else{
        wavesurfer[id].backend.un('audioprocess', showSpectCursor)

    }
    if(!isPianorollHidden.value){
        wavesurfer[id].backend.on('audioprocess', showPianorollCursor)
    }else{
        wavesurfer[id].backend.un('audioprocess', showPianorollCursor)
    }

}

const showSpectCursor = () => {
    let waveformClientWidth = wavesurfer[globalTrackIndex.selTrackIndex].drawer.wrapper.clientWidth
    let waveformScrollFullWidth = wavesurfer[globalTrackIndex.selTrackIndex].drawer.wrapper.scrollWidth
    if (wavesurfer[globalTrackIndex.selTrackIndex].drawer.wrapper.scrollLeft == 0){
        document.getElementById(`spectCursor-${globalTrackIndex.selTrackIndex}`).style.marginLeft = `${wavesurfer[globalTrackIndex.selTrackIndex].drawer.lastPos}px`
    }else if(waveformScrollFullWidth - wavesurfer[globalTrackIndex.selTrackIndex].drawer.lastPos < waveformClientWidth*0.5){
        document.getElementById(`spectCursor-${globalTrackIndex.selTrackIndex}`).style.marginLeft = `${waveformClientWidth - (waveformScrollFullWidth - wavesurfer[globalTrackIndex.selTrackIndex].drawer.lastPos)}px` 
    }else{
        document.getElementById(`spectCursor-${globalTrackIndex.selTrackIndex}`).style.marginLeft = `${waveformClientWidth*0.5}px` 
    }}

const showPianorollCursor = () => {
    let waveformClientWidth = wavesurfer[globalTrackIndex.selTrackIndex].drawer.wrapper.clientWidth
    let waveformScrollFullWidth = wavesurfer[globalTrackIndex.selTrackIndex].drawer.wrapper.scrollWidth
    if (wavesurfer[globalTrackIndex.selTrackIndex].drawer.wrapper.scrollLeft == 0){
        document.getElementById(`pianoroll-cursor-${globalTrackIndex.selTrackIndex}`).style.marginLeft = `${wavesurfer[globalTrackIndex.selTrackIndex].drawer.lastPos}px`
    }else if(waveformScrollFullWidth - wavesurfer[globalTrackIndex.selTrackIndex].drawer.lastPos < waveformClientWidth*0.5){
        document.getElementById(`pianoroll-cursor-${globalTrackIndex.selTrackIndex}`).style.marginLeft = `${waveformClientWidth - (waveformScrollFullWidth - wavesurfer[globalTrackIndex.selTrackIndex].drawer.lastPos)}px` 
    }else{
        document.getElementById(`pianoroll-cursor-${globalTrackIndex.selTrackIndex}`).style.marginLeft = `${waveformClientWidth*0.5}px` 
    }}


</script>


<template>


<div id="main-panel" class="bg-gray-100 -mt-3 pr-80 pl-10 -mx-3 border-b h">
    <!-- <div id="time-current"></div> -->

    <div id="playing" class="mb-0.5">

        <Icon icon="cil:media-play" width="24" id="playBtn" class="btn-hover-cursor" @click="playAll()"></Icon>
        <Icon icon="cil:media-pause" width="25" id="pauseBtn" class="btn-hover-cursor" @click="pauseAll()"></Icon>
        <Icon icon="cil:media-stop" width="25" id="stopBtn" class="btn-hover-cursor" @click="stopAll()"></Icon>
        

        <Icon icon="clarity:volume-up-line" @click="showVolume()" id="volume-btnOn" class="btn-hover-cursor" width="25"/>
        <Icon icon="clarity:volume-up-line" @click="hideVolume()" id="volume-btnOff" width="25" class="picker hidden btn-hover-cursor"/>
        <div class="inline hidden" id="volume-showed">
            <Icon icon="bi:volume-up" :inline="true" id="volume-mute"  width="25" @click="muteAll()" class="ml-2 btn-hover-cursor"/>
            <Icon icon="bi:volume-mute" :inline="true" id="volume-unMute"  width="25" @click="muteAll()" class="ml-2 hidden btn-hover-cursor"/>

            <input id="volume-slider" type="range" min="0" max="1" value="1" step="0.01" >

        </div>
        
                
        <div title = "waveform" class="ml-4">
            <Icon icon="mdi:waveform" width="50"  class="btn-hover mr-2" :class="{picker : !isWaveformHidden}" @click="$emit('showWaveform'); isWaveformHidden = !isWaveformHidden" />
        </div>
        <div title="spectrogram">
            <Icon icon="bi:border-width" width="50" :rotate="2" class="btn-hover mr-2" :class="{picker : !isSpectrogramHidden}" @click="$emit('showSpectrogram'); isSpectrogramHidden =! isSpectrogramHidden"/>
        </div>
        
        
        <div title="pianoroll">
            <Icon icon="gg:piano" width="50"  class="btn-hover mr-2" :class="{picker : !isPianorollHidden}" @click="$emit('showPianoroll'); isPianorollHidden =! isPianorollHidden"/>
        </div>
    
    <div class="flex">
        <InterMeasureInterval 
        :showIMI="showIMI" 
    
    :selectedTimeAnnotation="selectedTimeAnnotation[0]" 
    :isIMIvisible ="isIMIvisible"
    />

    <OnsetBeatsIntervals 
    :showIOI="showIOI" 
    :selectedOnsetDetection="selectedOnsetDetection" 
    :selectedTimeAnnotation="selectedTimeAnnotation"
    />
    </div>  

</div>
    <div class="controllers">

        <TimeSelection/>
        
        <BarSelection
        :showBars="showBars"
        :hideBars="hideBars"
        :selectedTimeAnnotation="selectedTimeAnnotation"
        />
        
        <MIDI/>
    </div>  

   
</div>


</template>


<style scoped>
.piano-roll{
    width: 6412px
}
.imagePR{
    
    width: 100%;
    height: 100%;
    


}
#main-panel{
    position: fixed;
    
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 20;
    
    width: 100%;
    white-space: nowrap;
    
}

#playing{
    display: flex;
    align-items: center;
    justify-content: space-between;
 
}

.controllers{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.375rem;
    
    
}





.buttons{
    
}

</style>
<style>
.picker{
    background-color: salmon;
    color: white;
}
.picker:hover{
    background-color: rgb(215, 209, 209);
   
}
.hide{
    display: none;
    
}
.deactive{
visibility: hidden;
}
</style>


