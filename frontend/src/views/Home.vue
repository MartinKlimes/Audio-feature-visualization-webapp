<script setup>
import { Icon } from '@iconify/vue';
import { ref, onBeforeMount, onMounted } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import NavBar from '../components/NavBar.vue';
import AudioTrackSide from '../components/trackManager/AudioTrackSide.vue'
import UploadModal from '../components/trackManager/UploadModal.vue';
import MainPanel from '../components/MainPanel/MainPanel.vue';
import { tracklistState, uploadModalState, trackList } from '../globalStores';
import Waveform from '../components/Waveform.vue';
import Spectrogram from '../components/Spectrogram.vue';

import {trackFromStart} from '../Waveform.js'
import PianoRoll from '../components/PianoRoll.vue';
import { api } from '../../custom';
import { getCookie } from '../cookieHandling';
import Draggable from '../components/Draggable.vue';

const trackListGlobalState = tracklistState();
const currentTrackList = trackList();
const isWaveform = ref(true)
const isSpectrogram = ref(true)
const isPianoRoll = ref(false)

onBeforeMount(() => {
    currentTrackList.getTrackList()
})

onBeforeRouteLeave((to, from) => {
      const answer = window.confirm(
        'Do you really want to leave? you have unsaved changes!'
      )
      // cancel the navigation and stay on the same page
      if (!answer) return false
})

const axiosConfig = {
    headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        'Content-Type': 'multipart/form-data',     
    },
}

 const trackname = 'tap.mp3'
// fetch('http://127.0.0.1:5000/test/' + trackname)
// .then(response => {
//     console.log(response)
// })


// const xhr = new XMLHttpRequest();
// xhr.open('GET', 'http://127.0.0.1:5000/test/' + trackname, true);
// xhr.withCredentials = true;
// xhr.send(null);

// api.get('/test/' + trackname)
// .then(response => {
//     console.log(response)
// })


function expandTracklist() {
    
    const tracklist = document.getElementById('tracklist');
    const tracklistContent = document.getElementById('tracklist-content');
    const tracklistButton = document.getElementById('arrow');
    const addTrackBtn = document.getElementById('add-track-btn');

    if (trackListGlobalState.tracklistExpanded) {
        trackListGlobalState.tracklistExpanded = false;
        tracklist.style.transform = 'translateX(-50%)';
        tracklistContent.style.paddingLeft = '15rem';        
        tracklistButton.style.borderLeft = '0.5rem solid black';
        tracklistButton.style.borderRight = '0rem'
        addTrackBtn.style.marginLeft = '15rem';
    }
    else {
        trackListGlobalState.tracklistExpanded = true;
        
        tracklist.style.transform = 'translateX(-0%)';
        tracklistContent.style.paddingLeft = '0%';
        tracklistButton.style.borderRight = '0.5rem solid black'
        tracklistButton.style.borderLeft = '0rem';
        addTrackBtn.style.marginLeft = '0rem'
    }
}


function openUploadModal() {
    const uploadModalGlobalState = uploadModalState();
    uploadModalGlobalState.uploadModalVisible = true;
}




</script>

<template>

