<script setup>
import { onMounted, ref } from 'vue';
import { ColorPicker } from 'vue-accessible-color-picker';
import BlueButttons from '../../buttons/BlueButttons.vue';
import { updateRecording } from '../../../../custom';
import { setInstrumentColor } from '../../../functions/useMidiPianoroll';
import ColorsPicker from '../../visualizationManager/ColorsPicker.vue';
import { onClickOutside } from '@vueuse/core';

const props = defineProps ({
    track: Object
})
const emits = defineEmits(['closeColorPicker'])


const instrumentsUnique  = ref(setInstrumentColor(props.track.id))
const selectedInstrument = ref(0)
const selectedColor = ref(null)
const target = ref(null);


let colorList = []
if (props.track.pianoroll.pianorollColor) {
    colorList = props.track.pianoroll.pianorollColor.slice(1, -1).split(',').map(color => color.replace(/"/g, ''))
}

const setColor = (color) => {
    setInstrumentColor(props.track.id, selectedInstrument.value,color)
    colorList[selectedInstrument.value] = color
    updateRecording(props.track.trackName,'pianorollColor',colorList)
}

onClickOutside(target, () => 
{   setTimeout(() => {
    emits('closeColorPicker')
    
}, 0);
})

const selectColor = () => {
    selectedColor.value = colorList[selectedInstrument.value]
}
</script>

<template>

<div class="flex mt-2 relative rounded-t bg-white justify-center items-center w-full" ref="target">
    <div class="max-w-35 overflow-x-auto flex gap-0.5 mb-2">
    <div v-for="instNum in instrumentsUnique" >
       
        <BlueButttons :is-btn-clicked="instNum === selectedInstrument" @click="selectedInstrument = instNum, selectColor()" class="px-1 mt-2" :icon-class="'hidden'">{{instNum}}</BlueButttons>
    </div>
</div>
    <ColorsPicker class="absolute h-27 w-full top-10" :selected-color="selectedColor"  @update-color="setColor($event),  selectColor()"
    :format="'hex'"
    />

</div>





</template>