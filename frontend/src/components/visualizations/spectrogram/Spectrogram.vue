<script setup>
import Cursor from "../../globalTools/Cursor.vue";
import { onMounted, onUnmounted, ref, watch } from "vue";
import Spectrogram from "../../../functions/wavesurferSpectorgram/index";
import colormap from "colormap";
import { wavesurfer } from "../../../functions/waveform/waveform";
import TimelinePlugin from "wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js";
import { Icon } from "@iconify/vue";
import { trackList } from "../../../stores/globalStores";
import LoadingOverlay from "../../globalTools/LoadingOverlay.vue";
import { useHideElement } from "../../../composables/useHideElement";
import NameVisualization from "../../globalTools/NameVisualization.vue";
const currentTrackList = trackList();
const hideBtn = ref(false);
const hideLegendPanel = ref(false);
const hideLablelsPanel = ref(false);

onMounted(() => {
  currentTrackList.selectTrack(props.track.id).spectrogram.isSpectrogramLoading = true;
  setTimeout(() => {
    createSpectrogramPlugin();
  }, 100);
});

const createSpectrogramPlugin = () => {
  watch(
    () => props.track.spectrogram.plotSpectrogram,
    () => {
      if (props.track.spectrogram.plotSpectrogram) {
        let colors = colormap({
          colormap: props.track.spectrogram.spectrogramColormap,
          nshades: 256,
          format: "float",
          alpha: 1,
        });

        wavesurfer[props.track.id]
          .addPlugin(
            Spectrogram.create({
              container: `#spectrogram-${props.track.id}`,
              colorMap: colors,
              colorscale: props.track.spectrogram.spectrogramColormap,
              fftSamples: props.track.spectrogram.fftSamples,
              height: props.track.spectrogram.spectrogramHeight,
              labels: true,
              legend: true,
              frequencyMax: 12000,
              frequencyMin: 0,
              log: false,
              windowFunc: props.track.spectrogram.windowFunc,
              splitChannels: false,
            })
          )
          .initPlugin("spectrogram");
        wavesurfer[props.track.id]
          .addPlugin(
            TimelinePlugin.create({
              container: `#timeline-spectrogram-${props.track.id}`,
            })
          )
          .initPlugin("timeline");
        wavesurfer[props.track.id].on("zoom", () => {
          currentTrackList.selectTrack(props.track.id).spectrogram.showSpectrogramRefresh = true;
        });
      }
    },
    { immediate: true }
  );
};

const props = defineProps({
  track: Object,
  isSelected: Boolean,
});

//po kliknutí na spektrogram a umístí kurzor na danou pozici a provede seek na odpovídající pozici ve zvukovém souboru.
const positionCursor = ($e) => {
  const waveWidth = wavesurfer[props.track.id].drawer.width;
  wavesurfer[props.track.id].seekTo(
    (parseInt(document.getElementById(`spectrogram-cursor-${props.track.id}`).style.left, 10) +
      wavesurfer[props.track.id].drawer.wrapper.scrollLeft) /
      waveWidth
  );
};
const renderSpectrogram = () => {
  currentTrackList.selectTrack(props.track.id).spectrogram.renderingSpectrogram = true;
  setTimeout(() => {
    wavesurfer[props.track.id].spectrogram.init();
  }, 100);
};

const { hide } = useHideElement(hideBtn);

const hideLegend = () => {
  hideLegendPanel.value = !hideLegendPanel.value;
  document.querySelector(`.spec-legend-${props.track.id}`).classList.toggle("hidden");
};

const hideLabels = () => {
  hideLablelsPanel.value = !hideLablelsPanel.value;
  document.querySelector(`.spec-labels-${props.track.id}`).classList.toggle("hidden");
};
</script>

<template>
  <div :class="[{ 'shadow-md shadow-gray-500': isSelected }, track.backgroundColor]">
    <div :id="`spectrogram-${track.id}`" class="relative min-h-20" @click="positionCursor()">
      <NameVisualization :track-name="track.trackName" class="top-0 left-15 z-20 text-gray-400" />

      <LoadingOverlay v-if="track.spectrogram.isSpectrogramLoading" />
      <Cursor :id="`spectrogram-cursor-${track.id}`" :color="'gray-500'" :width="4" />
      <Cursor :id="`spectrogram-liveCursor-${track.id}`" :color="'dark-800'" :width="1" />
      <div
        v-show="track.spectrogram.showSpectrogramRefresh"
        title="zoom spectrogram"
        class="absolute z-10 right-20 mt-1 cursor-pointer hover:bg-gray-500 rounded-md bg-white flex shadow-lg shadow-dark-500"
      >
        <Icon
          icon="zondicons:refresh"
          title="Zoom"
          :class="{ spin: track.spectrogram.renderingSpectrogram }"
          :width="30"
          @click="renderSpectrogram"
        />
      </div>
      <div @mouseenter="hide" class="w-15 h-full absolute right-0 bottom-0 z-10">
        <Icon
          v-if="hideBtn"
          :icon="hideLegendPanel ? 'mdi:show-outline' : 'mdi:hide-outline'"
          class="hover:bg-white hover:border hover:border-black rounded-md float-right"
          @click="hideLegend()"
        />
      </div>
      <div @mouseenter="hide" class="w-15 h-full absolute left-0 bottom-0 z-10">
        <Icon
          v-if="hideBtn"
          :icon="hideLablelsPanel ? 'mdi:show-outline' : 'mdi:hide-outline'"
          class="hover:bg-white hover:border hover:border-black rounded-md"
          @click="hideLabels()"
        />
      </div>
    </div>

    <div :id="`timeline-spectrogram-${track.id}`" :class="track.backgroundColor"></div>
  </div>
</template>
