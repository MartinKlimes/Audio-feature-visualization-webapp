<script setup>
import { onMounted, onUnmounted, watch, ref, computed } from "vue";
import { api } from "../../../../custom";
import BlueButtons from "../../buttons/BlueButtons.vue";
import { wavesurfer } from "../../../functions/waveform";
import { marker } from "../../../functions/waveform";
import { ColorPicker } from "vue-accessible-color-picker";
import SelectFiles from "../../buttons/SelectFiles.vue";
import ClickSoundBtn from "../../buttons/ClickSoundBtn.vue";

const props = defineProps({
  trackName: String,
  id: Number,
  dataType: String,
  txtFileName: String,
  markersList: Array
});
const currentColor = ref("");
const showColorPicker = ref(false);
const changeLine = ref(false);
const lineType = ref("")
const zIndex = ref(true)
const showClickSound = ref(false)
const selectedClickAudio = ref(null)

const markerID = computed(() => {
  return props.dataType == "bars" ? `#bars-marker-${props.id}` : `#${props.dataType}-${props.id}`;
});

const emits = defineEmits(["toggleLoading", "toggleEye", "fillMarkersList"]);

const addMarkers = (data) => {
  let i = 0;
  const addMarker = () => {
    if (i < data.length) {
      wavesurfer[props.id].addMarker({
        time: data[i],
        color: props.dataType == "onset" ? "red" : "blue",
        lineID: `${props.dataType}-${props.id}`,
      });
      i++;
      requestAnimationFrame(addMarker);
    } 
  };
  requestAnimationFrame(addMarker);
};

onMounted(() => {
  watch(
    () => props.dataType,
    () => {
      if (document.querySelector(markerID.value)) {

        if (document.querySelector(markerID.value).style.display == "none") {
          emits("toggleEye", [true, props.dataType]);
        
          document.querySelectorAll(markerID.value).forEach((marker) => (marker.style.display = "flex"));
        }
      } else {
        emits("toggleEye", [true, props.dataType]);
        if (props.dataType == "bars") {
          api.get("/get-file/" + props.txtFileName).then((response) => {
            
            emits('fillMarkersList', response.data.split("\n").map(str => parseFloat(str)))
            marker(response.data.split("\n"), props.id);
          });
        } else {
          emits("toggleLoading", props.dataType);
          api
            .get("/get-onset-detection/" + props.trackName, {
              params: { data_type: props.dataType },
            })
            .then((response) => {
              emits('fillMarkersList', response.data[props.dataType])
              // markersList.value[props.dataType] = response.data[props.dataType]
              
              addMarkers(response.data[props.dataType]);
              emits("toggleLoading", props.dataType);

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

//change color
watch(
  () => currentColor.value,
  () => {
    // document.querySelectorAll(markerID.value).forEach((marker) => (marker.style.background = currentColor.value));
    document.querySelectorAll(`#${props.dataType}-${props.id}`).forEach((marker) => (marker.style.background = currentColor.value));
  }
);

//change line type
watch(() => lineType.value, () => {
  const match = lineType.value.match(/\d+px/);
  const value = match ? match[0] : null;
  document.querySelectorAll(`#${props.dataType}-${props.id}`).forEach((marker) => (marker.style.width = value));

})

//change zIndex
const changeZindex = () => {
  zIndex.value =! zIndex.value
  let zIndexNum
  !zIndex.value ? zIndexNum = 10 : zIndexNum = 0
 
  document.querySelectorAll(`#${props.dataType}-${props.id}`).forEach((marker) => (marker.style.zIndex = zIndexNum));
  
}

</script>

<template>
 
  <div class="flex flex-col items-center gap-1 mt-1 w-full">
    <div class="grid grid-cols-2 gap-1 boxTight w-21 rounded-md p-2">
      <BlueButtons
        :icon="'ic:outline-color-lens'"
        :icon-class="'ml-0'"
        @click="showColorPicker = !showColorPicker"
        :is-btn-clicked="showColorPicker"
      ></BlueButtons>

      <BlueButtons
        :icon="'ph:list'"
        :icon-class="'ml-0 '"
        @click="changeLine = !changeLine"
        :is-btn-clicked="changeLine"
      ></BlueButtons>

      <BlueButtons
        :icon="!zIndex ? 'fluent:copy-24-filled' : 'fluent:copy-20-regular'"
        :icon-class="'ml-0'"
        @click="changeZindex"
      ></BlueButtons>

      <BlueButtons
        :icon=" showClickSound ? 'clarity:volume-up-line' : 'clarity:volume-mute-line'"
        :icon-class="'ml-0'"
        @click="showClickSound =! showClickSound"
        :is-btn-clicked="showClickSound"
      ></BlueButtons>
      
    </div>


    <transition>
      <SelectFiles 
      v-if="changeLine"
      :id="id" 
      :files="['w-20 h-[1px] bg-black ', 'w-20 h-[2px] bg-black ', 'w-20 h-[3px] bg-black ','w-20 h-[4px] bg-black ', 'w-20 h-[5px] bg-black ']"
      :isDivClass = "true"
      :selected-file="lineType"
      class="bottom-1 z-1 w-full"
      @select-file="lineType = $event"
      @close-modal="changeLine = false"

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

    <transition>

      <ClickSoundBtn
      v-if="showClickSound"
      :id="id" 
      :markers-list="markersList"
      :selected-sound="selectedClickAudio"
      class="w-full"
      @select-audio = "selectedClickAudio = $event"
      
      />
   


    </transition>

  </div>
</template>