<div class="min-h-screen">
    <NavBar/>
    <UploadModal/>

    <div id="main-container" class="h-[calc(100vh-4.5rem)] flex">

        <div id="tracklist" class="w-128 h-[calc(100vh-4.5rem)] mt-14 ">

            <div id="tracklist-divider" class="w-[97%] h-full bg-white ">
                
                <div id="tracklist-content" class="w-full h-[90%] pl-60 pt-3 pb-5 flex flex-col items-center gap-1">
                    
                    <div class=" h-55 w-[85%] ml-7 px-2 py-1 flex-col justify-center bg-light-700  border-2 border-gray-300  rounded-md">
                        <div class="flex justify-center items-center relative">
                            <span class="font-bold font-serif text-gray-500 text-sm">Chopin_ukázka_014</span>
                            <div class="w-4 h-4 bg-gray-100 border border-gray-400 hover:bg-gray-400 duration-200 rounded-sm absolute right-0 cursor-pointer" title="Select"></div>
                        </div>
                        <div class="mt-4 player-buttons h-7 w-full bg-gray-400 flex items-center justify-between px-2 rounded-md">
                            <Icon icon="material-symbols:volume-up-outline" width="20" />
                            <input type="range" class="slider appearance-none  rounded-lg cursor-pointer w-28">
                            <div class="inline-flex rounded-md shadow-sm bg-gray-600 text-white " >
                                <button class="w-5 text-sm border-r border-gray-400 rounded-l-md hover:bg-gray-300 hover:text-gray-800 duration-200 ">M</button>
                                <button class="w-5 text-sm rounded-r-md hover:bg-gray-300 hover:text-gray-800 duration-200 ">S</button>

                            </div>

                        </div>
                        
                        <div class="h-[47%] w-full mt-5 p-2 border border-dashed border-gray-500 rounded-md ">
                            <div class="grid grid-cols-2 gap-2">
                                <button class="btn-hover-cursor font-semibold w-22 shadow-sm shadow-dark-100">Waveform</button>
                                <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Spectrogram</button>
                                <button class="btn-hover-cursor  w-22 font-semibold shadow-sm shadow-dark-100">Pianoroll</button>
                                <div class="flex w-22 h-max">
                                    <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-r-none">IOI</button>
                                    <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-l-none">IBI</button>
                                </div>
        
                                <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Tempo</button>
                                <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">RMS</button>

                            

                            </div>
                        </div>
                        <Icon icon="ph:files" width="18" class="w-8 float-right mt-2 shadow-sm shadow-gray-500 rounded-md hover:bg-gray-300 cursor-pointer"/>
                    </div>
                    <!-- <div class="flex w-full h-[10%] border border-gray-500 mt-5 ">
                        <button class="btn">Bars</button>

                    </div> -->

                    <AudioTrackSide/>
                    

                </div>
                
                <div id="add-track-div" class="w-full h-[10%]">
                    <button @click="openUploadModal()" id="add-track-btn" class="btn btn-blue ml-60">Add tracks</button>
                </div>
            
            </div>
            
            <div id="tracklist-button" class="w-[1%] h-full">
                <button @click="expandTracklist()" id="arrow" class="h-50"></button>
            </div>
            
        </div>

        <div id="content" class="h-full w-full text-xl p-3 text-black ml-60 bg-light-300 overflow-hidden">
            <!-- <div class="mb-7">
                
                <MainPanel 
                @showWaveform="isWaveform =! isWaveform"
                @showSpectrogram="isSpectrogram =! isSpectrogram"
                @showPianoroll ="isPianoRoll =! isPianoRoll"
                /></div> -->
                
            <div v-for="(trackname, id) in trackFromStart" :key="trackname">

                <transition>
                    <Waveform 
                    v-show="isWaveform"  
                    :id="id"  
                    :trackname="trackname"/>
                </transition>

                <canvas :id="`myChart-${id}`" class="hidden" width="100%" height="200"></canvas>
                

                <transition>
                    <Spectrogram
                    v-show="isSpectrogram"
                    :id="id"
                    :trackname="trackname"/>
                </transition>

                <transition>
                    <PianoRoll
                    v-show="isPianoRoll"
                    :id="id"
                    :trackname="trackname"/>
                </transition>

            </div> 


        </div>
        

    </div>

</div>

</template>

<style scoped>

input[type=range]{
    -webkit-appearance: none;
}

input[type=range]::-webkit-slider-runnable-track {
    width: 300px;
    height: 5px;
    background: #ddd;
    border: none;
    border-radius: 3px;
}

input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    border: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: rgb(63, 63, 63);
    margin-top: -4px;
}

input[type=range]:focus {
    outline: none;
}

input[type=range]:focus::-webkit-slider-runnable-track {
    background: #ccc;
}



#tracklist{
    top: 0;
    position: absolute;

    display: flex;
    flex-direction: row;
    align-items: center;
    transform: translateX(-50%);

    transition: transform 0.2s;
    z-index:21;
    
}

#tracklist-content{
    /* display: flex;
    align-items: center;
    flex-direction: column; 

    gap: 0.25rem;*/

    transition: padding-left 0.2s;
    /* overflow-y: scroll;
    overflow-x: hidden; */
}


#tracklist-button{
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
}

#arrow {
    width: 0; 
    height: 0; 
    border-top: 0.5rem solid transparent;
    border-bottom: 0.5rem solid transparent;
    border-left: 0.5rem solid black;
}

#content{
    display: flex;
    flex-direction: column;
    align-items: left;
    overflow-y: scroll;
}

#add-track-div{
    display: flex;
    align-items: center;
    justify-content: center;
}

#add-track-btn{
    transition: margin-left 0.2s;
}

#add-files-btn{
    float: right;
}
.controls{
    width: 100;
    margin-right: auto;
    display: flex;
    align-items: center;
    cursor: pointer;
}
.v-enter-active,
.v-leave-active {
    transition: all 0.2s;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: scale(0.75);
}




</style>