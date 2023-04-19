<script setup>
import PlayBtn from "./PlayBtn.vue";
import { trackIndex } from "../../stores/globalStores";
import { wavesurfer } from "../../functions/waveform/waveform";
import { storeToRefs } from "pinia";
import { ref, watch, watchEffect } from "vue";

const globalTrackIndex = trackIndex();
const { selTrackIndex, selTracksToPlay } = storeToRefs(globalTrackIndex);
const isPlaying = ref([]);
const currentTime = ref('00:00:00');
const duration = ref('00:00:00');

const getCurrentTime = (id) => {
  countTime();
  const xpos = `${wavesurfer[id].drawer.lastPos - wavesurfer[id].drawer.wrapper.scrollLeft}px`;
  const liveCursorSpec = document.getElementById(`spectrogram-liveCursor-${id}`);
  const liveCursorpiano = document.getElementById(`pianoroll-liveCursor-${id}`);

  if (liveCursorSpec) {
    liveCursorSpec.style.left = xpos;
  }
  if (liveCursorpiano) {
    liveCursorpiano.style.left = xpos;
  }
};

const play = (id) => {
  const cursorSpec = document.getElementById(`spectrogram-cursor-${id}`);
  const cursorpiano = document.getElementById(`pianoroll-cursor-${id}`);

  if (cursorSpec) {
    cursorSpec.style.visibility = "hidden";
  }
  if (cursorpiano) {
    cursorpiano.style.visibility = "hidden";
  }

  wavesurfer[id].play();
  isPlaying.value.push(id);

  wavesurfer[id].on("audioprocess", getCurrentTime.bind(this, id));

  globalTrackIndex.selTracksToPlay.forEach((id) => {
    if (!isPlaying.value.includes(id)) {
      wavesurfer[id].play();
      isPlaying.value.push(id);
    }
  });

  wavesurfer[id].on("finish", function () {
    isPlaying.value.splice(isPlaying.value.indexOf(id), 1);
  });
};
const pause = (id) => {
  const cursorSpec = document.getElementById(`spectrogram-cursor-${id}`);
  const cursorpiano = document.getElementById(`pianoroll-cursor-${id}`);

  if (cursorSpec) {
    cursorSpec.style.visibility = "";
  }
  if (cursorpiano) {
    cursorpiano.style.visibility = "";
  }

  wavesurfer[id].pause();
  isPlaying.value.splice(isPlaying.value.indexOf(id), 1);
  globalTrackIndex.selTracksToPlay.forEach((id) => {
    isPlaying.value.splice(isPlaying.value.indexOf(id), 1);
    wavesurfer[id].pause();
  });
};

const stop = (id) => {
  pause(id);
  wavesurfer[id].seekTo(0);
  globalTrackIndex.selTracksToPlay.forEach((id) => {
    wavesurfer[id].seekTo(0);
  });
};

const skipForward = (id) => {
  wavesurfer[id].skipForward(wavesurfer[id].getDuration() / 100);
  globalTrackIndex.selTracksToPlay.forEach((id) => {
    wavesurfer[id].skipForward(wavesurfer[id].getDuration() / 100);
  });
};
const skipBackward = (id) => {
  wavesurfer[id].skipBackward(wavesurfer[id].getDuration() / 100);
  globalTrackIndex.selTracksToPlay.forEach((id) => {
    wavesurfer[id].skipBackward(wavesurfer[id].getDuration() / 100);
  });
};


const setDuration = () => {
  duration.value =
      Math.floor(wavesurfer[selTrackIndex.value].getDuration() / 60)
        .toString()
        .padStart(2, "0") + ":" + (wavesurfer[selTrackIndex.value].getDuration() % 60).toFixed(0).toString().padStart(2, "0") + ":" +
      (wavesurfer[selTrackIndex.value].getDuration() % 1).toFixed(2).substring(2);
}
const countTime = () => {
  return (currentTime.value =
    Math.floor(wavesurfer[selTrackIndex.value].getCurrentTime() / 60)
      .toString()
      .padStart(2, "0") +
    ":" +
    (wavesurfer[selTrackIndex.value].getCurrentTime() % 60).toFixed(0).toString().padStart(2, "0") +
    ":" +
    (wavesurfer[selTrackIndex.value].getCurrentTime() % 1).toFixed(2).substring(2));
};
watchEffect(() => {
  if (wavesurfer[selTrackIndex.value]) {
    setDuration()
    wavesurfer[selTrackIndex.value].on(
      "interaction",
      () => {
        setTimeout(() => {
          countTime();
        });
      },
      0
    );
  }
});
setTimeout(() => {
  setDuration()
}, 4000);
</script>

<template>
  <div class="flex gap-2 ml-40 mt-0.5 rounded-2xl bg-gray-300 h-9 px-3">
    <PlayBtn :icon="'tabler:player-track-prev-filled'" @click="skipBackward(selTrackIndex)" />
    <PlayBtn :icon="'tabler:player-track-next-filled'" @click="skipForward(selTrackIndex)" />
    <PlayBtn v-if="!isPlaying.includes(selTrackIndex)" :icon="'tabler:player-play-filled'" @click="play(selTrackIndex)" />
    <PlayBtn v-if="isPlaying.includes(selTrackIndex)" :icon="'tabler:player-pause-filled'" @click="pause(selTrackIndex)" />
    <PlayBtn :icon="'tabler:player-stop-filled'" @click="stop(selTrackIndex)" />
  </div>

  <div class="bg-gray-300 rounded-l-2xl px-3 mt-0.5 h-9 flex ml-10 font-bold items-center text-xl">
    {{ currentTime }}
  </div>
  <div v-if="wavesurfer[selTrackIndex]" class="bg-gray-300 rounded-r-2xl px-3 mt-0.5 h-9 flex ml-1 font-bold items-center text-xl">
    <!-- {{ wavesurfer[selTrackIndex].getDuration() }}
    {{ wavesurfer[selTrackIndex].getDuration() % 60 }} -->
    {{ duration }}
  </div>
</template>

<style scoped>
.highlighted {
  background-color: brown;
}
</style>
