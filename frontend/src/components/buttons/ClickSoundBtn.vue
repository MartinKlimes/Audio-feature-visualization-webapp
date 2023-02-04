<script setup>
import { Icon } from '@iconify/vue';
import { ref } from 'vue';
import SelectFiles from './SelectFiles.vue';
import { wavesurfer } from '../../functions/waveform';


let clickOnBarLineIndex = 0
let clickSoundList = ['Sound1.mp3','Sound2.mp3','Sound3.mp3','Sound4.mp3']

const selectSoundClick = ref(false)
const selectedClickSound = ref(new Audio('Sound2.mp3'))
const playSoundClick = ref(false)


const props = defineProps({
    id: Number,
    backgroundColor: String,
    markersList: String
    
})



const playSoundOnMarker = () => {
    wavesurfer[props.id].on('interaction', function () {
        clickOnBarLineIndex = 0
    });

    wavesurfer[props.id].backend.on('audioprocess',clickSound)

}
const muteSoundOnMarker = () => {
    wavesurfer[props.id].backend.un('audioprocess',clickSound)
}

const clickSound = (id) => {

    if (wavesurfer[props.id].isPlaying()) {        
        if (id > props.markersList[clickOnBarLineIndex]){
            selectedClickSound.value.play()
            clickOnBarLineIndex +=1
        }
    }
}

const selectClickSound = (event) => {
    selectedClickSound.value = new Audio(clickSoundList[clickSoundList.indexOf(event)]) 
    selectedClickSound.value.volume = 1
    selectedClickSound.value.play()
}

</script>

<template>
<div>
    <div class="absolute -right-1 top-1 ">
        <Icon v-if="!playSoundClick" @click="playSoundOnMarker(), playSoundClick =! playSoundClick" icon="clarity:volume-mute-line" class="rounded-md hover:opacity-80  p-0.5 cursor-pointer" width="20" :class="backgroundColor"  />
        <Icon v-if="playSoundClick" @click="muteSoundOnMarker(), playSoundClick =! playSoundClick" icon="clarity:volume-up-line" class="p-0.5 rounded-md shadow-inner shadow-dark-500 cursor-pointer" width="20" :class="backgroundColor"  />
        <Icon icon="material-symbols:arrow-right"  class="text-lg  cursor-pointer rounded-md hover:opacity-60 " @click="selectSoundClick =! selectSoundClick" :class="{'opacity-60 shadow-inner shadow-dark-400' : selectSoundClick}"/>
        
    </div>

    
    <SelectFiles  v-if="selectSoundClick" :files="clickSoundList" :id="id" @select-file="selectClickSound($event)" class="-mr-0.5 z-10"/>

</div>

</template>


<style scoped>
.sound-enter-active,
.sound-leave-active {
    transition: all 0.1s ease-out;
   
}

.sound-enter-from,
.sound-leave-to {
    transform: translateX(-20px);
  opacity: 0;
}



</style>