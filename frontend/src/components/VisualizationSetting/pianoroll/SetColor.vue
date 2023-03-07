<script setup>
import { onMounted, ref, onUnmounted } from 'vue';
import { ColorPicker } from 'vue-accessible-color-picker';
import BlueButttons from '../../buttons/BlueButttons.vue';
import { updateRecording } from '../../../../custom';
import { setInstrumentColor } from '../../../functions/useMidiPianoroll';
const props = defineProps ({
    track: Object
})
const instrumentsUnique  = ref(setInstrumentColor(props.track.id))
const selectedInstrument = ref(null)
let colorList = []
if (props.track.pianoroll.pianorollColor) {
    colorList = props.track.pianoroll.pianorollColor.slice(1, -1).split(',').map(color => color.replace(/"/g, ''))
}

const setColor = (color) => {
    setInstrumentColor(props.track.id, selectedInstrument.value,color)
    props.track.pianoroll.pianorollColor = []
    colorList[selectedInstrument.value] = color
    props.track.pianoroll.pianorollColor = colorList
    updateRecording(props.track.trackName,'pianorollColor',colorList)
}


</script>

<template>

<div class="flex overflow-x-auto bg-white">
    
    <ColorPicker @color-change="setColor($event.cssColor)" class= " absolute -right-3 -left-3 top-26 right-0 overflow-hidden max-h-60 rounded-md " alpha-channel="hide"  />
    
    <div v-for="istNum in instrumentsUnique">
        <BlueButttons :is-btn-clicked="istNum === selectedInstrument" @click="selectedInstrument = istNum" class="px-1 mt-2" :icon-class="'hidden'">{{istNum}}</BlueButttons>
    </div>

</div>





</template>