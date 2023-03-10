<script setup>
import BlueButttons from '../../buttons/BlueButttons.vue';
import { ref } from 'vue';
import {updateRecording} from '../../../../custom'
import { onClickOutside } from '@vueuse/core';

const props = defineProps({
    track: Object
})
const emits = defineEmits(['closeSizeSetter'])

const size = ref(props.track.pianoroll.pianorollHeight )
const target = ref(null)

const setSize = () => {
    props.track.pianoroll.pianorollHeight = size.value
    updateRecording(props.track.id,'pianorollHeight', size.value)

}
onClickOutside(target, () => 
{   setTimeout(() => {
    emits('closeSizeSetter')
    
}, 0);
})
</script>



<template>


<div class="bg-yellow-200 border border-black rounded-md py-1 flex flex-col items-center" ref="target">
    <h1>Set Element Size</h1>

      <!-- <label for="size">Size:</label> -->
    <input type="range" @change="setSize(size)" v-model="size" min="200" max="1000" step="100" id="size" />
    <span>{{ size }}px</span>
    

    <BlueButttons :is-btn-clicked="loading" :icon="(loading ? 'fa:spinner' : '')" :icon-class="(loading ? 'spin' : 'hidden')" 
     :disabled="loading" class="mt-1">Set Size</BlueButttons>
    
  </div>





</template>