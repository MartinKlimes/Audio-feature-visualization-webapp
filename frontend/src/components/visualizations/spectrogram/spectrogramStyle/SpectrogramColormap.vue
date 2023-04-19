<script setup>
import colormap from "colormap";
import SelectFiles from "../../../globalTools/SelectFiles.vue";
import { onMounted, ref } from "vue";
import { api } from "../../../../composables/custom";
import { wavesurfer } from "../../../../functions/waveform/waveform";
import { trackList } from "../../../../stores/globalStores";
import { updateRecording } from "../../../../composables/custom";

const imagePaths = ref([]);
const currentTrackList = trackList();

const props = defineProps({
  id: Number,
});

onMounted(() => {
  api.get("/get-files-list/colormap").then(function (response) {
    response.data.forEach((element) => {
      api.get("/get-file/" + element).then((response) => {
        imagePaths.value.push(response.request.responseURL);
      });
    });
  });
});

const changeColormap = (e) => {
  currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = true;

  setTimeout(() => {
    const colorName = e.split("/").pop().split(".")[0];
    currentTrackList.selectTrack(props.id).spectrogram.spectrogramColormap = colorName;
    updateRecording(props.id, "spectrogramColormap", colorName);
    let colors = colormap({
      colormap: colorName,
      nshades: 256,
      format: "float",
      alpha: 1,
    });

    wavesurfer[props.id].spectrogram.params.colorscale = colorName;
    wavesurfer[props.id].spectrogram.params.colorMap = colors;
    wavesurfer[props.id].spectrogram.init();
    currentTrackList.selectTrack(props.id).spectrogram.isSpectrogramLoading = false;
  }, 0);
};
</script>

<template>
  <div class="w-20 shadow-inner shadow-dark-300 rounded-md flex justify-center mt-2 text-gray-600 text-sm">
    {{ currentTrackList.selectTrack(id).spectrogram.spectrogramColormap }}
  </div>
  <transition>
    <SelectFiles
      :id="id"
      :files="imagePaths"
      :isImage="true"
      class="mt-2"
      :selected-file="
        imagePaths[
          imagePaths.indexOf(`http://127.0.0.1:5000/get-file/${currentTrackList.selectTrack(id).spectrogram.spectrogramColormap}.png`)
        ]
      "
      @select-file="changeColormap($event)"
    />
  </transition>
</template>
