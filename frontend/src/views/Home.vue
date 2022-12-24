<script setup>
import { Icon } from '@iconify/vue';
import { ref, onMounted } from 'vue';
import NavBar from '../components/NavBar.vue';
import AudioTrackSide from '../components/AudioTrackSide.vue'
import UploadModal from '../components/UploadModal.vue';
import MainPanel from '../components/MainPanel.vue';
import { tracklistState, uploadModalState, trackList } from '../globalStores';
import Waveform from '../components/Waveform.vue';
import Spectrogram from '../components/Spectrogram.vue';
import { getTrackList } from '../filesFunctions'
import {trackFromStart} from '../Waveform.js'
import PianoRoll from '../components/PianoRoll.vue';
import { api } from '../../custom';
import { getCookie } from '../cookieHandling';

const trackListGlobalState = tracklistState();
const currentTrackList = trackList();
const isWaveform = ref(true)
const isSpectrogram = ref(false)
const isPianoRoll = ref(false)

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

<div id="home-layout">
    <NavBar/>
    <UploadModal/>
    

    <div id="main-container" class="h-[calc(100vh-4.5rem)]">


        <div id="tracklist" class="w-120 h-[calc(100vh-4.5rem)] mt-14">

            <div id="tracklist-divider" class="w-[97%] h-full bg-white ">
                
                <div id="tracklist-content" class="w-full h-[90%] pl-60 pt-5 pb-5">
                    <AudioTrackSide/>
                    

                </div>
                
                <div id="add-track-div" class="w-full h-[10%]">
                    <button @click="openUploadModal()" id="add-track-btn" class="btn btn-blue ml-60">Add tracks</button>
                </div>
            
            </div>
            
            <div id="tracklist-button" class="w-[3%] h-full">
                <button @click="expandTracklist()" id="arrow" class="h-50"></button>
            </div>
            
        </div>

        <div id="content" class="h-full w-full text-xl p-3 text-black ml-56 bg-light-300 overflow-hidden">
            <div class="mb-7">
                
                <MainPanel 
                @showWaveform="isWaveform =! isWaveform"
                @showSpectrogram="isSpectrogram =! isSpectrogram"
                @showPianoroll ="isPianoRoll =! isPianoRoll"
                /></div>
                
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


#home-layout {
    min-height: 100vh;
}

#main-container{
    display: flex;
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
    display: flex;
    align-items: center;
    flex-direction: column;

    gap: 0.25rem;

    transition: padding-left 0.2s;
    overflow-y: scroll;
    overflow-x: hidden;
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