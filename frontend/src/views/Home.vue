<script setup>
import { ref } from 'vue';
import NavBar from '../components/MainPanel/NavBar.vue';
import AudioTrackSide from '../components/trackManager/AudioTrackSide.vue'
import UploadModal from '../components/trackManager/UploadModal.vue';
import { tracklistState, uploadModalState, trackList, trackIndex } from '../globalStores';
import Waveform from '../components/Waveform.vue';
import { getCookie } from '../cookieHandling';
import Cursor from '../components/Cursor.vue';
import TrackToVisualize from '../components/visualizationManager/TrackToVisualize.vue';
import RightPanel from '../components/RightPanel.vue';
import PianoRoll from '../components/PianoRoll.vue';
import Spectrogram from '../components/Spectrogram.vue';

const currentTrackList = trackList();


const hideSettingPanel = ref(false)
const hideTracklistPanel = ref(false)
const globalTrackIndex = trackIndex()
const uploadModalVisible = ref(false)

currentTrackList.fetchRecordings()




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

        <div id="tracklist" class="w-62 h-[calc(100vh-12.5rem)] " :class="{'transform -translate-x-[97%] border border-black' : hideTracklistPanel}">

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
        class="h-full  text-xl text-black  bg-light-800 overflow-y-auto overflow-x-hidden transform duration-400"
        :class="{'w-[78vw] ml-63': !hideSettingPanel && !hideTracklistPanel, 'w-[86vw] ml-63' : hideSettingPanel && !hideTracklistPanel, 'w-[90.5vw] ml-3 ' : hideTracklistPanel && !hideSettingPanel, 'w-[98.5vw] mx-3.5' : hideTracklistPanel && hideSettingPanel}"
        >
        



        
        <!-- <div class="mb-7">
            
                <MainPanel 
                @showWaveform="isWaveform =! isWaveform"
                @showSpectrogram="isSpectrogram =! isSpectrogram"
                @showPianoroll ="isPianoRoll =! isPianoRoll"
                /></div> -->
                <div v-for="track in currentTrackList.trackState" :key="track.id" >
                
                <transition>
                    <Waveform 
                    v-show="track.waveform.isWaveformDisplayed"
                    :isSelected = "track.id===globalTrackIndex.selTrackIndex"
                    :track="track"
                    @click="globalTrackIndex.selTrackIndex = track.id"/>
                    
                </transition>
                <transition>
                    <Spectrogram
                    v-if="track.spectrogram.isSpectrogram && track.spectrogram.plotSpectrogram"   
                    v-show="track.spectrogram.isSpectrogramDisplayed"
                    :isSelected = "track.id===globalTrackIndex.selTrackIndex"

                    :track="track"
                    @click="globalTrackIndex.selTrackIndex = track.id"/>
                    
                </transition>
                <!-- <transition>
                    <PianoRoll
                    v-if="track.pianoroll.isPianoroll"  
                    v-show="track.pianoroll.isPianorollDisplayed"  
                    :isSelected = "track.id===globalTrackIndex.selTrackIndex"
                    :track="track"
                    @click="globalTrackIndex.selTrackIndex = track.id"
                    />
                </transition> -->
              
                

                
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
        :class="{'transform translate-x-39.5 border border-black w-0' : hideSettingPanel}">
        
        
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



/* canvas{
    display: block;
    height: 200px;
    width: 800px;
    
   
} */

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

::-webkit-scrollbar{
  width: 8px;
}
::-webkit-scrollbar-track{
  background-color: rgba(194, 194, 194, 0.685);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb{
  background: #999797;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover{
  background: #747474;
}
 


</style>