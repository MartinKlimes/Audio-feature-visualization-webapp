<script setup>
import { onMounted, onUnmounted } from "vue";
import { api } from "../../../../custom";
import BlueButtons from "../../buttons/BlueButtons.vue";
import { wavesurfer } from "../../../functions/waveform";

const props = defineProps({
  trackName: String,
  id: Number,
  dataType: String
});
const emits = defineEmits(["toggleLoading"]);

const addMarkers = (data) => {
  let i = 0;
  const addMarker = () => {
    if (i < data.length) {
      wavesurfer[props.id].addMarker({
        time: data[i],
        color: props.dataType == 'onset' ? 'red' : 'blue',
        index: `${props.dataType}`,
      });
      i++;
      requestAnimationFrame(addMarker);
    } else {
      emits("toggleLoading");
    }
  }
  requestAnimationFrame(addMarker);
}

onMounted(() => {
  if(document.getElementById(props.dataType)){
    if(document.getElementById(props.dataType).style.display == 'none'){
      document.querySelectorAll(`#${props.dataType}`).forEach(marker => marker.style.display = 'flex')
    }
  } else{
    emits("toggleLoading");
    api
      .get("/get-onset-detection/" + props.trackName, {
        params: { data_type: props.dataType },
      })
      .then((response) => {
        addMarkers(response.data[props.dataType]);
      });
  }
});


onUnmounted(() => {

  document.querySelectorAll(`#${props.dataType}`).forEach(marker => marker.style.display = 'none')

});
</script>

<template>
  
  <div class="flex gap-2">
    <BlueButtons
      title="Show IOI"
      class="mt-3 items-center opacity-90"
      :is-btn-clicked="false"
      @click="showIOI()"
      :icon-class="'hidden'"
      >Color</BlueButtons
    >
  </div>
</template>
