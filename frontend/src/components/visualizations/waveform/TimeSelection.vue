<script setup>
import { ref, onMounted, onDeactivated, onActivated } from 'vue';
import { wavesurfer} from '../../../functions/waveform';
import BlueButttons from '../../buttons/BlueButttons.vue';

const from = ref()
const to = ref()

const props = defineProps({
    id: Number,
    trackName: String,
    loading: Boolean
})
const emits = defineEmits(['trim-audio'])

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

</script>

<template>

<div class="flex flex-col items-center ">
    <div class="flex mt-1  rounded-md">
    <input v-model="from" type="number" placeholder="from" class="input-field-nomargin w-15 border-2 border-blue-400" @change="selectTime()">
    <input v-model="to" type="number" placeholder="to"  class="input-field-nomargin w-15 ml-1 border-2 border-blue-400" @change="selectTime()">
    </div>
    <BlueButttons :is-btn-clicked="loading" :icon="(loading ? 'fa:spinner' : '')" :icon-class="(loading ? 'spin' : 'hidden')" @click="$emit('trim-audio', [from, to])" :disabled="loading" class="mt-1 px-2">Select</BlueButttons>

</div>

</template>







