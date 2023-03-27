<script setup>

import { tracklistState, trackList } from '../../globalStores';
import { storeToRefs } from 'pinia'
import { api } from '../../../custom';
import UploadModal from './UploadModal.vue';
import { reactive, ref } from 'vue'
import { Icon } from '@iconify/vue';
import {showAlert, closeAlert} from '../../alerts'
import { uploadModalState } from '../../globalStores';



const currentTrackList = trackList();
const performer = 'Janacek';
const year = '1994';



const tracklistGlobalState = tracklistState();
const {tracklistExpanded} = storeToRefs(tracklistGlobalState);



</script>


<template>
    <div v-for="(trackname, i) in currentTrackList.trackName" :id="`file-${i}`" :key="trackname">
        <div v-if="!(trackname.includes('...') || trackname.includes('\(trim.'))">
            <div class="py-2 px-4 rounded-md text-black bg-light-900 hover:bg-gray-400 transition audio-track h-10" :id="`audioList-${trackname}`">
                    <div class="track-name cursor-pointer"
                    @click="getAudioFile(trackname[0])">
                        {{ trackname[0] }}
                    </div>  
                <Transition>     
                    <div v-if="tracklistExpanded" class="hidden-content">               
                        <div>
                            <!-- {{performer}} -->                          
                        </div>
                        <div>
                            <!-- {{year}} -->
                        </div>            
                        <!-- <label class="ref-check">
                            <input type="checkbox"  class="align-middle mb-[0.2rem]" v-model="deleteItems" :value="`${trackname}`" >
                        </label> -->                   
                        <div class="w-[1.5rem] flex items-center justify-center hover:text-dark-50 transition cursor-pointer" @click="deleteTrack(trackname)">
                        <Icon icon="fluent:delete-48-regular" :inline="true" width="18"/>
                        </div>                    
                    </div>              
                </Transition>
            </div>
            
        </div>
        <div v-if="trackname.includes('\(bars') || trackname.includes('\(trim.')">
            <div class="py-2 px-4 rounded-md text-black bg-rose-400 audio-track h-10" :id="`audioList-${trackname}`">
                    <div class="track-name cursor-pointer"
                    @click="getAudioFile(trackname)">
                        {{ trackname }}
                    </div>  
                <Transition>     
                    <div v-if="tracklistExpanded" class="hidden-content">                                
                        <div class="w-[1.5rem] flex items-center justify-center hover:text-dark-50 transition cursor-pointer" @click="deleteTrack(trackname)">
                        <Icon icon="fluent:delete-48-regular" :inline="true" width="18"/>
                        </div>                    
                    </div>              
                </Transition>
            </div>
        
        </div>

        
    </div> 


</template>


<style scoped>
.audio-track{
    display: flex;
    flex-direction: row;
    gap: 1rem;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

.hidden-content{
    display: flex;
    flex-direction: row;
    gap: 1rem;
}

/* .v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
} */

</style>