<script setup>
import { trackList } from '../../globalStores';

const currentTrackList = trackList()


const props = defineProps({
    files: Array,
    id: Number
})

const emits = defineEmits(["selectFile"]);

</script>



<template>
<div class="absolute right-1 bottom-8 w-51 h-27 bg-gray-400 border border-black rounded-md overflow-y-auto">

<div class="bg-light-blue-400 border border-black m-1 p-0.5 text-sm font-bold rounded-md hover hover:border-gray-400 cursor-pointer shadow-md shadow-gray-700" :class="{'shadow-inner shadow-dark-500 bg-light-blue-300 hover:border-black' : currentTrackList.selectTrack(id).txtFileName == file || currentTrackList.selectTrack(id).MIDIFileName == file}" v-for="file in files" @click="$emit('selectFile', file)">

    {{ file }}

</div>



</div>





</template>