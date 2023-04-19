<script setup>
import  "html-midi-player";
import { ref, onMounted, watchEffect, watch } from "vue";
import { wavesurfer } from "../../../functions/waveform/waveform";
import Cursor from "../../globalTools/Cursor.vue";
import { api } from "../../../composables/custom";
import { trackCursorPosition, createVerticalKeyboard, setInstrumentColor } from "../../../functions/pianoroll/useMidiPianoroll";
import TimelinePlugin from "wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js";
import LoadingOverlay from "../../globalTools/LoadingOverlay.vue";
import { trackList } from "../../../stores/globalStores";
import PianorollKeyboardSettings from "./pianorollSettings/PianorollKeyboardSettings.vue";
import NameVisualization from "../../globalTools/NameVisualization.vue";

const pianoroll = ref(null);
const pianorollSrc = ref(null);
const currentTrackList = trackList();

const props = defineProps({
  track: Object,
});

const setPianorollCurrentPosition = (params) => {
  trackCursorPosition(
    wavesurfer[props.track.id].drawer.lastPos + props.track.pianoroll.scrollLeft,
    props.track.id,
    props.track.pianoroll.dynamicNames,
    props.track.pianoroll.ActiveNotesColor
  );
};

const scrollListener = () => {
  pianoroll.value.getElementsByTagName("div")[2].addEventListener("scroll", (e) => {
    if (wavesurfer[props.track.id]) {
      wavesurfer[props.track.id].drawer.wrapper.scrollLeft = e.target.scrollLeft;
    }
  });
};
const mousemoveListener = () => {
  pianoroll.value.getElementsByTagName("div")[2].addEventListener("mousemove", (e) => {
    const wave = wavesurfer[props.track.id].drawer.wrapper;
    const x = wave.scrollLeft + e.clientX - pianoroll.value.getBoundingClientRect().left;
    const waveformCursor = document.getElementById(`waveform-cursor-${props.track.id}`);
    if (waveformCursor) {
      waveformCursor.style.left = `${x}px`;
    }
    const spectrogramCursor = document.getElementById(`spectrogram-cursor-${props.track.id}`);
    if (spectrogramCursor) {
      spectrogramCursor.style.left = `${x - wavesurfer[props.track.id].drawer.wrapper.scrollLeft}px`;
    }
    document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left = `${
      x - wavesurfer[props.track.id].drawer.wrapper.scrollLeft
    }px`;
  });
};

watch(
  () => props.track.MIDIFileName,
  () => {
    props.track.pianoroll.isPianorollLoading = true;

    api.get("/get-file/" + props.track.MIDIFileName, { responseType: "blob" }).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      pianorollSrc.value = url;
      setTimeout(() => {
        editPianoroll();
      }, 2000);
    });
  },
  { immediate: true }
);

const changeSize = (keyHeight) => {
  const width = wavesurfer[props.track.id].drawer.width / wavesurfer[props.track.id].getDuration();
  const paddingRight =
    (wavesurfer[props.track.id].getDuration() - document.getElementById(`pianoroll-player-${props.track.id}`).duration) * width;
  pianoroll.value.getElementsByTagName("div")[2].style.paddingRight = `${paddingRight}px`;
  pianoroll.value.config = { pixelsPerTimeStep: width, noteHeight: keyHeight };
};
const editTrimmedPianoroll = () => {
  const width = wavesurfer[props.track.id].drawer.width / wavesurfer[props.track.id].getDuration();
  currentTrackList.selectTrack(props.track.id).pianoroll.scrollLeft = props.track.start * width;
  pianoroll.value.getElementsByTagName("div")[2].style.overflow = "hidden";
  pianoroll.value.getElementsByTagName("div")[2].scrollLeft = props.track.start * width;
};

