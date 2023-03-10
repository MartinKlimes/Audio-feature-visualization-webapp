<script setup>
import { ref, onMounted} from 'vue';
import { Icon } from '@iconify/vue';
import { trackIndex } from '../globalStores';
import { api } from '../../custom';
import { createWavesurfer } from '../functions/waveform';
import { wavesurfer } from '../functions/waveform';


const globalTrackIndex = trackIndex()


onMounted(() => {
    api.get('/get-file/' + props.track.trackName)
    .then((response) => {
        const audioSrc = response.request.responseURL
        const colors = props.track.waveform.waveformColor.slice(2, -2).split('","')
        createWavesurfer(audioSrc ,props.track.trackName, props.track.id, colors[1], colors[0], props.track.waveform.splitChannels)
        
        // globalTrackIndex.changeIndex(props.track.id)
    })

})


const props = defineProps({
    track: Object,
    isSelected: Boolean
})

</script>


 

<template>
      <!-- //vif -->
<div justify="between" class=" rounded-sm py-0.5 " :class="props.track.backgroundColor">
<div class="relative mt-1  " :id="`waveformContainer-${props.track.id}`" :class="[{'shadow-md shadow-gray-500' : props.isSelected}]">
    <transition>
    
    <div :id="`waveform-${props.track.id}`" >
        <div class=" text-gray-400 ml-2 text-sm">{{props.track.trackName}}</div> 
        
    </div>
    </transition>
    <!-- <Icon icon="ci:close-small" v-show="!state.isWaveformHide" class="hover:bg-gray-300 transition cursor-pointer top-0 right-0 absolute -my-1  -mr-4.25 text-black" @click="deleteVisualization(id)"/> -->

    <div :id="`timeline-${props.track.id}`" ></div>

    </div>
</div>


</template>
