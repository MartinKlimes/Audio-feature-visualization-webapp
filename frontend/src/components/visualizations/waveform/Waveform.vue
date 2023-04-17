<script setup>
import { ref, onMounted } from "vue";
import { Icon } from "@iconify/vue";
import { useHideBtn } from "../../../composables/useHideBtn";
import { api } from "../../../../custom";
import { createWavesurfer } from "../../../functions/waveform";
import { wavesurfer } from "../../../functions/waveform";
import { trackIndex, trackList } from "../../../stores/globalStores";
import LoadingOverlay from "../../tools/LoadingOverlay.vue";



const showZoomerSetting = ref(false)
const hideZoomer = ref(false)
const globalTrackIndex = trackIndex()
const currentTrackList = trackList()
const {hide} = useHideBtn(showZoomerSetting)

onMounted(() => {
  currentTrackList.selectTrack(props.track.id).waveform.isWaveformLoading = true
  api.get("/get-file/" + props.track.trackName).then((response) => {
    const audioSrc = response.request.responseURL;

    let colors = [];
    if (props.track.waveform.waveformColor) {
      colors = props.track.waveform.waveformColor.slice(2, -2).split('","');
    } else {
      colors[0] = "purple";
      colors[1] = "violet";
    }

    createWavesurfer(
      audioSrc,
      props.track.trackName,
      props.track.id,
      colors[1],
      colors[0],
      props.track.waveform.splitChannels,
      props.track.waveform.waveformHeight
    );
    if(props.track.waveform.isWaveform){
      globalTrackIndex.changeIndex(props.track.id)
    }
  });
});

const props = defineProps({
  track: Object,
  isSelected: Boolean,
});

const changeHeight = (e) => {
    wavesurfer[props.track.id].params.normalize = false
    wavesurfer[props.track.id].params.barHeight = e
    wavesurfer[props.track.id].drawBuffer()
  


};

const refreshZoomer = () => {
    wavesurfer[props.track.id].params.normalize = true
    document.getElementById(`zoomerWidth-${props.track.id}`).value = 20
    document.getElementById(`zoomerHeight-${props.track.id}`).value = 1
    wavesurfer[props.track.id].zoom(20)
    wavesurfer[props.track.id].seekTo(0)
}

</script>

<template>
  <!-- //vif -->

  <div justify="between" class="rounded-sm py-0.5" :class="track.backgroundColor">
    <div
      class="relative mt-1"
      :id="`waveformContainer-${track.id}`"
      :class="[{ 'shadow-md shadow-gray-500': props.isSelected }]"
    >
      <transition>
        <div :id="`waveform-${track.id}`" >
          <LoadingOverlay  v-if="track.waveform.isWaveformLoading"/>
          <div class="text-gray-400 ml-2 text-sm " >{{ track.trackName }} </div>

     
        <div v-show="!hideZoomer" data-html2canvas-ignore="true">

            <div class="absolute right-15 bottom-10 z-10 flex rounded-md bg-white p-0.5" @mouseenter="zoom">
                <Icon icon="material-symbols:zoom-out" />
                <input
                type="range"
                min="0"
                max="200"
                value="20"
                step="5"
                class="slider vertical bg-transparent "
                :id="`zoomerWidth-${track.id}`"
                @input="wavesurfer[track.id].zoom($event.target.value)"
                />
                <Icon icon="material-symbols:zoom-in-rounded" />
            </div>
            <div class="absolute -right-15 bottom-35 z-10 flex transform -rotate-90" @mouseenter="zoom">
                <Icon icon="material-symbols:zoom-out"  :rotate="1" />
                <input
                type="range"
                min="0"
                max="20"
                value="1"
                :id="`zoomerHeight-${track.id}`"
                
                class="slider vertical bg-transparent "
                
                @input="changeHeight($event.target.value)"
                />
                <Icon icon="material-symbols:zoom-in-rounded"  :rotate="1"/>
                   
            </div>
        </div>
      
       
            <transition>
                <div v-show="showZoomerSetting"  class="absolute right-3 gap-1 bottom-10 bg-gray-400 rounded-md flex z-10  z-10 cursor-pointer" data-html2canvas-ignore="true">
                    <Icon icon="zondicons:refresh" class="hover:bg-white hover:border hover:border-black rounded-l-md" @click="refreshZoomer"/>
                    <Icon  :icon="hideZoomer ? 'mdi:show' : 'mdi:hide'" class="hover:bg-white hover:border hover:border-black rounded-r-md" @click="hideZoomer =! hideZoomer"/>
                </div>
            </transition>
            <div @mouseenter="hide" class="w-15 h-10 absolute right-0 bottom-10 z-5"></div>
        </div>
      </transition>
      <!-- <Icon icon="ci:close-small" v-show="!state.isWaveformHide" class="hover:bg-gray-300 transition cursor-pointer top-0 right-0 absolute -my-1  -mr-4.25 text-black" @click="deleteVisualization(id)"/> -->

      <div :id="`timeline-${track.id}`"></div>
    </div>
  </div>
</template>

