<script setup>
import { api } from '../../../custom';
import { trackList } from '../../globalStores';
import { createWavesurfer } from '../../functions/waveform'
import { wavesurfer } from '../../functions/waveform';
import { Icon } from '@iconify/vue';
import BlueButttons from '../buttons/BlueButtons.vue';
import {updateRecording} from '../../../custom'
import Plotly from 'plotly.js-dist'
import { showAlert, closeAlert } from '../../alerts';

const currentTrackList = trackList()

const props = defineProps({
    track: Object,
})


const createVisualization = (visualization, isVisualization, isVisualizationDisplayed) => {
    updateRecording(props.track.id, isVisualizationDisplayed, !visualization[isVisualizationDisplayed])

    if(!visualization[isVisualization]){
        visualization[isVisualization + 'Loading'] = true
        visualization[isVisualization] = true
        visualization[isVisualizationDisplayed] = true
        updateRecording(props.track.id,isVisualization, true)
    }else {
        visualization[isVisualizationDisplayed] = !visualization[isVisualizationDisplayed]
    }
}


const createPianoroll = (params) => {
    if(props.track.MIDIFileName){
        createVisualization(props.track.pianoroll, 'isPianoroll', 'isPianorollDisplayed')
        // setTimeout(() => {
        //     props.track.waveform.isWaveformReady = false
            
        // }, 1000);
    }else{
        showAlert('First select MIDI file!')
        setTimeout(closeAlert, 1500)
    }
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

        <BlueButttons :is-btn-clicked="track.waveform.isWaveformDisplayed " :isDisabled="!track.waveform.isWaveform" icon-class='hidden' @click="createVisualization(track.waveform, 'isWaveform', 'isWaveformDisplayed')" class="h-6">Waveform</BlueButttons>
        
        <BlueButttons 
        :is-btn-clicked="track.spectrogram.isSpectrogramDisplayed " 
        :isDisabled="!track.spectrogram.isSpectrogram" 
        :icon="(track.spectrogram.isSpectrogramLoading ? 'fa:spinner' : '')" 
        :icon-class="(track.spectrogram.isSpectrogramLoading ? 'spin' : 'hidden')" 
        @click="createVisualization(track.spectrogram, 'isSpectrogram', 'isSpectrogramDisplayed')
" 
        :class="{'text-xs' : track.spectrogram.isSpectrogramLoading}" class="h-6">Spectrogram</BlueButttons>

        <!-- <BlueButttons   @click="createSpectrogram()" class="h-6">Spectrogram</BlueButttons> -->

       
        <BlueButttons 
        :is-btn-clicked="track.pianoroll.isPianorollDisplayed" 
        :isDisabled="!track.pianoroll.isPianoroll" 
        :icon="(track.pianoroll.isPianorollLoading ? 'fa:spinner' : '')" 
        :icon-class="(track.pianoroll.isPianorollLoading  ? 'spin' : 'hidden')" 
        @click="createPianoroll" 
        :class="{'text-xs' : track.pianoroll.isPianorollLoading }" class="h-6"
        >
        Pianoroll</BlueButttons>

            <div class="flex w-22 h-max">
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-r-none" @click="">IOI</button>
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-l-none">IBI</button>
            </div>
            
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Tempo</button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">RMS</button>

        

        </div>
    </div>
</template>