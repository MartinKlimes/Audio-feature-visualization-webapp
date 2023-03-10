<script setup>
import Cursor from './Cursor.vue';
import {onMounted} from 'vue';
import Spectrogram from '../functions/spectorgram/index';
import colormap from "colormap"
import { wavesurfer } from '../functions/waveform';
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js';



let colors = colormap({
    colormap: 'jet',
    nshades: 256,
    format: 'float',
    alpha: 1
})

onMounted(() => {
  wavesurfer[props.track.id].addPlugin(Spectrogram.create({
      container: `#spectrogram-${props.track.id}`,
          colorMap: colors,
          fftSamples: 1024,
          height: 256,
          labels: true,
          legend: true,
          frequencyMax: 12000,
          frequencyMin: 0,
          log: false,
          windowFunc: 'hann',
          splitChannels: false,
          
  })).initPlugin('spectrogram')
  wavesurfer[props.track.id].addPlugin(TimelinePlugin.create({
          container: `#timeline-spectrogram-${props.track.id}`,
      })).initPlugin('timeline')

})

const props = defineProps({
  track: Object,
  isSelected: Boolean

})


  //po kliknutí na spektrogram a umístí kurzor na danou pozici a provede seek na odpovídající pozici ve zvukovém souboru.
const positionCursor = ($e) => {
  const waveWidth = wavesurfer[props.track.id].drawer.width
  wavesurfer[props.track.id].seekTo((parseInt(document.getElementById(`spectrogram-cursor-${props.track.id}`).style.left, 10) + wavesurfer[props.track.id].drawer.wrapper.scrollLeft) / waveWidth)

}
</script>






<template>

<div :class="[{'shadow-md shadow-gray-500' : isSelected}]" >
 

  <div :id="`spectrogram-${track.id}`" class="relative" @click="positionCursor()">
    <Cursor :id="`spectrogram-cursor-${track.id}`" :color="'gray-500'" :width="4"/>
    <Cursor :id="`spectrogram-liveCursor-${track.id}`"  :color="'dark-800'" :width="1"/>
    
  </div>
  <div :id="`timeline-spectrogram-${track.id}`" :class="track.backgroundColor"></div>

</div>



</template>