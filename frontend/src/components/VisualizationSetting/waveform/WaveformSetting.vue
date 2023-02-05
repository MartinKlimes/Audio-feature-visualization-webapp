<script setup>
import { Icon } from '@iconify/vue';
import { ref, shallowRef } from 'vue';
import BarSelection from './BarSelection.vue';
import TimeSelection from './TimeSelection.vue';
import { wavesurfer, marker } from '../../../functions/waveform';
import { api } from '../../../../custom';
import { trackIndex, trackList } from '../../../globalStores';
import { showAlert, closeAlert } from '../../../alerts';
import { ColorPicker } from 'vue-accessible-color-picker'
import BlueButtons from '../../buttons/BlueButttons.vue'
import ClickSoundBtn from '../../buttons/ClickSoundBtn.vue';
import { createWavesurfer } from '../../../functions/waveform';

const currentSetting = shallowRef()
const loading = ref(false)
const currentTrackList = trackList()
const showColorPicker = ref(false)
const isBtnClicked = ref(false)
const bars = ref()
const setWaveformColor = ref('setProgressColor')
const splitChannelsStatus = ref(false)

const props = defineProps({
    track: Object,
})

const removeWaveform = () => {
    wavesurfer[props.track.id].destroy()
    props.track.isWaveform = false
    props.track.isWaveformDisplayed = false
    api.get("/change-track-status/isWaveform/" + props.track.trackName + "/''")
    api.get("/change-track-status/isWaveformDisplayed/" + props.track.trackName + "/''")
}

const showBars = () => {
    if(!props.track.txtFileName){
        showAlert('First select the text file!');
        setTimeout(closeAlert, 1500);
    } else {
        if(wavesurfer[props.track.id].markers.markers.length > 0) {
            isBtnClicked.value = false
            currentSetting.value = ''
            wavesurfer[props.track.id].clearRegions()
            wavesurfer[props.track.id].clearMarkers()
        } else {
            api.get('/get-file/' + props.track.txtFileName)
              .then((response) => {
             
                isBtnClicked.value = true
                bars.value = response.data.split('\n');
                console.log(bars);
              
                marker(response.data.split('\n'), props.track.id);
              }
            )
        }
    }
}
const showBarsToSelect = () => {
    if(!isBtnClicked.value){
        
        showBars()
    }
    if(props.track.txtFileName){

        currentSetting.value === BarSelection ? currentSetting.value = '' : currentSetting.value = BarSelection
    }
}

const trimAudio = (event) => {

    loading.value = true
    api.get('/trim-audio/' + props.track.trackName + '/' + event[0] + '/' + event[1] + '/' + event[2] + '/' + event[3])
    .then((response) => {
        // console.log(response.data);
        currentTrackList.fill()
        loading.value=false
    })

}
const changeColorStatus = () => {
    // console.log([wavesurfer[props.track.id].getProgressColor(), wavesurfer[props.track.id].getWaveColor()]);
    api.get("/change-track-status/waveformColor/" + props.track.trackName + "/" + [wavesurfer[props.track.id].getProgressColor(), wavesurfer[props.track.id].getWaveColor(), splitChannelsStatus.value])
    
}

const splitChannels = () => {
    props.track.splitChannels = !props.track.splitChannels
    props.track.isWaveform = false
    api.get("/change-track-status/splitChannels/" + props.track.trackName + "/''")
    setTimeout(() => {
        props.track.isWaveform = true
    }, 500);
}

</script>

<template>
<div class=" flex flex-col items-center relative">
    <Icon  class="absolute -left-1 -top-1 rounded"  :class="track.backgroundColor" icon="mdi:waveform" />

    <BlueButtons @click="showBars" :is-btn-clicked="isBtnClicked" :icon="(isBtnClicked ? 'mdi:eye-outline' : 'mdi:eye-off-outline')" @mouseover="track.showFileInfo=true" @mouseleave="track.showFileInfo=false"  :class="{'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-transparent'  : !track.txtFileName}">Bars</BlueButtons>

    <button v-if="!isBtnClicked" class="absolute top-0 right-0 opacity-50 hover:opacity-100"><Icon icon="entypo:export" @click="wavesurfer[track.id].exportImage()"/></button>

    <ClickSoundBtn v-if="isBtnClicked" :id="track.id" :backgroundColor="track.backgroundColor" :markers-list="bars"/>

    <Transition>
        <div v-if="track.showFileInfo && track.txtFileName" class="absolute bg-blue-300 z-1 rounded-md  text-xs px-1 py-0.5 shadow-inner shadow-gray-500 mt-9 ">{{track.txtFileName}}</div>
    </Transition>

    <span class="text-xs opacity-50 mt-3" >Select part</span>
    <div class="flex  border border-dashed border-gray-400 rounded-md p-1 justify-center items-center " >

        <BlueButtons class="mr-1"  @click="showBarsToSelect()"  :class="{'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-transparent'  : !track.txtFileName}"  :icon="'material-symbols:content-cut-rounded'" :is-btn-clicked="currentSetting === BarSelection">Bars</BlueButtons>
        <BlueButtons @click="currentSetting === TimeSelection ? currentSetting = '' : currentSetting = TimeSelection" :icon="'material-symbols:content-cut-rounded'" :is-btn-clicked="currentSetting === TimeSelection">Time</BlueButtons>
        
    </div>
    <transition>
        <KeepAlive>
            <component :is="currentSetting" :trackName="track.trackName" :id="track.id" :loading="loading" @trim-audio="trimAudio($event)"/>
        </KeepAlive>
    </transition>

    <BlueButtons :icon="'ic:outline-color-lens'" @click="showColorPicker =! showColorPicker, changeColorStatus()" :is-btn-clicked="showColorPicker" class="mt-3">Color</BlueButtons>

    <BlueButtons title="Split channels" class="mt-3 items-center opacity-90 " :is-btn-clicked="track.splitChannels" @click="splitChannels()" :icon-class="'ml-0 '" :rotate="1"  :icon="'carbon:split-screen'"></BlueButtons>

    <button title="reload waveform" class="mt-4 opacity-50 hover:opacity-100 absolute right-0 -bottom-2" @click="removeWaveform"> <Icon icon="mingcute:delete-2-line" /> </button>

        <Transition>
    <div v-if="showColorPicker"  class="flex flex-col w-10 p-1  rounded-md gap-1 bg-white absolute z-5 -bottom-51 -right-2">
        <BlueButtons :icon="'material-symbols:line-end-arrow-notch'" class="items-center justify-center h-4" 
        :is-btn-clicked="setWaveformColor == 'setProgressColor'" 
        @click="setWaveformColor = 'setProgressColor'"></BlueButtons>

        <BlueButtons :icon="'material-symbols:line-start-arrow-notch'"  class="items-center justify-center h-4 " 
        :is-btn-clicked="setWaveformColor == 'setWaveColor'" 
        @click="setWaveformColor = 'setWaveColor'"></BlueButtons>
    </div>
    </Transition>

    <Transition>
        <ColorPicker v-if="showColorPicker"  @color-change="setWaveformColor == 'setProgressColor' ? wavesurfer[track.id].setProgressColor($event.cssColor) : wavesurfer[track.id].setWaveColor($event.cssColor)" class= " absolute -right-3 -left-3 top-35 right-0 overflow-hidden max-h-60 rounded-md " :class="track.backgroundColor" alpha-channel="hide"  />
    </Transition>

  





   
</div>



</template>

