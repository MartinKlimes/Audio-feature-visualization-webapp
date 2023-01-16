<script setup>
import { api } from '../../../custom';
import { makeWaveform } from '../../Waveform';
import { trackList } from '../../globalStores';
import { createWavesurfer } from '../../functions/waveform'

const currentTrackList = trackList()


const props = defineProps({
    id: Number,
    name: String,
})


const createWaveform = () => {
    currentTrackList.selectTrack(props.id).isWaveform = !currentTrackList.selectTrack(props.id).isWaveform 
    api.get("/change-track-status/isWaveform/" + props.name)

}



const createSpectrogram = () => {
    currentTrackList.trackState[props.id].wavesurfer.play()
}


</script>


<template>

<div class="h-[47%] w-full mt-5 p-2 border border-dashed border-gray-500 rounded-md ">
        <div class="grid grid-cols-2 gap-2">
            <button class="btn-hover-cursor font-semibold w-22 shadow-sm shadow-dark-100" @click="createWaveform">Waveform</button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100" @click="createSpectrogram">Spectrogram</button>
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