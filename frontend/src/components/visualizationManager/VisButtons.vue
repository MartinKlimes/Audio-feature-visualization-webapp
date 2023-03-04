<script setup>
import { api } from '../../../custom';
import { makeWaveform } from '../../Waveform';
import { trackList } from '../../globalStores';
import { createWavesurfer } from '../../functions/waveform'
import { wavesurfer } from '../../functions/waveform';
import { Icon } from '@iconify/vue';
import BlueButttons from '../buttons/BlueButttons.vue';
import {updateRecording} from '../../../custom'
import Plotly from 'plotly.js-dist'


const currentTrackList = trackList()


const props = defineProps({
    track: Object,
})



const createWaveform = () => {
    updateRecording(props.track.trackName,'isWaveformDisplayed', !props.track.waveform.isWaveformDisplayed)
    if(!props.track.waveform.isWaveform){
        props.track.waveform.isWaveformLoading = true
        props.track.waveform.isWaveform = true
        props.track.waveform.isWaveformDisplayed = true
        updateRecording(props.track.trackName,'isWaveform', true)
    }else{
        props.track.waveform.isWaveformDisplayed = !props.track.waveform.isWaveformDisplayed
    }
}

const createSpectrogram = () => {
    if (!wavesurfer[props.track.id]) {
        props.track.waveform.isWaveform = true
        updateRecording(props.track.trackName,'isWaveform', true)

    }
    createVisualization(props.track.spectrogram, 'isSpectrogram', 'isSpectrogramDisplayed')

}

const createPianoroll = () => {
    updateRecording(props.track.trackName,'isPianorollDisplayed', !props.track.pianoroll.isPianorollDisplayed)

    if(!props.track.pianoroll.isPianoroll){
        props.track.pianoroll.isPianorollLoading = true
        props.track.pianoroll.isPianoroll = true
        props.track.pianoroll.isPianorollDisplayed = true
        updateRecording(props.track.trackName,'isPianoroll', true)
    }else{
        props.track.pianoroll.isPianorollDisplayed = !props.track.pianoroll.isPianorollDisplayed
        

    }
    
}
const createVisualization = (visualization, isVisualization, isVisualizationDisplayed) => {
    updateRecording(props.track.trackName, isVisualizationDisplayed, !visualization[isVisualizationDisplayed])

    if(!visualization[isVisualization]){
        visualization[isVisualization + 'Loading'] = true
        visualization[isVisualization] = true
        visualization[isVisualizationDisplayed] = true
        updateRecording(props.track.trackName,isVisualization, true)
    }else {
        visualization[isVisualizationDisplayed] = !visualization[isVisualizationDisplayed]
    }
}



const plotSpectrogram = () => {
    updateRecording(props.track.trackName,'isPianoroll', false)

}

</script>


<template>
 

<div class="h-[47%] w-full mt-5 p-2 border  shadow-md  border-gray-500 rounded-md bg-white ">
        <div class="grid grid-cols-2 gap-2">
            <!-- <button class="btn-hover-cursor font-semibold w-22 shadow-sm shadow-dark-100" :class="{'bg-lime-500 hover:bg-lime-400': track.isWaveformDisplayed && !track.isWaveformLoading, 
            'bg-yellow-100 hover:bg-yellow-50' : track.isWaveform && !track.isWaveformDisplayed || track.isWaveformLoading,
         }" @click="createWaveform">Waveform <Icon
            v-if="track.isWaveformLoading == true"
            icon="fa:spinner"
            class="spin"
            :inline=true
            
           />
        </button> -->

        <BlueButttons :is-btn-clicked="track.waveform.isWaveformDisplayed " :isDisabled="!track.waveform.isWaveform" :icon="(track.waveform.isWaveformLoading ? 'fa:spinner' : '')" :icon-class="(track.waveform.isWaveformLoading ? 'spin' : 'hidden')" @click="createVisualization(track.waveform, 'isWaveform', 'isWaveformDisplayed')" :class="{'text-xs' : track.waveform.isWaveformLoading}" class="h-6">Waveform</BlueButttons>

        <BlueButttons :is-btn-clicked="track.spectrogram.isSpectrogramDisplayed " :isDisabled="!track.spectrogram.isSpectrogram" :icon="(track.spectrogram.isSpectrogramLoading ? 'fa:spinner' : '')" :icon-class="(track.spectrogram.isSpectrogramLoading ? 'spin' : 'hidden')" @click="createSpectrogram" :class="{'text-xs' : track.spectrogram.isSpectrogramLoading}" class="h-6">Spectrogram</BlueButttons>

        <!-- <BlueButttons   @click="createSpectrogram()" class="h-6">Spectrogram</BlueButttons> -->

       
        <BlueButttons :is-btn-clicked="track.pianoroll.isPianorollDisplayed" :isDisabled="!track.pianoroll.isPianoroll" :icon="(track.pianoroll.isPianorollLoading ? 'fa:spinner' : '')" :icon-class="(track.pianoroll.isPianorollLoading  ? 'spin' : 'hidden')" @click="createVisualization(track.pianoroll, 'isPianoroll', 'isPianorollDisplayed')" :class="{'text-xs' : track.pianoroll.isPianorollLoading }" class="h-6">Pianoroll</BlueButttons>

            <div class="flex w-22 h-max">
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-r-none" @click="plotSpectrogram">IOI</button>
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-l-none">IBI</button>
            </div>
            
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Tempo</button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">RMS</button>

        

        </div>
    </div>
</template>