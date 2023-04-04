<script setup>
import WaveformSetting from './visualizations/waveform/WaveformSetting.vue';
import PianorollSetting from './visualizations/pianoroll/PianorollSetting.vue';
import SpectrogramSetting from './visualizations/spectrogram/SpectrogramSetting.vue';
import BlueButttons from './buttons/BlueButtons.vue';
import { shallowRef, watch,ref,watchEffect} from 'vue';
import { Icon } from '@iconify/vue';
import { trackIndex } from '../globalStores';

const currentTrackSetting = shallowRef()
const globalTrackIndex = trackIndex()

const visualizations = [[WaveformSetting, 'mdi:waveform'],[ SpectrogramSetting, 'icon-park:music-rhythm'], [PianorollSetting, 'ph:piano-keys-thin']]
const visualizationTxt = [[IMISetting, 'IMI'], [IOISetting, 'IOI'], [IBISetting, 'IBI']]

const list = ref([]);
watchEffect(() => {
    list.value[0] = props.track.waveform.isWaveform
    list.value[1] = props.track.spectrogram.isSpectrogram
    list.value[2] = props.track.pianoroll.isPianoroll
    for(let i = 0; i < list.value.length; i++) {
        if(list.value[i]) {
            currentTrackSetting.value = visualizations[i][0]
            break; 
        }
    }
})

watchEffect(() => {
    currentTrackSetting.value = visualizations[props.selectedVis][0]

})

const props = defineProps({
    track: Object,
    isSelected: Boolean,
    selectedVis: Number
    
})


</script>



<template>



<div v-show="isSelected" class="h-full p-1 rounded-md flex flex-col gap-1 items-center  " :class="track.backgroundColor">

    <span class="max-w-37 overflow-x-auto whitespace-nowrap font-serif text-sm font-bold opacity-60 rounded-md overflow-hidden"
    >
    {{track.trackName}}
    </span>

   

<div class="min-w-38 border-2 rounded-md border-gray ">

    <div class="flex  overflow-x-auto gap-1 mb-1">
  
            <Icon v-for="(visualization, i) in visualizations" :key=i 
           v-show="list[i]"
            :icon="visualization[1]" width="23" 
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
<style>
.box {
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);

}
.boxTight {
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);

}

</style>