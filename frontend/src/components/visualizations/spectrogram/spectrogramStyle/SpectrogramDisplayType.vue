<script setup>
import { ref, watch } from 'vue';
import { wavesurfer } from '../../../../functions/waveform/waveform';
import { trackList } from '../../../../stores/globalStores';



const selectedValue = ref(null)
const currentTrackList = trackList()
const isLogDisplay = ref(wavesurfer[props.id].spectrogram.params.log)

watch(() =>isLogDisplay.value, () => {
    if(isLogDisplay.value){
        selectedValue.value = 'logaritmic'
    }else{
        selectedValue.value = 'linear'

    }
}, {immediate: true})

const values = ['linear', 'logaritmic']
const props = defineProps({
    id: Number
})


const changeDisplay = (e) => {
    isLogDisplay.value =! isLogDisplay.value
    currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = true
  setTimeout(() => {
    wavesurfer[props.id].spectrogram.params.log = isLogDisplay.value
    
    wavesurfer[props.id].spectrogram.init()
    currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = false
    
  }, 0);
}
</script>



<template>
<div class="box p-2 bg-white rounded-md mt-2 flex flex-col items-center">

<div>
<div v-for="value in values" :key="value">
  <input type="radio" :value="value" v-model="selectedValue" @change="changeDisplay(value)" class="cursor-pointer">
  <label class="font-bold text-xs ml-1">{{ value }}</label>
</div>
</div>

</div>



</template>