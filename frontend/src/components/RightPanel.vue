<script setup>
import WaveformSetting from './VisualizationSetting/WaveformSetting.vue';
import { trackIndex } from '../globalStores';

const globalTrackIndex = trackIndex()

const props = defineProps({
    track: Object,
})

</script>



<template>
    

    <div v-show="track.id == globalTrackIndex.selTrackIndex" class="w-[99%] border-l border-gray-300 rounded-md flex flex-col gap-1">
        <div class="h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 flex ">
            
            <WaveformSetting 
            v-if="track.isWaveform" 
            :trackName="track.trackName" 
            :id="track.id"/>
        
            
        </div>
        <div class="h-55 w-full p-2 bg-gray-200 rounded-md border border-gray-300 flex ">
            
            {{ track.trackName }}
        
            
        </div>
        <!-- <SpectrogramSetting/> -->
        
    </div>

</template>
