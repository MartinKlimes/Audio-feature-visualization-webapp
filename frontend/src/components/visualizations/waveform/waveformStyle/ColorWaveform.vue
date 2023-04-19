<script setup>
import { ColorPicker } from "vue-accessible-color-picker";
import { wavesurfer } from "../../../../functions/waveform/waveform";
import { onClickOutside } from "@vueuse/core";
import { ref, watchEffect } from "vue";
import { updateRecording } from "../../../../composables/custom";

const props = defineProps({
  id: Number,
  trackName: String,
});

const emits = defineEmits(["closeWaveformColorPicker"]);
const target = ref(null);
const lightnessAdjustment = ref(50);
const currentColor = ref(wavesurfer[props.id].getWaveColor());

const changeColorStatus = () => {
  updateRecording(props.id, "waveformColor", [wavesurfer[props.id].getProgressColor(), wavesurfer[props.id].getWaveColor()], props.id);
  // api.get("/change-track-status/waveformColor/" + props.track.trackName + "/" + [wavesurfer[props.track.id].getProgressColor(), wavesurfer[props.track.id].getWaveColor(), splitChannelsStatus.value])
};

watchEffect(() => {
  const match = currentColor.value.match(/hsl\((\d+) ([\d.]+)% ([\d.]+)%\)/);
  if (!match) {
    return;
  }
  const hue = parseInt(match[1]);
  const saturation = parseFloat(match[2]);
  const lightness = parseFloat(match[3]);

  const newLightness = Math.min(Math.max(lightness + lightnessAdjustment.value, 0), 100);
  const newColor = `hsl(${hue}, ${saturation}%, ${newLightness}%)`;

  wavesurfer[props.id].setProgressColor(newColor);
  wavesurfer[props.id].setWaveColor(currentColor.value);
});

window.onbeforeunload = () => {
  changeColorStatus();
};

onClickOutside(target, () => {
  wavesurfer[props.id].getWaveColor();
  changeColorStatus();
  setTimeout(() => {
    emits("closeWaveformColorPicker");
  }, 0);
});
</script>

<template>
  <div ref="target" class="relative">
    <ColorPicker
      :color="currentColor"
      @color-change="currentColor = $event.cssColor"
      class="overflow-hidden max-h-60 rounded-md z-20 mt-2"
      alpha-channel="hide"
    />

    <label for="range-input" class="absolute right-0 bottom-7 z-10 text-sm">lightness</label>
    <input
      id="range-input"
      type="number"
      class="absolute w-10 h-10 rounded-md text-dark-700 bg-white font-bold right-0 bottom-0"
      v-model="lightnessAdjustment"
      min="0"
      max="100"
    />
  </div>
</template>

<style scoped>
input[type="number"]:focus {
  outline: none;
}
</style>
