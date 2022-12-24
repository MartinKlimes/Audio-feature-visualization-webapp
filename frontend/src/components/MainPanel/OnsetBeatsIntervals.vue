<script setup>
import { Icon } from '@iconify/vue';
import { ref, onMounted } from 'vue';
import { trackIndex, trackList } from '../../globalStores';
import { wavesurfer } from '../../Waveform';
import IOISound from '/public/beepIOI.mp3'
import IBISound from '/public/beepIBI.mp3'

var IOIAudio = new Audio(IOISound);
var IBIAudio = new Audio(IBISound);


const globalTrackIndex = trackIndex()
const isIOIVolumeToggled = ref(false)
const isIBIVolumeToggled = ref(false)
let clickOnIOILineIndex = 0
let clickOnIBILineIndex = 0
let IOISoundAnnotation
let IBISoundAnnotation


const props = defineProps({
    showIOI: Boolean,
    selectedOnsetDetection: Array,
    selectedTimeAnnotation: Array

})
onMounted(() => {
    window.eventBus.on('select', event => clickOnIOILineIndex = 0)   
    window.eventBus.on('select', event => clickOnIBILineIndex = 0)   
})

function interOnsetInterval(selectedOnset, selectedTrackIndex, selectedTimeAnnotation, onset){
    if (onset == true){
       
        var index = `onset-line-${selectedTrackIndex}`
        var indexBtn = 'IOIbtn'
        var volumeBtn = 'showVolumeIOI'
        var onset_index = 0
        var color = 'red'
        
    } else{
        var index = `beats-line-${selectedTrackIndex}`
        var indexBtn = 'IBIbtn'
        var volumeBtn = 'showVolumeIBI'
        var onset_index = 1
        var color = 'blue'
    }
    

    if (document.getElementById(index)){
       
        
        if (document.getElementById(index).hidden == true){
            var onsetLines = document.querySelectorAll(`#${index}`)
            onsetLines.forEach(line => {
                line.hidden = false
            })
            document.getElementById(indexBtn).className = 'btn-hover picker'
            document.getElementById(volumeBtn).className = 'flex'
        } else{
            var onsetLines = document.querySelectorAll(`#${index}`)

            onsetLines.forEach(line => {
                line.hidden = true
            })
            document.getElementById(indexBtn).className = 'btn-hover'
            document.getElementById(volumeBtn).className = 'hidden'
            // if(document.getElementById('IOIbtn').className == 'btn-hover picker' || document.getElementById('IBIbtn').className == 'btn-hover picker'){
            //     document.getElementById('showVolumeIOI').className = ''
            // }
        }
        
    } else{
        
        wavesurfer[selectedTrackIndex].clearMarkers()
       
        selectedOnset[onset_index].forEach(function(onset, id){
          
            wavesurfer[selectedTrackIndex].addMarker({
                time: onset,               
            })
            var marginLeft = wavesurfer[selectedTrackIndex].markers.markers[id].el.offsetLeft
            var lineWaveform = document.createElement("div")
            lineWaveform.id = index
            var styles = 'border-left: 2px dashed ' + color + ' ;'
                        + 'margin-left: ' + marginLeft + 'px;'
                        + 'height: 128px;'
                        + 'z-index: 4;'
                        + 'position: absolute;'
                            
            lineWaveform.setAttribute('style', styles);
            wavesurfer[selectedTrackIndex].drawer.wrapper.appendChild(lineWaveform)
            
            var lineSpectrogram = document.createElement("div")
            lineSpectrogram.id =index
            var styles = 'border-left: 1px dotted white; '
                        + 'margin-left: ' + marginLeft + 'px;'
                        + 'height: 300px;'
                        + 'z-index: 5;'
                        + 'position: absolute;' 
                        + 'opacity: .5'
                                
            lineSpectrogram.setAttribute('style', styles);
            wavesurfer[selectedTrackIndex].spectrogram.wrapper.appendChild(lineSpectrogram)

        })

       
        wavesurfer[selectedTrackIndex].clearMarkers()
        if(wavesurfer[selectedTrackIndex].regions.list[1] != null){
            selectedTimeAnnotation[0][1].forEach(function(oneMarker, id){
                wavesurfer[selectedTrackIndex].addMarker({
                    time: oneMarker,
                    label: id+1,
                    color: "black",
                })
            })
        }
        // if (onset == true){
        //     document.getElementById('IOIbtn').className = 'btn-hover picker'
        //     document.getElementById(volumeBtn).className = ''
        // } else{
        //     document.getElementById('IBIbtn').className = 'btn-hover picker'
        // }
        document.getElementById(indexBtn).className = 'btn-hover picker'
        document.getElementById(volumeBtn).className = ''
        
    }

}


