<script setup>
import { ref, onMounted, onUnmounted, onDeactivated, onActivated } from 'vue';
import { changeBackground } from '../../filesFunctions';
import { trackFromStart } from '../../Waveform';
import { trackIndex, trackList} from '../../globalStores';
import { api } from '../../../custom';
import { wavesurfer, trimWaveform } from '../../functions/waveform';

const globalTrackIndex = trackIndex()
const currentTrackList = trackList()

const isCheckTime = ref(true)
const from = ref()
const to = ref()

const props = defineProps({
    id: Number,
    trackName: String,
})

onMounted(() => {
    selectTime()
})
// onUnmounted(() => {
//     wavesurfer[props.id].clearRegions()
//     wavesurfer[props.id].disableDragSelection()
// })

onDeactivated(() => {
  // called when removed from the DOM into the cache
  // and also when unmounted
    wavesurfer[props.id].clearRegions()
    wavesurfer[props.id].disableDragSelection()
})

onActivated(() => {
  // called on initial mount
  // and every time it is re-inserted from the cache
  selectTime()
})

function selectTime(){
    if (wavesurfer[props.id].regions.list){
        wavesurfer[props.id].clearRegions()
    }  
    var reg = wavesurfer[props.id].addRegion({
        start: from.value,
        end: to.value,
        color: 'hsla(200, 100%, 30%, 0.3)'
    })

    if (to.value < from.value){
        to.value = from.value
    }
    var reg = wavesurfer[props.id].enableDragSelection({
        start: from.value,
        end: to.value,
    })
      
    wavesurfer[props.id].on("region-updated", (region, e) => {  
            var regions = wavesurfer[props.id].regions.list;
            var keys = Object.keys(regions);
            if(keys.length > 1){
                regions[keys[0]].remove();
            }
            from.value = region.start
            to.value = region.end
            region.color = 'hsla(200, 100%, 30%, 0.3)'
    })

}

const trimAudio = () => {
    
    api.get('/trim-audio/' + props.trackName + '/' + from.value + '/' + to.value + '/undefined/undefined')
    .then((response) => {
        // console.log(response.data);
        currentTrackList.fill()
    })
    // .then((response) => {  
    //     // getOnset(nameOfCuttedTrack + ' - ' +trackFromStart.value[selectedTrackIndex][0], trackFromStart.value[selectedTrackIndex][0] + nameOfCuttedTrack)
    // })

    // currentTrackList.addTrack(props.trackName)


    // trimWaveform(props.trackName, from.value, to.value, props.id)  
 /////využít audio list, aby nebylo nutné taht ze serveru řpes get-audio
    

}


</script>


<template>

<div class="flex flex-col items-center ">
    <div class="flex mt-1  rounded-md">
    <input v-model="from" type="number" placeholder="from" class="input-field-nomargin w-15 border-2 border-blue-400" @change="selectTime()">
    <input v-model="to" type="number" placeholder="to"  class="input-field-nomargin w-15 ml-1 border-2 border-blue-400" @change="selectTime()">
    </div>
    <button class="btn btn-blue hover:bg-blue-500 transition w-max mt-1" @click="trimAudio">Select</button>
</div>

<!-- <button class="btn-hover" :class="{ picker : !isCheckTime}" @click=" isCheckTime=! isCheckTime; selectTime()">Select a section</button> -->
</template>



<style scoped>

#time-selection{
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>





