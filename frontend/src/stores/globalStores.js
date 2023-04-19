import { defineStore } from "pinia";
import { api } from "../composables/custom";

export const alertState = defineStore("alertState", {
  state: () => ({
    show: false,
    message: "",
  }),
});

export const userInfo = defineStore("userInfo", {
  state: () => ({
    username: "",
  }),
});

export const trackList = defineStore("trackList", {
  state: () => ({
    trackState: [],
    barsList: [],
    midiList: [],
  }),
  actions: {
    async fetchRecordings() {
      try {
        const response = await api.get("/get-track-list");
        const recordings = response.data;

        this.trackState = recordings[0];
        this.barsList = recordings[1];
        this.midiList = recordings[2];
      } catch (error) {
        console.error(error);
      }
    }
  },
  getters: {
    selectTrack: (state) => (id) => {
      return state.trackState.find((track) => track.id === id);
    }
  },
});

export const trackIndex = defineStore("trackIndex", {
  state: () => ({
    selTrackIndex: "",
    selTracksToPlay: [],
  }),
  actions: {
    changeIndex(id) {
      this.selTrackIndex = id;
    },
  },
});
