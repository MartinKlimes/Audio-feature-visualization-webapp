<script setup>
import { Icon } from "@iconify/vue";
import { trackList } from "../../globalStores";
import { api } from "../../../custom";
import { showAlert, closeAlert } from "../../alerts";
import EditTrack from "./EditTrack.vue";
import { ref } from "vue";


const currentTrackList = trackList();

const deleteTrack = async(event) => {
  
  await api.get('/delete-audio-file/'+event.name)
  .then((response) => {
    showAlert(response.data.message);
    setTimeout(closeAlert, 1500);
    currentTrackList.trackName.splice(event.index, 1);
  })

};

</script>

<template>
  <div class="bg-white rounded border border-b-gray-200 relative flex flex-col">
    <div class="px-6 pt-6 pb-5 font-bold border-b border-gray-200">

        <span class="card-title">My audio</span>
        <Icon
          icon="material-symbols:audio-file-outline"
          class="ml-3 text-lg"
          :inline="true"
        />
    </div>
    <div class="p-6 h-150 overflow-y-auto">
      
      <EditTrack
        v-for="(trackName, i) in currentTrackList.trackName"
        :key="trackName"
        :name="trackName[0]"
        :index="i"
        @deleteTrack="deleteTrack($event)"
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
