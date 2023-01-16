<script setup>
import { Icon } from '@iconify/vue';
import { ref, reactive, onMounted } from 'vue';
import { wavesurfer,trackFromStart, marker } from '../../Waveform';
import { addTxtFilesToUpload } from '../../filesFunctions';
import { trackIndex } from '../../globalStores';
import clickAudio from '/public/click.mp3'


const globalTrackIndex = trackIndex()

var click = new Audio(clickAudio)
click.volume = 1

const fromBar = ref(0)
const toBar = ref(0)
const isToggled = ref(true)

 

let clickOnBarLineIndex
let timeAnnotation

onMounted(() => {
    window.eventBus.on('select', event => clickOnBarLineIndex = 0)        
       
})

const props = defineProps({
    hideBars: Boolean,
    showBars: Boolean,
    selectedTimeAnnotation: Array
})


function selectBar(hideBars){   
    window.eventBus.emit('stopTimeSelection') 

    if(!hideBars){

        if (toBar.value < fromBar.value){
            toBar.value = fromBar.value
        }
        
        if (wavesurfer[globalTrackIndex.selTrackIndex].regions.list['selected']){
            wavesurfer[globalTrackIndex.selTrackIndex].regions.list['selected'].remove()
        }
        var reg = wavesurfer[globalTrackIndex.selTrackIndex].addRegion({
            id: 'selected',
            drag: false,
            resize: false,
            color: 'hsla(207, 52%, 50%, 0.25)',
            start: wavesurfer[globalTrackIndex.selTrackIndex].regions.list[fromBar.value].start,
            end: wavesurfer[globalTrackIndex.selTrackIndex].regions.list[toBar.value].end,
        })
    }else{
        wavesurfer[globalTrackIndex.selTrackIndex].clearRegions()
        wavesurfer[globalTrackIndex.selTrackIndex].clearMarkers()
    }
}

const playSoundOnBars = (selectedTimeAnnotation) => {
    timeAnnotation = selectedTimeAnnotation 
    wavesurfer.forEach(oneWavesurfer => {
        oneWavesurfer.backend.on('audioprocess',clickSound)
    });
}
const muteSoundOnBars = () => {
      wavesurfer.forEach(oneWavesurfer => {
        oneWavesurfer.backend.un('audioprocess',clickSound)
    });
}
const clickSound = () => {
    if (wavesurfer[globalTrackIndex.selTrackIndex].isPlaying()) {        
        if (wavesurfer[globalTrackIndex.selTrackIndex].getCurrentTime() > timeAnnotation[0][1][clickOnBarLineIndex]){
            click.play()
            clickOnBarLineIndex +=1
        }
    }
}

</script>


<template>
<div class="flex flex-col items-center ">
    <div class="flex mt-1  rounded-md">
    <input v-model="fromBar" type="number" placeholder="from" class="input-field-nomargin w-12 border-2 border-blue-400 " @change="selectBar(hideBars)">
    <input v-model="toBar" type="number" placeholder="to"  class="input-field-nomargin w-12 border-2 border-blue-400 ml-1" @change="selectBar(hideBars)">
</div>
    <button class="btn btn-blue hover:bg-blue-500 transition mt-1" @click="selectBar(hideBars)">Select bars {{fromBar}} to {{toBar}}</button>
</div>

<!-- <div v-show="!hideBars" class="flex ">
    <input v-model="fromBar" type="number" placeholder="from" class="input-field-nomargin w-12 mx-1 mt-1 " @change="selectBar(hideBars)">
    <input v-model="toBar" type="number" placeholder="to"  class="input-field-nomargin w-12 mr-1 mt-1" @change="selectBar(hideBars)">
    <button class="btn hover:bg-gray-300 transition mt-1" @click="trimWaveform(wavesurfer[globalTrackIndex.selTrackIndex].regions.list[fromBar].start,wavesurfer[globalTrackIndex.selTrackIndex].regions.list[toBar].end, globalTrackIndex.selTrackIndex, fromBar, toBar); hideBars =! hideBars; selectBar(hideBars)">Select bars {{fromBar}} to {{toBar}}</button>
 
        <Icon icon="clarity:volume-up-line" width="50" :class="{hide: isToggled}" class="btn-hover mr-1 mt-1 picker "  @click=" isToggled = !isToggled; muteSoundOnBars()"/>
        <Icon icon="clarity:volume-mute-line" width="50" :class="{hide: !isToggled}" class="btn-hover mr-1 mt-1"  @click=" isToggled = !isToggled; playSoundOnBars(selectedTimeAnnotation)"/>
  
</div> 
<button  class="btn-hover" :class="{hide : showBars}" @click="selectBar(hideBars); marker(selectedTimeAnnotation[0][1], globalTrackIndex.selTrackIndex); hideBars =! hideBars;showBars =! showBars">Show Bars</button>
<button class="btn-hover picker" :class="{hide : hideBars}" @click=" hideBars =! hideBars; showBars = !showBars; selectBar(hideBars)">Hide Bars</button>

<label for="added-textFile" class="hover:cursor-pointer" >
    <div id="add-files-btn" class="btn-hover">Upload bars</div>
</label>
<input id="added-textFile" type="file" class="hidden" accept=".txt" multiple 
@change="addTxtFilesToUpload(globalTrackIndex.selTrackIndex, trackFromStart[globalTrackIndex.selTrackIndex][0]); hideBars = !hideBars"> -->





</template>

<style scoped>

#bars-selection{
    display: flex;
    align-items: center;
    justify-content: space-between;
   
}
</style>