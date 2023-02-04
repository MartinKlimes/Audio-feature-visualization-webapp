<script setup>
import { ref } from 'vue';
import NavBar from '../components/MainPanel/NavBar.vue';
import AudioTrackSide from '../components/trackManager/AudioTrackSide.vue'
import UploadModal from '../components/trackManager/UploadModal.vue';
import { tracklistState, uploadModalState, trackList, trackIndex } from '../globalStores';
import Waveform from '../components/Waveform.vue';
import { getCookie } from '../cookieHandling';

import TrackToVisualize from '../components/visualizationManager/TrackToVisualize.vue';
import RightPanel from '../components/RightPanel.vue';

const currentTrackList = trackList();

const hideSettingPanel = ref(false)
const hideTracklistPanel = ref(false)
const globalTrackIndex = trackIndex()
const uploadModalVisible = ref(false)

currentTrackList.fill()


const axiosConfig = {
    headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        'Content-Type': 'multipart/form-data',     
    },
}


</script>

<template>

<div class="min-h-full">
    <NavBar @open-upload-modal="uploadModalVisible = true" :uploadModalVisible="uploadModalVisible"/>
    <UploadModal v-if="uploadModalVisible"  @close-upload-modal="uploadModalVisible = false"/>

    <div id="main-container" class="h-[calc(100vh-4.5rem)]  flex overflow-hidden relative">

        <div id="tracklist" class="w-62 h-[calc(100vh-4.5rem)] " :class="{'transform -translate-x-[96%] border border-black' : hideTracklistPanel}">

            <div id="tracklist-divider" class="w-[97%] h-full bg-white ">
                
                <div id="tracklist-content" class="w-full h-[90%] pb-5 flex flex-col items-center gap-1 overflow-y-auto">
                    <div v-for="track in currentTrackList.trackState" :key="track.id">
                        <TrackToVisualize      
                        v-if="track.isTrackSelected"
                        :track="track"
                        @click="globalTrackIndex.selTrackIndex = track.id"
                        
                        />
                    </div>
                        <!-- <div class="flex w-full h-[10%] border border-gray-500 mt-5 ">
                            <button class="btn">Bars</button>
    
                        </div> -->
                    

                    <AudioTrackSide/>
                    

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
                    v-show="track.isWaveformDisplayed"
                    :track="track"
                    @click="globalTrackIndex.selTrackIndex = track.id"/>
                   
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
        <div 
        class="h-full w-41 absolute top-0 right-1 flex bg-gray-200 transform duration-400"
        :class="{'transform translate-x-37 border border-black' : hideSettingPanel}">
        
        
        <div id="tracklist-button" class="w-[7%] h-full">
            <button @click="hideSettingPanel = ! hideSettingPanel" id="arrow-left" class="h-50 border-black"
            :class="{' border-r-[0.5rem] border-l-[0rem]' : hideSettingPanel, 'border-l-[0.5rem] border-r-[0rem]': !hideSettingPanel}"></button>
        </div>
        <div v-for="track in currentTrackList.trackState" :key="track.id">
            <RightPanel v-if="track.isTrackSelected" :track="track"/>
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
<style>
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