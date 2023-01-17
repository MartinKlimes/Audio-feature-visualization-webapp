<script setup>
import { Icon } from '@iconify/vue';
import { ref, onMounted } from 'vue';

import NavBar from '../components/NavBar.vue';
import AudioTrackSide from '../components/trackManager/AudioTrackSide.vue'
import UploadModal from '../components/trackManager/UploadModal.vue';
import MainPanel from '../components/MainPanel/MainPanel.vue';
import { tracklistState, uploadModalState, trackList, trackIndex } from '../globalStores';
import Waveform from '../components/Waveform.vue';
import Spectrogram from '../components/Spectrogram.vue';
import {trackFromStart} from '../Waveform.js'
import PianoRoll from '../components/PianoRoll.vue';
import { api } from '../../custom';
import { getCookie } from '../cookieHandling';

import TrackToVisualize from '../components/visualizationManager/TrackToVisualize.vue';
import WaveformSetting from '../components/VisualizationSetting/WaveformSetting.vue';
import SpectrogramSetting from '../components/VisualizationSetting/SpectrogramSetting.vue';

const trackListGlobalState = tracklistState();
const currentTrackList = trackList();
const isWaveform = ref(false)
const isSpectrogram = ref(true)
const isPianoRoll = ref(false)
const hideSettingPanel = ref(false)
const hideTracklistPanel = ref(false)
const globalTrackIndex = trackIndex()


currentTrackList.fill()


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


// function expandTracklist() {
    
//     const tracklist = document.getElementById('tracklist');
//     // const tracklistContent = document.getElementById('tracklist-content');
//     const tracklistButton = document.getElementById('arrow');
//     const addTrackBtn = document.getElementById('add-track-btn');
//     const content = document.getElementById('content');
//     const panel = document.getElementById('visualization-settings');

//     if (trackListGlobalState.tracklistExpanded) {
//         trackListGlobalState.tracklistExpanded = false;
        
//         tracklist.style.transform = 'translateX(0%)';
//         tracklist.style.transition = 'transform 0s'
//         content.style.transform = 'translateX(0rem)'
//         content.style.transition = 'transform 0s'

//         if(panel.style.transform === 'translateX(5.5rem)'){
//             content.style.width = '87.5vw'
//         }else{
//             content.style.width = '82.9vw'
            
//         }
//         // tracklistContent.style.paddingLeft = '15rem';        
//         tracklistButton.style.borderRight = '0.5rem solid black';
//         tracklistButton.style.borderLeft = '0rem'
//         // addTrackBtn.style.marginLeft = '15rem';
//     }
//     else {
//         trackListGlobalState.tracklistExpanded = true;
//         tracklist.style.transform = 'translateX(-98.5%)';
//         tracklist.style.transition = 'transform 0.4s'
//         content.style.transform = 'translateX(-15rem)'
//         content.style.transition = 'transform 0.4s'
//         tracklistButton.style.borderLeft = '0.5rem solid black'
//         tracklistButton.style.borderRight = '0rem';
    
//         if (panel.style.transform === ''){
//             content.style.width = '95vw' 
//             // alert('asfd')
//         } else {
//             content.style.width = '100vw' 
//         }
        
        
        
//         // content.style.width = '100vw' 
//         // content.style.width = currWidth + 1 + 'rem'
//         // tracklistContent.style.paddingLeft = '0%';
        
//         // addTrackBtn.style.marginLeft = '0rem'
//     }
// }
// const expandSettings = () => {
//     const panel = document.getElementById('visualization-settings');
//     const paneltButton = document.getElementById('arrow');
//     const content = document.getElementById('content');
//     const tracklist = document.getElementById('tracklist');

   

    
    
//     if(panel.style.transform === ''){
//         alert('1')
//         panel.style.transform = 'translateX(5.5rem)';
//         // content.style.transform = 'translateX(5.5rem)'
//         if(tracklist.style.transform === 'translateX(0rem)'){
//             content.style.width =  '87.5vw'
//             alert('2')
//         }else{
//             content.style.width =  '100vw'
//             alert('3')
//         }

//     }else {
//         panel.style.transform = 'translateX(0rem)';
//         // content.style.transform = 'translateX(5.5rem)'
//         content.style.width =  '82.9vw'
//     }
    // }else{
    //     if (trackListGlobalState.tracklistExpanded && panel.style.transform === 'translateX(0rem)'){

    //     }

    //     panel.style.transform = 'translateX(5.5rem)';
    //     // content.style.width =  '100vw'

    // }


// }


function openUploadModal() {
    const uploadModalGlobalState = uploadModalState();
    uploadModalGlobalState.uploadModalVisible = true;
}




</script>

<template>

