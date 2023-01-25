<script setup>
import { api } from '../../../custom';
import { makeWaveform } from '../../Waveform';
import { trackList } from '../../globalStores';
import { createWavesurfer } from '../../functions/waveform'
import { wavesurfer } from '../../functions/waveform';
import { Icon } from '@iconify/vue';
const currentTrackList = trackList()


const props = defineProps({
    track: Object,
})


const createWaveform = () => {

    // if(currentTrackList.selectTrack(props.id).isWaveform){
    //     document.getElementById(`waveformContainer-${props.id}`).style.visibility = 'hidden'
    // }else{ 
    //     currentTrackList.selectTrack(props.id).isWaveform = !currentTrackList.selectTrack(props.id).isWaveform 
    //     api.get("/change-track-status/isWaveform/" + props.name)

    // }
    if(!props.track.isWaveform){
        props.track.isWaveformLoading = true
        props.track.isWaveform = true
        props.track.isWaveformDisplayed = true
        api.get("/change-track-status/isWaveform/" + props.track.trackName)
        api.get("/change-track-status/isWaveformDisplayed/" + props.track.trackName)
    }else{
        props.track.isWaveformDisplayed = !props.track.isWaveformDisplayed
        api.get("/change-track-status/isWaveformDisplayed/" + props.track.trackName)
    }

}



const createSpectrogram = () => {
    currentTrackList.trackState[props.id].wavesurfer.play()
}


</script>


<template>
 

<div class="h-[47%] w-full mt-5 p-2 border border-dashed border-gray-500 rounded-md ">
        <div class="grid grid-cols-2 gap-2">
            <button class="btn-hover-cursor font-semibold w-22 shadow-sm shadow-dark-100" :class="{'bg-lime-500 hover:bg-lime-400': track.isWaveformDisplayed && !track.isWaveformLoading, 
            'bg-yellow-100 hover:bg-yellow-50' : track.isWaveform && !track.isWaveformDisplayed || track.isWaveformLoading,
         }" @click="createWaveform">Waveform <Icon
            v-if="track.isWaveformLoading == true"
            icon="fa:spinner"
            class="spin"
            :inline=true
            
           />
        </button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100" :class="{'text-xs bg-yellow-100 hover:bg-yellow-50' : track.isSpectrogramLoading == true}"
            @click="createSpectrogram">Spectrogram<Icon
            v-if="track.isSpectrogramLoading == true"
            icon="fa:spinner"
            class="spin"
            :inline=true
            
           /></button>
            <button class="btn-hover-cursor  w-22 font-semibold shadow-sm shadow-dark-100">Pianoroll</button>
            <div class="flex w-22 h-max">
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-r-none">IOI</button>
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-l-none">IBI</button>
            </div>
            
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Tempo</button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">RMS</button>

        

        </div>
    </div>
</template>