<script setup>
import { ref } from 'vue';
import BlueButttons from '../../buttons/BlueButttons.vue';
import SizePR from './SizePR.vue'
import SetColor from './SetColor.vue'




const sizeSet = ref(false)
const setColor = ref(false)
const props = defineProps({
    track: Object
})

const color = 'red'
const numberOfInstrument = 2

// const pianoroll = document.getElementById(`pianoroll-${props.track.id}`)
// var svg = pianoroll.getElementsByTagName('div')[2].getElementsByTagName('svg')[0];
// const notes = Array.from(svg.querySelectorAll('.note'));
// const instruments = notes.map(note => Number(note.getAttributeNS(null, 'data-instrument')))

// const changeInstColor = () => {
//     notes.forEach((element, id) => {
//         if(instruments[id] == numberOfInstrument){
//             element.setAttributeNS(null, 'fill', color)
//         }
//     })
// }


const noteNamesSwitch = () => {
    const noteNames = document.querySelectorAll(`#keyboard-${props.track.id} div #noteName`);

    noteNames.forEach(noteName => {     
        noteName.classList.toggle('hidden');
    });
}
const keyboardSwitch = () => {
    document.querySelector(`#keyboard-${props.track.id}`).classList.toggle('hidden');

}
</script>



<template>
<div class=" flex flex-col items-center relative">

    <BlueButttons @click="sizeSet = !sizeSet" class="px-2" :icon-class="'hidden'">Size</BlueButttons>
    <Transition>
        <SizePR :id="track.id" :trackName="track.trackName" v-if="sizeSet" @close="sizeSet = false"/>
    </Transition>

    <BlueButttons @click="setColor = !setColor" class="px-2 mt-2" :icon-class="'hidden'">Set color</BlueButttons>
    <Transition>
        <SetColor :id="track.id" v-if="setColor"/>
    </Transition>

    <BlueButttons @click="noteNamesSwitch" class="px-2 mt-2" :icon-class="'hidden'">noteNames</BlueButttons>
    <BlueButttons @click="keyboardSwitch" class="px-2 mt-2" :icon-class="'hidden'">keyboard</BlueButttons>
    
    <!-- <button @click="changeInstColor">změn</button> -->
</div>
    









</template>