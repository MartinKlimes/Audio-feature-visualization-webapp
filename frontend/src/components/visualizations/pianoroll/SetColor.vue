<script setup>
import { onUnmounted, ref, watchEffect, watch } from 'vue';

import BlueButttons from '../../buttons/BlueButtons.vue';
import { updateRecording } from '../../../../custom';
import { setInstrumentColor } from '../../../functions/useMidiPianoroll';
import ColorsPicker from '../../visualizationManager/ColorsPicker.vue';
import { onClickOutside } from '@vueuse/core';


const props = defineProps ({
    id: Number
})

const emits = defineEmits(['closeColorPicker'])

const selectedInstrument = ref(0)
const target = ref(null);
const color = ref(null)
const colorsList = ref(null)
let instruments = []

watch(() => color.value,() =>  {
    const {uniqueInstruments, instrumentColors}  = setInstrumentColor(props.id, selectedInstrument.value, color.value)
    instruments = uniqueInstruments
    colorsList.value = instrumentColors
    color.value = null
}, {immediate: true})


// const setColor = (color) => {
//     setInstrumentColor(props.track.id, selectedInstrument.value,color)
//     props.track.pianoroll.pianorollColor[selectedInstrument.value] = color
//     updateRecording(props.track.trackName,'pianorollColor',props.track.pianoroll.pianorollColor)
// }

onClickOutside(target, () => 
{   
    setTimeout(() => {
    emits('closeColorPicker')
    
}, 0);
})

onUnmounted(() => {
    const colorsToList = Object.values(colorsList.value);
    console.log(colorsToList);

    updateRecording(props.id,'pianorollColor',colorsToList)
    
})

</script>

<template>
{{ color }}sdfd
<div class="flex mt-2 relative rounded-t bg-white justify-center items-center w-full" ref="target">
    <div class="max-w-35 overflow-x-auto flex gap-0.5 mb-2">
    <div v-for="instNum in instruments" >
       
        <BlueButttons :is-btn-clicked="instNum === selectedInstrument" @click="selectedInstrument = instNum" class="px-1 mt-2" :icon-class="'hidden'">{{instNum}}</BlueButttons>
    </div>
</div>
    <ColorsPicker class="absolute h-27 w-full top-10" :selected-color="colorsList[selectedInstrument]"  @update-color="color = $event"
    :format="'hex'"
    />

</div>





</template>