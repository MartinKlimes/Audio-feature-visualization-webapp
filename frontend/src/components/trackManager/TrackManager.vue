<script setup>
import { Icon } from "@iconify/vue";
import { trackList } from "../../globalStores";
import { api } from "../../../custom";
import { showAlert, closeAlert } from "../../alerts";
import EditTrack from "./EditTrack.vue";
import EditBars from "./EditBars.vue"
import EditMIDI from "./EditMIDI.vue"
import { ref, reactive } from "vue";
import { marker } from "../../functions/waveform"
import SelButtons from "./SelButttons.vue"


const currentTrackList = trackList();
const state = reactive ({
  isEditTrack: true,
  isEditBars: false,
  isEditMIDI: false,
})

const deleteTrack = async(event) => {
  
  await api.get('/delete-audio-file/'+event.name)
  .then((response) => {
    showAlert(response.data.message);
    setTimeout(closeAlert, 1500);
    currentTrackList.trackState.splice(event.index, 1);
    currentTrackList.fill()
  })

};
const getTxt = () => {
  api.get('/get-audio-file/' + 'chopin1_gt.txt')
    .then((response) => {
      let bars = response.data.split('\n');

      marker(response.data.split('\n'), 5);
    }
  )
}

</script>

<template>
  <div class="bg-white rounded border border-b-gray-200 relative flex flex-col">
    <div class="px-6 pt-6 pb-5 font-bold border-b border-gray-200">

    <SelButtons @click="state.isEditTrack = true,state.isEditBars = false, state.isEditMIDI = false" :active="state.isEditTrack">
      Audio <Icon icon="material-symbols:audio-file-outline" class=" text-lg" :inline="true" />
    </SelButtons>
    <SelButtons @click="state.isEditBars = true,state.isEditTrack = false, state.isEditMIDI = false" :active="state.isEditBars">
      Bars <Icon icon="clarity:bars-line" :rotate="1" class=" text-lg" :inline="true" />
    </SelButtons>
    <SelButtons @click="state.isEditMIDI = true,state.isEditTrack = false, state.isEditBars= false" :active="state.isEditMIDI">
      MIDI <Icon icon="mdi:midi-port" class=" text-lg" :inline="true" />
    </SelButtons>
<!-- 

    
        <button class="btn btn-blue mr-1" :class="{'bg-blue-500 shadow-inner drop-shadow-sm shadow-dark-50 hover:bg-blue-500' : state.isEditTrack}" @click="state.isEditTrack = true,state.isEditBars = false, state.isEditMIDI = false">Audio <Icon
          icon="material-symbols:audio-file-outline"
          class=" text-lg"
          
          :inline="true"
        /></button>
        <button class="btn btn-blue mr-1" @click="state.isEditBars = true,state.isEditTrack = false, state.isEditMIDI = false">Bars <Icon
          icon="clarity:bars-line" :rotate="1"
          class="ml-3 text-lg"
          :inline="true"
        /></button>
        <button class="btn btn-blue mr-1" @click="state.isEditMIDI = true,state.isEditTrack = false, state.isEditBars= false">MIDI<Icon
          icon="fad:midiplug"
          class="ml-3 text-lg"
          :inline="true"
        /> </button> -->

    </div>
    
    <div class="p-6 h-150 overflow-y-auto">

      <EditTrack
        v-if="state.isEditTrack"
        v-for="(track, i) in currentTrackList.trackState"
        :key="track.id"
        :name="track.trackName"
        :index="i"
        @deleteTrack="deleteTrack($event)"
      />
      <EditBars
        v-if="state.isEditBars"
      />
      <EditMIDI
        v-if="state.isEditMIDI"
      />

      <!-- <div v-for="(trackname, i) in currentTrackList.trackName[0]">
        <div class="border border-gray-200 p-3 mb-4 rounded mt-4">
          <div >
            <h4 class="inline-block text-2xl font-bold">{{trackname}}</h4>
            <button
              class="ml-1 py-1 px-2 text-xs rounded text-white bg-red-600 float-right"
              @click="deleteTrack(trackname)"
            >
            <Icon icon="fa:times" />
            </button>
            <button
              title="Rename song"
              class="ml-1 py-1 px-2 text-xs rounded text-white bg-blue-600 float-right "
            >
            <Icon icon="fa:pencil" />
            </button>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>
