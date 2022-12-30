<script setup>
import { Icon } from "@iconify/vue";
import { trackList } from "../globalStores";
import { api } from "../../custom";
import { showAlert, closeAlert } from "../alerts";


const currentTrackList = trackList();

const deleteTrack = (trackToDelete) => {
  const fileToRemove = currentTrackList.trackName[0].indexOf(trackToDelete)
  currentTrackList.trackName[0].splice(fileToRemove, 1);
  api.get('/delete-audio-file/'+trackToDelete)
  .then((response) => {
      showAlert(response.data.message);
      setTimeout(closeAlert, 1500);
  })
}


</script>

<template>
  <div class="bg-white rounded border border-b-gray-200 relative flex flex-col">
    <div class="px-6 pt-6 pb-5 font-bold border-b border-gray-200">
      <span class="card-title">My audio</span>
      <Icon
        icon="material-symbols:audio-file-outline"
        class=" ml-3 text-lg " 
        :inline="true"
      />
    </div>
    <div class="p-6 h-150 overflow-y-auto">
    
      <!-- <div class="border border-gray-200 p-3 mb-4 rounded">
        <div>
          <h4 class="inline-block text-2xl font-bold mb-3">Song Name</h4>
          <button
            class="ml-1 py-1 px-2 text-xs rounded text-white bg-red-600 float-right"
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
        <div>
          <form>
            <div class="mb-3">
             
              <input
                type="text"
                class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
                placeholder="Enter Song Title"
              />
            </div>
            <div class="mb-3">
              <label class="inline-block mb-2">Genre</label>
              <input
                type="text"
                class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
                placeholder="Enter Genre"
              />
            </div>
            <button
              type="submit"
              class="py-1.5 px-3 rounded text-white bg-green-600"
            >
              Submit
            </button>
            <button
              type="button"
              class="py-1.5 px-3 rounded text-white bg-gray-600"
            >
              Go Back
            </button>
          </form>
        </div>
      </div> -->
      <div v-for="(trackname, i) in currentTrackList.trackName[0]">
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
      </div>

    </div>
  </div>
</template>
