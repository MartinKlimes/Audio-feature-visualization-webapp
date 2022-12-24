<script setup>
import { ref, onMounted } from 'vue';
import { wavesurfer } from '../../Waveform';
import { changeBackground } from '../../filesFunctions';
import { trackFromStart, trimWaveform } from '../../Waveform';
import { trackIndex } from '../../globalStores';

const globalTrackIndex = trackIndex()

const isCheckTime = ref(true)
const from = ref()
const to = ref()

onMounted(() => {
    window.eventBus.on('stopTimeSelection', event => isCheckTime.value = true)
})

function selectTime(){
    window.eventBus.emit('stopBarSelection') 
   
    for(let i = 0; i < wavesurfer.length; i++){

        if (!isCheckTime.value){
            if (to.value < from.value){
                to.value = from.value
            }
            if (wavesurfer[i].regions.list){
                wavesurfer[i].clearRegions()
            }   
            var reg = wavesurfer[i].addRegion({
                start: from.value,
                end: to.value,
            })
            var reg = wavesurfer[i].enableDragSelection({
                start: from.value,
                end: to.value,
            })
            
            wavesurfer[i].on("region-updated", (region, e) => {  
                    changeBackground(trackFromStart.value[i][0])
                    globalTrackIndex.selTrackIndex = i

                    var regions = wavesurfer[i].regions.list;
                    var keys = Object.keys(regions);
                    if(keys.length > 1){
                        regions[keys[0]].remove();
                    }
                    from.value = region.start
                    to.value = region.end
            })
        }else{
            wavesurfer[i].clearRegions()
            wavesurfer[i].disableDragSelection()
        }

    }
}


</script>


<template>
    
<div :class="{deactive : isCheckTime}" >
    <input v-model="from" type="number" placeholder="from" class="input-field-nomargin w-16.1" @change="selectTime()">
    <input v-model="to" type="number" placeholder="to"  class="input-field-nomargin w-16.1 ml-1" @change="selectTime()">
    <button class="btn hover:bg-gray-300 transition mx-1" @click="isCheckTime = !isCheckTime; trimWaveform(from, to, globalTrackIndex.selTrackIndex); selectTime()">Select</button>
</div>

<button class="btn-hover" :class="{ picker : !isCheckTime}" @click=" isCheckTime=! isCheckTime; selectTime()">Select a section</button>
</template>



<style scoped>

#time-selection{
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>





