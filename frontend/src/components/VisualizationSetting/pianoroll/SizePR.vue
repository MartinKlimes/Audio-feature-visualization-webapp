<script setup>
import BlueButttons from '../../buttons/BlueButttons.vue';
import { ref } from 'vue';
import { trackList } from '../../../globalStores';
import {createVerticalKeyboard} from '../../../functions/useMidiPianoroll'
import {updateRecording} from '../../../../custom'

const currentTrackList = trackList()

const props = defineProps({
    id: Number,
    trackName: String
})

const emits = defineEmits(['close'])

const size = ref(500)

const setSize = () => {
    currentTrackList.selectTrack(props.id).pianoroll.pianorollHeight = size.value

    updateRecording(props.trackName,'pianorollHeight', size.value)

    // emits('close')
    // const pianoroll = document.getElementById(`pianoroll-${props.id}`)
    // createVerticalKeyboard(pianoroll,size.value )
    // pianoroll.config = {noteHeight: 20}
    // var svg = pianoroll.getElementsByTagName('div')[2].getElementsByTagName('svg')[0];
    // console.log(svg);

}




</script>



<template>


<div class="bg-yellow-200 border border-black rounded-md py-1 flex flex-col items-center">
    <h1>Set Element Size</h1>

      <!-- <label for="size">Size:</label> -->
    <input type="range" v-model="size" min="200" max="1000" step="100" id="size" />
    <span>{{ size }}px</span>
    

    <BlueButttons :is-btn-clicked="loading" :icon="(loading ? 'fa:spinner' : '')" :icon-class="(loading ? 'spin' : 'hidden')" 
    @click="setSize(size)" :disabled="loading" class="mt-1">Set Size</BlueButttons>
    
  </div>





</template>