const editPianoroll = () => {
  watch(
    () => props.track.waveform.isWaveformReady,
    () => {
      if (props.track.waveform.isWaveformReady) {
        let colors;
        let noteHeight;
        // getsaturationValues(props.track.id) //save saturation for colors
        //if track is trimmed
        if (props.track.start) {
          editTrimmedPianoroll();
        } else {
          currentTrackList.selectTrack(props.track.id).pianoroll.scrollLeft = 0;
          scrollListener();
        }

        mousemoveListener();

        if (props.track.pianoroll.pianorollColor) {
          colors = props.track.pianoroll.pianorollColor
            .slice(1, -1)
            .split(",")
            .map((color) => color.replace(/"/g, ""));
        }

        watchEffect(() => {
          const { keyHeight } = createVerticalKeyboard(
            props.track.id,
            props.track.pianoroll.pianorollHeight,
            colors,
            props.track.pianoroll.dynamicNames
          );
          noteHeight = keyHeight;
          changeSize(keyHeight);
          props.track.pianoroll.isPianorollLoading = false;
        });
        watch(
          () => props.track.MIDIFileName,
          () => {
            setTimeout(() => {
              if (props.track.start) {
                editTrimmedPianoroll();
              }
              const { keyHeight } = createVerticalKeyboard(props.track.id, props.track.pianoroll.pianorollHeight, colors);
              changeSize(keyHeight);
              noteHeight = keyHeight;
              props.track.pianoroll.isPianorollLoading = false;
            }, 1000);
          }
        );

        wavesurfer[props.track.id].on("interaction", () => {
          if (props.track.pianoroll.isPianorollDisplayed) {
            setTimeout(
              () =>
                trackCursorPosition(
                  wavesurfer[props.track.id].drawer.lastPos + props.track.pianoroll.scrollLeft,
                  props.track.id,
                  props.track.pianoroll.dynamicNames,
                  props.track.pianoroll.ActiveNotesColor
                ),
              0
            );
          }
        });

        let trackCursor;
        wavesurfer[props.track.id].on("play", () => {
          if (props.track.pianoroll.isPianorollDisplayed) {
            trackCursor = setInterval(setPianorollCurrentPosition, 100);
          }
        });
        wavesurfer[props.track.id].on("pause", () => {
          clearInterval(trackCursor);
        });

        wavesurfer[props.track.id]
          .addPlugin(
            TimelinePlugin.create({
              container: `#timeline-pianoroll-${props.track.id}`,
            })
          )
          .initPlugin("timeline");

        wavesurfer[props.track.id].on("zoom", () => {
          if (props.track.start) {
            //if track is trimmed
            editTrimmedPianoroll();
          }
          if (colors) {
            setTimeout(() => {
              colors.forEach((color, index) => {
                setInstrumentColor(props.track.id, index, color);
              });
            }, 1000);
          }
          changeSize(noteHeight);
        });
      }
    },
    { immediate: true }
  );
};

const positionCursor = () => {
  const waveWidth = wavesurfer[props.track.id].drawer.width;
  wavesurfer[props.track.id].seekTo(
    (parseInt(document.getElementById(`pianoroll-cursor-${props.track.id}`).style.left, 10) +
      wavesurfer[props.track.id].drawer.wrapper.scrollLeft) /
      waveWidth
  );
};
</script>

<template>
  <div class="relative">
    <NameVisualization :track-name="track.trackName" class="left-15 text-gray-500"/>
    <LoadingOverlay v-if="track.pianoroll.isPianorollLoading" />
    <PianorollKeyboardSettings :id="track.id" />
    <midi-player :id="`pianoroll-player-${track.id}`" :src="pianorollSrc" class="hidden">UpUpAndAway</midi-player>
    <midi-visualizer type="piano-roll" :src="pianorollSrc" :id="`pianoroll-${track.id}`" ref="pianoroll" @click="positionCursor">
      <Cursor :id="`pianoroll-cursor-${track.id}`" :color="'gray-500'" :width="3" style="pointer-events: none" />
      <Cursor :id="`pianoroll-liveCursor-${track.id}`" :color="'dark-800'" />
    </midi-visualizer>
    <div :id="`keyboard-${track.id}`" class="absolute top-0"></div>
    <div :id="`timeline-pianoroll-${track.id}`" :class="props.track.backgroundColor"></div>
  </div>
</template>

<style>
.white-background {
  background-color: white;
}
.black-background {
  background-color: black;
}
.red-background {
  background-color: red;
}
.piano-roll-visualizer {
}

.highlighted {
  fill: red;
}
</style>
