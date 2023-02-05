<script setup>
import WaveformSetting from './VisualizationSetting/waveform/WaveformSetting.vue';
import { trackIndex } from '../globalStores';

const globalTrackIndex = trackIndex()

const props = defineProps({
    track: Object,
})

</script>



<template>


<div v-show="track.id == globalTrackIndex.selTrackIndex" class="w-[99%] h-full p-1 rounded-md flex flex-col gap-1 items-center " :class="track.backgroundColor">
    <span class="font-serif text-sm font-bold opacity-60 rounded-md max-h-5 overflow-hidden " :class="{'text-xs py-1' : track.trackName.length > 16}">{{track.trackName}}</span>

    <div class="h-max w-full p-2 bg-gray-200 rounded-md border  border-gray-300 shadow-md flex ">
        
        <WaveformSetting 
        v-if="track.isWaveform" 
        :track="track"/>
    
        
    </div>
    <!-- <div class="h-55 w-full p-2 bg-gray-200 rounded-md border border-gray-300 shadow-md flex ">
        
        {{ track.trackName }}
    
        
    </div> -->
    <!-- <SpectrogramSetting/> -->
    
</div>

</template>
