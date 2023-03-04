<script setup>
import { onMounted, ref } from 'vue';
import { ColorPicker } from 'vue-accessible-color-picker';


const props = defineProps ({
    id: Number
})

const instruments  = ref(null)
onMounted(() => {

const svgElements = document.querySelector(`#pianoroll-${props.id} div:nth-of-type(3) svg`)
const notes = Array.from(svgElements.querySelectorAll('.note'));
instruments.value = Array.from(new Set(notes.map(note => Number(note.getAttributeNS(null, 'data-instrument')))));

})

</script>





<template>
<div>
    {{ instruments }}
    <ColorPicker @color-change="setWaveformColor == 'setProgressColor' ? wavesurfer[track.id].setProgressColor($event.cssColor) : wavesurfer[track.id].setWaveColor($event.cssColor)" class= " absolute -right-3 -left-3 top-35 right-0 overflow-hidden max-h-60 rounded-md " alpha-channel="hide"  />

</div>





</template>