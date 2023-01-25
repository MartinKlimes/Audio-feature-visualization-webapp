<script setup>
import { ref, reactive, onMounted} from 'vue';
import { Icon } from '@iconify/vue';
import {wavesurfer, trackFromStart, track} from '../Waveform'; 
import { changeBackground } from '../filesFunctions';
import { trackIndex } from '../globalStores';
import { api } from '../../custom';
import { trackList } from '../globalStores';
import { createWavesurfer } from '../functions/waveform';

const currentTrackList = trackList()
const globalTrackIndex = trackIndex()

onMounted(() => {
    api.get('/get-audio-file/' + props.trackname)
        .then((response) => {
            const audioSrc = response.request.responseURL
            createWavesurfer(audioSrc ,props.trackname, props.id)
            
        })

})




const props = defineProps({
    id: Number,
    trackname: String
})

const state = reactive({
    isWaveformHide: false,
    isPlayBtnHide: false,
    isVolumeBtnHide: false,
    isMuteBtnHide: false,
})


let trackNameStorage = JSON.parse(localStorage.getItem('trackName'))

function activeVolumeSlider(id){
        var volumeInput = document.getElementById(`volume-slider-${id}`);
        var onChangeVolume = function (e) {
        wavesurfer[id].setVolume(e.target.value);
        };
        volumeInput.addEventListener('input', onChangeVolume);
        volumeInput.addEventListener('change', onChangeVolume);
}

function deleteVisualization(id){
   
    

    trackFromStart.value.forEach(element => {
        if(document.getElementById(`audioList-${element[0]}`)){
            document.getElementById(`audioList-${element[0]}`).style.backgroundColor = "rgba(221, 225, 227)"
        }
    });
    
    wavesurfer.splice(id,1)
    trackFromStart.value.splice(id, 1);
    localStorage.setItem(`trackName`, JSON.stringify(trackFromStart.value))

    // let index = track.value.filter(oneTrackName => oneTrackName[0] == track.value[id][0] && oneTrackName[1] == track.value[id][1] )
    // track.value.splice(track.value.indexOf(index[0]), 1);
    // console.log(track.value)

    // document.getElementById(`waveform-${id}`).style.display = "none" 
    // document.getElementById(`timeline-${id}`).style.display = "none" 
    

    // timeAnnotationStorage.splice(timeAnnotationStorage.indexOf(selectedTimeAnnotation[0]) ,1)
    // localStorage.setItem(`timeAnnotation`, JSON.stringify(timeAnnotationStorage))

}

const playTrack = (id) => {
    wavesurfer[id].play()
    state.isPlayBtnHide = true
    wavesurfer[id].on('finish', function () {
        state.isPlayBtnHide = false
    });
}

</script>


 

<template>
    <!-- //vif -->
<div justify="between" >
<div class="relative mt-1 border border-gray-300" :id="`waveformContainer-${id}`" :class="{'shadow-md shadow-gray-500' : id==globalTrackIndex.selTrackIndex}">
    <div :class="{hide : !state.isWaveformHide}" :id="`showWaveBtn-${id}`" @click="state.isWaveformHide = false">
        <Icon icon="ep:arrow-down"  width="18" class="btn-hover-cursor"/>
        <div class="inline text-gray-400 text-sm ml-3">{{trackname}} (w)</div>
    </div>
    <transition>
    
    
    <div :id="`waveform-${id}`" v-show="!state.isWaveformHide" >
        
        <Icon icon="bi:play" width="20"  :class="{hide : state.isPlayBtnHide}" :id="`playPause-btnOn-${id}`" @click="playTrack(id)" class="btn-hover-cursor" />

        <Icon icon="bi:pause" width="20"  :class="{hide : !state.isPlayBtnHide}" :id="`playPause-btnOff-${id}`" @click="wavesurfer[id].pause(); state.isPlayBtnHide = false"  class="btn-hover-cursor"/>

        <Icon icon="bi:volume-down" :class="{hide : state.isVolumeBtnHide}"    width="20" :id="`volume-btnOn-${id}`" @click="state.isVolumeBtnHide = true, activeVolumeSlider
        (id)" class="btn-hover-cursor"/>
        
        <div v-show="state.isVolumeBtnHide" class="inline" :id="`volume-showed-${id}`">
            
            <Icon  icon="bi:volume-down" :id="`volume-btnOff-${id}`"  width="20" @click="state.isVolumeBtnHide = false" class="picker btn-hover-cursor "/>

            <Icon icon="bi:volume-up" :class="{hide : state.isMuteBtnHide}"    :id="`volume-mute-${id}`"  width="20" @click="wavesurfer[id].toggleMute(); state.isMuteBtnHide = true" class="ml-2 btn-hover-cursor"/>
            <Icon icon="bi:volume-mute"  :class="{hide : !state.isMuteBtnHide}" :id="`volume-unMute-${id}`"  width="20" @click="wavesurfer[id].toggleMute(); state.isMuteBtnHide = false" class="ml-2 btn-hover-cursor"/>

            <input :id="`volume-slider-${id}`" type="range" min="0" max="1" value="1" step="0.01" >
            
        </div>
        
        <Icon icon="ep:arrow-up" width="18" @click="state.isWaveformHide = true" :id="`hideWaveBtn-${id}`" class="btn-hover-cursor"/>
        <div class="inline text-gray-400 text-sm">{{trackname}}</div>
        
        
        
    </div>
    </transition>
    <!-- <Icon icon="ci:close-small" v-show="!state.isWaveformHide" class="hover:bg-gray-300 transition cursor-pointer top-0 right-0 absolute -my-1  -mr-4.25 text-black" @click="deleteVisualization(id)"/> -->

    <div :class="{hide : state.isWaveformHide}" :id="`timeline-${id}`" ></div>

    </div>
</div>


</template>



<style scoped>

.v-enter-active,
.v-leave-active {
    transition: all 0.2s;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: scale(0.75);
}


</style>