const playSoundOnIOI = (selectedOnsetDetection) => {
    IOISoundAnnotation = selectedOnsetDetection
    wavesurfer.forEach(oneWavesurfer => {
        oneWavesurfer.backend.on('audioprocess',IOISoundActivate)
    });

}
const muteSoundOnIOI = () => {
    wavesurfer.forEach(oneWavesurfer => {
        oneWavesurfer.backend.un('audioprocess',IOISoundActivate)
    });
}
const IOISoundActivate = () => {
    if (wavesurfer[globalTrackIndex.selTrackIndex].isPlaying()) {        
        if (wavesurfer[globalTrackIndex.selTrackIndex].getCurrentTime() > IOISoundAnnotation[0][1][0][clickOnIOILineIndex]){
            IOIAudio.play()
            clickOnIOILineIndex +=1
        }
    }
}        

const playSoundOnIBI = (selectedOnsetDetection) => {
    IBISoundAnnotation = selectedOnsetDetection
    wavesurfer.forEach(oneWavesurfer => {
        oneWavesurfer.backend.on('audioprocess',IBISoundActivate)
    });
}
const muteSoundOnIBI = () => {
    wavesurfer.forEach(oneWavesurfer => {
        oneWavesurfer.backend.un('audioprocess',IBISoundActivate)
    });
}
const IBISoundActivate = () => {
    if (wavesurfer[globalTrackIndex.selTrackIndex].isPlaying()) {        
        if (wavesurfer[globalTrackIndex.selTrackIndex].getCurrentTime() > IBISoundAnnotation[0][1][1][clickOnIBILineIndex]){
            IBIAudio.play()
            clickOnIBILineIndex +=1
        }
    }
}        
     

</script>




<template>

<button v-show="showIOI" class="btn-hover" id="IOIbtn" title="Inter-Onset-Intervals,"  @click="interOnsetInterval(selectedOnsetDetection[0][1], globalTrackIndex.selTrackIndex, selectedTimeAnnotation, onset = true)">IOI</button>
<div class="hidden" id="showVolumeIOI">
    <Icon icon="clarity:volume-up-line" width="50" v-show="isIOIVolumeToggled" class="btn-hover mr-2 picker"  @click="isIOIVolumeToggled = !isIOIVolumeToggled; muteSoundOnIOI()"/>
    <Icon icon="clarity:volume-mute-line" width="50" v-show="!isIOIVolumeToggled" class="btn-hover mr-2"  @click="isIOIVolumeToggled = !isIOIVolumeToggled;playSoundOnIOI(selectedOnsetDetection) "/>
</div>

<button v-show="showIOI" class="btn-hover" id="IBIbtn" title="Inter-Beats-Intervals,"  @click="interOnsetInterval(selectedOnsetDetection[0][1], globalTrackIndex.selTrackIndex, selectedTimeAnnotation)">IBI</button>
<div class="hidden" id="showVolumeIBI">
    <Icon icon="clarity:volume-up-line" width="50" v-show="isIBIVolumeToggled" class="btn-hover mr-2 picker"  @click="isIBIVolumeToggled = !isIBIVolumeToggled; muteSoundOnIBI()"/>
    <Icon icon="clarity:volume-mute-line" width="50" v-show="!isIBIVolumeToggled" class="btn-hover mr-2"  @click="isIBIVolumeToggled = !isIBIVolumeToggled; playSoundOnIBI(selectedOnsetDetection)"/>
</div>
</template>