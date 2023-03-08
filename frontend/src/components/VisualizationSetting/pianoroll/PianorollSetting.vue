<script setup>
import { ref, onMounted } from 'vue';
import BlueButttons from '../../buttons/BlueButttons.vue';

import SetColor from './SetColor.vue'
import { Icon } from '@iconify/vue';
import { updateRecording } from '../../../../custom';
import SizeSize from './SizeSize.vue';
const sizeSet = ref(false)
const setColor = ref(false)
const props = defineProps({
    track: Object
})



const noteNamesHide = () => {
    props.track.pianoroll.dynamicNames = false
    setTimeout(() => {
        const noteNames = document.querySelectorAll(`#keyboard-${props.track.id} div #noteName`);
    
        noteNames.forEach(noteName => {     
            noteName.classList.toggle('hidden');
        }); 
    },0);
}
const keyboardSwitch = () => {
    document.querySelector(`#keyboard-${props.track.id}`).classList.toggle('hidden');

}

const removePianoroll = () => {
    props.track.pianoroll.isPianoroll = false
    props.track.pianoroll.isPianorollDisplayed = false
    updateRecording(props.track.trackName,'isPianoroll', false)
    updateRecording(props.track.trackName,'isPianorollDisplayed', false)

}
</script>



<template>
<div class=" flex flex-col items-center relative ">
    <BlueButttons @click="sizeSet = !sizeSet" class="px-2" :icon-class="'hidden'">Size</BlueButttons>
    <Transition>
        <SizeSize :track="track" v-if="sizeSet" @close-size-setter="sizeSet = false"/>
    </Transition>

    <BlueButttons :is-btn-clicked="setColor"  @click="setColor = !setColor" class="px-2 mt-2" :icon-class="'hidden'">Set color</BlueButttons>
    <Transition>
        <SetColor :track="track"  v-if="setColor" @close-color-picker="setColor = false"/>
    </Transition>

    <BlueButttons  @click="noteNamesHide" class="px-2 mt-2" :icon-class="'hidden'">noteNames</BlueButttons>
    <BlueButttons :is-btn-clicked="track.pianoroll.dynamicNames" @click="track.pianoroll.dynamicNames =!  track.pianoroll.dynamicNames" class="px-2 mt-2" :icon-class="'hidden'">dynamicNames</BlueButttons>
    <BlueButttons @click="keyboardSwitch" class="px-2 mt-2" :icon-class="'hidden'">keyboard</BlueButttons>

    <button title="Delete pianoroll" class="mt-4 opacity-50 hover:opacity-100  " @click="removePianoroll"> <Icon icon="mingcute:delete-2-line" /> </button>
    <!-- <button @click="changeInstColor">změn</button> -->
</div>
    









</template>