<script setup>
import { ref, reactive, onMounted} from 'vue';
import { Icon } from '@iconify/vue';
import { trackIndex } from '../globalStores';
import { api } from '../../custom';
import { trackList } from '../globalStores';
import { createWavesurfer } from '../functions/waveform';
import { wavesurfer } from '../functions/waveform';


const currentTrackList = trackList()
const globalTrackIndex = trackIndex()


onMounted(() => {
    api.get('/get-file/' + props.track.trackName)
    .then((response) => {
        const audioSrc = response.request.responseURL
        createWavesurfer(audioSrc ,props.track.trackName, props.track.id, props.track.waveformColor.split(',')[1], props.track.waveformColor.split(',')[0], props.track.splitChannels)
        globalTrackIndex.selTrackIndex = props.track.id
    })

})


const props = defineProps({
    track: Object
})
const state = reactive({
    isWaveformHide: false,
    isPlayBtnHide: false,
    isVolumeBtnHide: false,
    isMuteBtnHide: false,
})



// function activeVolumeSlider(id){
//         var volumeInput = document.getElementById(`volume-slider-${id}`);
//         var onChangeVolume = function (e) {
//         wavesurfer[id].setVolume(e.target.value);
//         };
//         volumeInput.addEventListener('input', onChangeVolume);
//         volumeInput.addEventListener('change', onChangeVolume);
// }





</script>


 

<template>
      <!-- //vif -->
<div justify="between" class=" rounded-sm px-1 py-0.5 " :class="props.track.backgroundColor">
<div class="relative mt-1  " :id="`waveformContainer-${props.track.id}`" :class="[{'shadow-md shadow-gray-500' : props.track.id==globalTrackIndex.selTrackIndex}]">
    <!-- <div :class="{'hidden' : !state.isWaveformHide}" :id="`showWaveBtn-${props.track.id}`" @click="state.isWaveformHide = false">
        <Icon icon="ep:arrow-down"  width="18" class="btn-hover-cursor"/>
        <div class="inline text-gray-400 text-sm ml-3">{{track.trackName}} (w)</div>
    </div> -->
    
    <transition>
    
    
    <div :id="`waveform-${props.track.id}`" v-show="!state.isWaveformHide">
        <div class=" text-gray-400 ml-2 text-sm">{{props.track.trackName}}</div> 

        <!-- <Icon icon="bi:play" width="20"  :class="{'hidden' : state.isPlayBtnHide}" :id="`playPause-btnOn-${track.id}`" @click="playTrack(track.id)" class="btn-hover-cursor" />

        <Icon icon="bi:pause" width="20"  :class="{'hidden' : !state.isPlayBtnHide}" :id="`playPause-btnOff-${track.id}`" @click="wavesurfer[track.id].pause(); state.isPlayBtnHide = false"  class="btn-hover-cursor"/>

        <Icon icon="bi:volume-down" :class="{hide : state.isVolumeBtnHide}"    width="20" :id="`volume-btnOn-${track.id}`" @click="state.isVolumeBtnHide = true, activeVolumeSlider
        (id)" class="btn-hover-cursor"/>
        
        <div v-show="state.isVolumeBtnHide" class="inline" :id="`volume-showed-${track.id}`">
            
            <Icon  icon="bi:volume-down" :id="`volume-btnOff-${id}`"  width="20" @click="state.isVolumeBtnHide = false" class="picker btn-hover-cursor "/>

            <Icon icon="bi:volume-up" :class="{hide : state.isMuteBtnHide}"    :id="`volume-mute-${track.id}`"  width="20" @click="wavesurfer[track.id].toggleMute(); state.isMuteBtnHide = true" class="ml-2 btn-hover-cursor"/>
            <Icon icon="bi:volume-mute"  :class="{hide : !state.isMuteBtnHide}" :id="`volume-unMute-${track.id}`"  width="20" @click="wavesurfer[track.id].toggleMute(); state.isMuteBtnHide = false" class="ml-2 btn-hover-cursor"/>

            <input :id="`volume-slider-${track.id}`" type="range" min="0" max="1" value="1" step="0.01" >
            
        </div>
        
        <Icon icon="ep:arrow-up" width="18" @click="state.isWaveformHide = true" :id="`hideWaveBtn-${track.id}`" class="btn-hover-cursor"/>-->
        
        
        
        
    </div>
    </transition>
    <!-- <Icon icon="ci:close-small" v-show="!state.isWaveformHide" class="hover:bg-gray-300 transition cursor-pointer top-0 right-0 absolute -my-1  -mr-4.25 text-black" @click="deleteVisualization(id)"/> -->

    <div :class="{hide : state.isWaveformHide}" :id="`timeline-${props.track.id}`" ></div>

    </div>
</div>


</template>
