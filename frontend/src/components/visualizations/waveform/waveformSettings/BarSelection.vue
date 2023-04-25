<script setup>
import { ref, onDeactivated } from "vue";
import { wavesurfer } from "../../../../functions/waveform/waveform";
import BlueButttons from "../../../buttons/BlueButtons.vue";
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();

const fromBar = ref(0);
const toBar = ref(0);

onDeactivated(() => {
  // called when removed from the DOM into the cache
  // and also when unmounted
  if (wavesurfer[props.id].regions.list["selected"]) {
    wavesurfer[props.id].regions.list["selected"].remove();
  }
});

const props = defineProps({
  id: Number,
  trackName: String,
  loading: Boolean,
});

const emits = defineEmits(["trim-audio"]);

function selectBar() {
 
  if (toBar.value < fromBar.value) {
    toBar.value = fromBar.value;
  }

  if (wavesurfer[props.id].regions.list["selected"]) {
    wavesurfer[props.id].regions.list["selected"].remove();
  }
  var reg = wavesurfer[props.id].addRegion({
    id: "selected",
    drag: false,
    resize: false,
    color: "hsla(200, 100%, 30%, 0.3)",
    start: wavesurfer[props.id].regions.list[fromBar.value].start,
    end: wavesurfer[props.id].regions.list[toBar.value].end,
  });
  // }else{
  //     wavesurfer[globalTrackIndex.selTrackIndex].clearRegions()
  //     wavesurfer[globalTrackIndex.selTrackIndex].clearMarkers()
  // }
}
</script>

<template>
  <div class="flex flex-col items-center box bg-white mt-1 p-1 rounded-md w-full">
    <div class="flex mt-1 rounded-md">
      <input
        v-model="fromBar"
        type="number"
        placeholder="from"
        class="input-field-nomargin w-13 border-2 border-blue-400"
        @change="selectBar()"
      />
      <input
        v-model="toBar"
        type="number"
        placeholder="to"
        class="input-field-nomargin w-13 border-2 border-blue-400 ml-1"
        @change="selectBar()"
      />
    </div>

    <BlueButttons
      :is-btn-clicked="loading"
      :icon="loading ? 'fa:spinner' : ''"
      :icon-class="loading ? 'spin' : 'hidden'"
      @click="$emit('trim-audio', [wavesurfer[id].regions.list[fromBar].start, wavesurfer[id].regions.list[toBar].end, fromBar, toBar])"
      :disabled="loading"
      class="mt-1 px-2"
      >{{t('Visualization.select')}}</BlueButttons
    >
  </div>

  <!-- <div v-show="!hideBars" class="flex ">
    <input v-model="fromBar" type="number" placeholder="from" class="input-field-nomargin w-12 mx-1 mt-1 " @change="selectBar(hideBars)">
    <input v-model="toBar" type="number" placeholder="to"  class="input-field-nomargin w-12 mr-1 mt-1" @change="selectBar(hideBars)">
    <button class="btn hover:bg-gray-300 transition mt-1" @click="trimWaveform(wavesurfer[globalTrackIndex.selTrackIndex].regions.list[fromBar].start,wavesurfer[globalTrackIndex.selTrackIndex].regions.list[toBar].end, globalTrackIndex.selTrackIndex, fromBar, toBar); hideBars =! hideBars; selectBar(hideBars)">Select bars {{fromBar}} to {{toBar}}</button>
 
        <Icon icon="clarity:volume-up-line" width="50" :class="{hide: isToggled}" class="btn-hover mr-1 mt-1 picker "  @click=" isToggled = !isToggled; muteSoundOnBars()"/>
        <Icon icon="clarity:volume-mute-line" width="50" :class="{hide: !isToggled}" class="btn-hover mr-1 mt-1"  @click=" isToggled = !isToggled; playSoundOnBars(selectedTimeAnnotation)"/>
  
</div> 
<button  class="btn-hover" :class="{hide : showBars}" @click="selectBar(hideBars); marker(selectedTimeAnnotation[0][1], globalTrackIndex.selTrackIndex); hideBars =! hideBars;showBars =! showBars">Show Bars</button>
<button class="btn-hover picker" :class="{hide : hideBars}" @click=" hideBars =! hideBars; showBars = !showBars; selectBar(hideBars)">Hide Bars</button>
 -->
</template>

<style scoped>
#bars-selection {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
