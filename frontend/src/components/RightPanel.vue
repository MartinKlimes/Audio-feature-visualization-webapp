<script setup>
import WaveformSetting from './visualizations/waveform/WaveformSetting.vue';
import PianorollSetting from './visualizations/pianoroll/PianorollSetting.vue';
import SpectrogramSetting from './visualizations/spectorgram/SpectrogramSetting.vue';
import BlueButttons from './buttons/BlueButttons.vue';
import { shallowRef } from 'vue';
import { Icon } from '@iconify/vue';

const currentTrackSetting = shallowRef()

// const visualizations = {'WaveformSetting' : 'mdi:waveform', 'icon-park:music-rhythm' : SpectrogramSetting, 'ph:piano-keys-thin' : PianorollSetting}
const visualizations = [[WaveformSetting, 'mdi:waveform'],[ SpectrogramSetting, 'icon-park:music-rhythm'], [PianorollSetting, 'ph:piano-keys-thin' ]]


setTimeout(() => {
    currentTrackSetting.value = WaveformSetting
}, 3000);

const props = defineProps({
    track: Object,
    isSelected: Boolean
    
})

</script>



<template>
  


<div v-show="isSelected" class="h-full p-1 rounded-md flex flex-col gap-1 items-center  " :class="track.backgroundColor">

    <span class="max-w-37 overflow-x-auto whitespace-nowrap font-serif text-sm font-bold opacity-60 rounded-md overflow-hidden"
    >
    {{track.trackName}}
    </span>

   

<div class="min-w-38 border rounded-md border-gray">

    <div class="flex max-w-37 overflow-x-auto gap-1 mb-1">
    
            <Icon v-for="(visualization, i) in visualizations" :key=i :icon="visualization[1]" width="23" 
            class="cursor-pointer p-0.5" @click="currentTrackSetting = visualization[0]"
            :class="[currentTrackSetting === visualization[0] ? ' bg-gray-100 shadow-inner shadow-dark-200 ' : 'bg-transparent hover:opacity-70', {'rounded-b-none rounded-l-md ' : i === 0}]"
            />
            <!-- <Icon  icon="mdi:waveform" width="20" class="rounded-b-none rounded-l-md cursor-pointer" @click="currentTrackSetting = WaveformSetting"
            :class="[currentTrackSetting === WaveformSetting ? ' bg-gray-100 shadow-inner shadow-dark-200' : 'bg-transparent' ]"
            /> -->

            <!-- <Icon  class="text-black" icon="icon-park:music-rhythm" @click="currentTrackSetting = SpectrogramSetting"/>
            <Icon  class="" icon="ph:piano-keys-thin" @click="currentTrackSetting = PianorollSetting"/> -->

   
    </div>


    <KeepAlive>
        <component :is="currentTrackSetting" :track="track"/>

    </KeepAlive>
    
    <!-- <WaveformSetting 
    v-if="track.waveform.isWaveform" 
    :track="track"/> -->

    <!-- <PianorollSetting 
    v-if="track.pianoroll.isPianoroll" 
    :track="track"/> -->


</div>

</div>  
</template>


<style scoped>
::-webkit-scrollbar {
  width: 4px;
  height: 10px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.5);
 
  
}

</style>