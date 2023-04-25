<script setup>
import { trackIndex, trackList } from "../../stores/globalStores";
import { api } from "../../composables/custom";
import { showAlert, closeAlert } from "../../composables/alerts";
import EditTrack from "./EditTrack.vue";
import { ref, reactive } from "vue";
import SelButtons from "../buttons/BlueButtons.vue";
import EditBarsMIDI from "./EditBarsMIDI.vue";
import { getCookie } from "../../composables/cookieHandling";
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n();

const currentTrackList = trackList();
const globalTrackIndex = trackIndex();
const state = reactive({
  isEditTrack: true,
  isEditBars: false,
  isEditMIDI: false,
});

const deleteTrack = async (event) => {

  await api.delete("/delete-file/" + event, {headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token"),
          "Content-Type": "application/json",
        }}).then((response) => {
    showAlert(response.data.message);
    setTimeout(closeAlert, 1500);
    // currentTrackList.trackState.splice(event.index, 1);
    currentTrackList.fetchRecordings();

    setTimeout(() => {
      if (currentTrackList.trackState[0]) {
        globalTrackIndex.changeIndex(currentTrackList.trackState[0].id);
      }
    }, 100);
  });
};
</script>

<template>
  <div class="bg-white rounded border border-b-gray-200 relative flex flex-col">
    <div class="px-6 pt-6 pb-5 font-bold border-b border-gray-200 flex">
      <SelButtons
        @click="(state.isEditTrack = true), (state.isEditBars = false), (state.isEditMIDI = false)"
        :isBtnClicked="state.isEditTrack"
        :icon="'material-symbols:audio-file-outline'"
        class="mr-1"
      >
        Audio
      </SelButtons>
      <SelButtons
        @click="(state.isEditBars = true), (state.isEditTrack = false), (state.isEditMIDI = false)"
        :isBtnClicked="state.isEditBars"
        :icon="'clarity:bars-line'"
        class="mr-1"
      >
        {{t('EditTrack.bars')}}
      </SelButtons>
      <SelButtons
        @click="(state.isEditMIDI = true), (state.isEditTrack = false), (state.isEditBars = false)"
        :isBtnClicked="state.isEditMIDI"
        :icon="'mdi:midi-port'"
      >
        MIDI
      </SelButtons>
    
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
      <EditBarsMIDI
        v-if="state.isEditBars"
        v-for="(track, i) in currentTrackList.barsList"
        :key="i"
        :name="track"
        type="bars/"
        @deleteTrack="deleteTrack($event)"
      ></EditBarsMIDI>

      <EditBarsMIDI
        v-if="state.isEditMIDI"
        v-for="(track, i) in currentTrackList.midiList"
        :key="i"
        :name="track"
        type="midi/"
        @deleteTrack="deleteTrack($event)"
      ></EditBarsMIDI>

    </div>
  </div>
</template>
