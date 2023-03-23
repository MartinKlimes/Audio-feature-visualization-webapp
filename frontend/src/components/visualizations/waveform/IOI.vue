<script setup>
import { onMounted, onUnmounted, watch, ref, computed } from "vue";
import { api } from "../../../../custom";
import BlueButtons from "../../buttons/BlueButtons.vue";
import { wavesurfer } from "../../../functions/waveform";
import { marker } from "../../../functions/waveform";
import { ColorPicker } from "vue-accessible-color-picker";
import SelectFiles from "../../buttons/SelectFiles.vue";

const props = defineProps({
  trackName: String,
  id: Number,
  dataType: String,
  txtFileName: String,
});
const currentColor = ref("");
const showColorPicker = ref(false);
const changeLine = ref(false);
const lineType = ref("")

const markerID = computed(() => {
  return props.dataType == "bars" ? `#bars-marker` : `#${props.dataType}`;
});

const emits = defineEmits(["toggleLoading", "toggleEye"]);

const addMarkers = (data) => {
  let i = 0;
  const addMarker = () => {
    if (i < data.length) {
      wavesurfer[props.id].addMarker({
        time: data[i],
        color: props.dataType == "onset" ? "red" : "blue",
        lineID: `${props.dataType}`,
      });
      i++;
      requestAnimationFrame(addMarker);
    } else {
      emits("toggleLoading", props.dataType);
    }
  };
  requestAnimationFrame(addMarker);
};

onMounted(() => {
  watch(
    () => props.dataType,
    () => {
      if (document.getElementById(props.dataType)) {
        console.log(markerID.value);

        if (document.querySelector(markerID.value).style.display == "none") {
          emits("toggleEye", [true, props.dataType]);
          console.log(markerID.value);
          document.querySelectorAll(markerID.value).forEach((marker) => (marker.style.display = "flex"));
        }
      } else {
        emits("toggleEye", [true, props.dataType]);
        if (props.dataType == "bars") {
          api.get("/get-file/" + props.txtFileName).then((response) => {
            marker(response.data.split("\n"), props.id);
          });
        } else {
          emits("toggleLoading", props.dataType);
          api
            .get("/get-onset-detection/" + props.trackName, {
              params: { data_type: props.dataType },
            })
            .then((response) => {
              addMarkers(response.data[props.dataType]);
            });
        }
      }
    },
    { immediate: true }
  );
});

onUnmounted(() => {
  document.querySelectorAll(markerID.value).forEach((marker) => (marker.style.display = "none"));
  emits("toggleEye", [false, props.dataType]);
});

watch(
  () => currentColor.value,
  () => {
    document.querySelectorAll(`#${props.dataType}`).forEach((marker) => (marker.style.background = currentColor.value));
  }
);

watch(() => lineType.value, () => {
  const match = lineType.value.match(/\d+px/);
  const value = match ? match[0] : null;
  document.querySelectorAll(`#${props.dataType}`).forEach((marker) => (marker.style.width = value));

})

</script>

<template>
  <div class="flex flex-col items-center gap-1">
    <div class="flex">
      <BlueButtons
        :icon="'ic:outline-color-lens'"
        :icon-class="'mr-1'"
        @click="showColorPicker = !showColorPicker"
        :is-btn-clicked="showColorPicker"
        class="mt-1 w-max"
      ></BlueButtons>

      <input
        id="range-input"
        type="number"
        title="Line width"
        class="pl-1 w-9 h-7 rounded-md text-dark-700 bg-gray-300 font-bold mt-1 ml-1"
        v-model="lightnessAdjustment"
        min="0"
        max="100"
      />

      <BlueButtons
        :icon="'ph:list'"
        :icon-class="'mr-1 '"
        @click="changeLine = !changeLine"
        :is-btn-clicked="changeLine"
        class="mt-1 ml-1"
      ></BlueButtons>
    </div>
    <transition>
      <SelectFiles 
      v-if="changeLine"
      :id="id" 
      :files="['w-20 h-[1px] bg-black ', 'w-20 h-[2px] bg-black ', 'w-20 h-[3px] bg-black ','w-20 h-[4px] bg-black ', 'w-20 h-[5px] bg-black ']"
      :isDivClass = "true"
      class="bottom-1 z-1 max-h-37"
      @select-file="lineType = $event"

      />
    </transition>



    <transition>
      <ColorPicker
        v-if="showColorPicker"
        :selected-color="currentColor"
        @color-change="currentColor = $event.cssColor"
        class="overflow-hidden max-h-60 rounded-md z-20 mt-2"
        alpha-channel="hide"
      />
    </transition>
  </div>
</template>

<style scoped>
input[type="number"]:focus {
  outline: none;
}
</style>