<div class="min-h-full">
    <NavBar/>
    <UploadModal/>

    <div id="main-container" class="h-[calc(100vh-4.5rem)]  flex overflow-hidden relative">

        <div id="tracklist" class="w-62 h-[calc(100vh-4.5rem)]  " :class="{'transform -translate-x-[96%] border border-black' : hideTracklistPanel}">

            <div id="tracklist-divider" class="w-[97%] h-full bg-white ">
                
                <div id="tracklist-content" class="w-full h-[90%] pb-5 flex flex-col items-center gap-1 overflow-y-auto">
                    <div v-for="track in currentTrackList.selectedTracks" :key="track.id">
                        <TrackToVisualize      
                        :name="track.trackName"
                        :id="track.id"
                        />
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
            <div id="tracklist-button" class="w-[3%] h-full ">
                <button @click="hideTracklistPanel = !hideTracklistPanel" id="arrow" class="h-50 border-black" 
                :class="{' border-l-[0.5rem] border-r-[0rem]' : hideTracklistPanel, 'border-r-[0.5rem] border-l-[0rem]': !hideTracklistPanel}"></button>
            </div>

            
        </div>
        
        <div id="content" 
        class="h-full w-83vw text-xl pl-1 text-black ml-61 bg-light-800 overflow-y-auto overflow-x-hidden transform duration-400"
        :class="{'w-[87vw] pr-1' : hideSettingPanel && !hideTracklistPanel, 'w-[95.8vw] ml-0 pl-2.5 ' : hideTracklistPanel && !hideSettingPanel, 'w-[99.5vw] ml-0 pl-2' : hideTracklistPanel && hideSettingPanel}"
        >
            
            <!-- <div class="mb-7">
                
                <MainPanel 
                @showWaveform="isWaveform =! isWaveform"
                @showSpectrogram="isSpectrogram =! isSpectrogram"
                @showPianoroll ="isPianoRoll =! isPianoRoll"
                /></div> -->
            <div v-for="track in currentTrackList.trackState" :key="track.id">
                
                <transition>
                    <Waveform 
                    v-if="track.isWaveform"  
                     
                    :id="track.id"  
                    :trackname="track.trackName"/>
                </transition>
            </div>
            <!-- <div v-for="(trackname, id) in trackFromStart" :key="trackname">

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
            </div> -->
        </div>
        <!-- <div id="tracklist-button" class="w-[1%] h-full">
                <button @click="expandTracklist()" id="arrow" class="h-50"></button>
        </div> -->
        <!-- <div id="tracklist-button" class="w-[3%] h-full">
                <button @click="expandTracklist()" id="arrow-left" class="h-50"></button>
            </div> -->
        <div id="visualization-settings" 
            class="h-full w-41 absolute top-0 right-1 flex bg-gray-100 transform duration-400"
            :class="{'transform translate-x-37 border border-black' : hideSettingPanel}"
            >


            <div id="tracklist-button" class="w-[7%] h-full">
                <button @click="hideSettingPanel = ! hideSettingPanel" id="arrow-left" class="h-50 border-black"
                :class="{' border-r-[0.5rem] border-l-[0rem]' : hideSettingPanel, 'border-l-[0.5rem] border-r-[0rem]': !hideSettingPanel}"></button>
            </div>
            <div v-for="track in currentTrackList.trackState" :key="track.id">
            
                <div v-if="track.id == globalTrackIndex.selTrackIndex" class="w-[99%] border-l border-gray-300 rounded-md flex flex-col gap-1">
                    <div class="h-max w-full p-2 bg-gray-200 rounded-md border border-gray-300 flex ">
                        
                        <WaveformSetting v-if="track.isWaveform" :trackName="track.trackName" :id="track.id"/>
                    
                        
                    </div>
                    <div class="h-55 w-full p-2 bg-gray-200 rounded-md border border-gray-300 flex ">
                        
                        {{ track.trackName }}
                    
                        
                    </div>
                    <!-- <SpectrogramSetting/> -->
                    
                </div>
            </div>

        </div>
        

    </div>

</div>

</template>

<style scoped>





#tracklist{
    top: 0;
    left: 0;
    position: absolute;

    display: flex;
    flex-direction: row;
    align-items: center;
   /* transform: translateX(0rem); */

    transition: transform 0.4s;
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
    /* border-right: 0.5rem solid black; */
}
#arrow-left {
    width: 0; 
    height: 0; 
    border-top: 0.5rem solid transparent;
    border-bottom: 0.5rem solid transparent;
    /* border-left: 0.5rem solid black; */
}

#content{
    top: 0;
    left: 0;
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: left;
    /* transition: transform 0.4s;
    transition: margin-left 0.4s; */
    
}
#visualization-settings{
    /* transform: translateX(0rem); */
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