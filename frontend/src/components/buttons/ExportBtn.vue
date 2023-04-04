<script setup>
import BlueButtons from './BlueButtons.vue';
import { Icon } from '@iconify/vue';
import { ref } from 'vue';
import { wavesurfer } from '../../functions/waveform';
import html2canvas from 'html2canvas';

const props = defineProps({
    id: Number,
    visualization: String,
    trackName: String,
})

const exportingPNG = ref(false)


const saveImage = () => {
    exportingPNG.value = true
    wavesurfer[props.id].zoom(0)
    const divToExport = document.getElementById(`${props.visualization}-${props.id}`);
    
    if(props.visualization === 'spectrogram'){
        wavesurfer[props.id].spectrogram.init()
    }
    
    setTimeout(() => {
      html2canvas(divToExport).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const img = new Image();
        img.src = imgData;
        const a = document.createElement('a');
        a.href = imgData;
        a.download = `${props.trackName}-${props.visualization}.png`
        a.click();
      });
    wavesurfer[props.id].zoom(20)
    if(props.visualization === 'spectrogram'){
        wavesurfer[props.id].spectrogram.init()
    }
    exportingPNG.value = false

    }, 100);
    
}


</script>




<template>
    <!-- <BlueButtons
    :icon="exportingPNG ? 'fa:spinner' : 'entypo:export' " 
    :class="{'spin' : exportingPNG}" 
    :icon-class="'ml-0'"
    @click="saveImage" 
    ></BlueButtons> -->
<button  class="opacity-60 hover:opacity-100 ">
      <Icon :icon="exportingPNG ? 'fa:spinner' : 'entypo:export' " :class="{'spin' : exportingPNG}" @click="saveImage" />
</button>



</template>