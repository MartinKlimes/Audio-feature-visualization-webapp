<script setup>
import { ref, onMounted, onDeactivated, onActivated, watchEffect, onUnmounted } from "vue";
import { wavesurfer } from "../../../../functions/waveform/waveform";
import BlueButttons from "../../../buttons/BlueButtons.vue";

const from = ref(null);
const to = ref(null);
const selectedRegion = ref(null);

const props = defineProps({
  id: Number,
  trackName: String,
  loading: Boolean,
});
const emits = defineEmits(["trim-audio"]);

onMounted(() => {
  watchEffect(() => {
    if (selectedRegion.value) {
      selectedRegion.value.update({
        start: from.value,
        end: to.value,
      });
    }
  });

  wavesurfer[props.id].on("region-created", (region, e) => {
    if (selectedRegion.value) {
      selectedRegion.value.remove();
    }
    selectedRegion.value = region;
    setTimeout(() => {
      from.value = region.start;
      to.value = region.end;
    }, 200);
  });
  wavesurfer[props.id].on("region-updated", (region, e) => {
    from.value = region.start;
    to.value = region.end;
  });
});

onUnmounted(() => {
  const region = wavesurfer[props.id].regions.list[`region-${props.id}`];
  if (region) {
    region.remove();
  }
});
onDeactivated(() => {
  // called when removed from the DOM into the cache
  // and also when unmounted
  const region = wavesurfer[props.id].regions.list[`region-${props.id}`];
  if (region) {
    region.remove();
  }
  wavesurfer[props.id].disableDragSelection();
});

onActivated(() => {
  if (from.value && to.value) {
    var reg = wavesurfer[props.id].addRegion({
      start: from.value,
      end: to.value,
      color: "hsla(200, 100%, 30%, 0.3)",
      id: `region-${props.id}`,
    });
  }
  selectedRegion.value = reg;
  var reg = wavesurfer[props.id].enableDragSelection({
    color: "hsla(200, 100%, 30%, 0.3)",
    id: `region-${props.id}`,
  });
});
</script>

<template>
  <div class="flex flex-col items-center box bg-white mt-1 p-1 rounded-md w-full">
    <div class="flex mt-1 rounded-md">
      <input v-model="from" type="number" placeholder="from" class="input-field-nomargin w-15 border-2 border-blue-400" />
      <input v-model="to" type="number" placeholder="to" class="input-field-nomargin w-15 ml-1 border-2 border-blue-400" />
    </div>
    <BlueButttons
      :is-btn-clicked="loading"
      :icon="loading ? 'fa:spinner' : ''"
      :icon-class="loading ? 'spin' : 'hidden'"
      @click="$emit('trim-audio', [from, to])"
      :disabled="!from || !to"
      class="mt-1 px-2"
      >Select</BlueButttons
    >
  </div>
</template>
