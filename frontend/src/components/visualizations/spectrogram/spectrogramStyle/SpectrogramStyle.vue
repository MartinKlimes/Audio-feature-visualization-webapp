<script setup>
import { ref } from 'vue';
import { onClickOutside } from "@vueuse/core";
import SpectrogramColormap from './SpectrogramColormap.vue';
import BlueButtons from '../../../buttons/BlueButtons.vue';
import SizeSetter from '../../../tools/SizeSetter.vue';
const target = ref(null);
const emits = defineEmits(['closeModal'])
const showSizeSetter = ref(false);
const showColormapSetter = ref(false)
const loadingColor = ref(false)
const props = defineProps({
    id: Number,
    trackName: String,
    spectrogramColormap: String,
})



onClickOutside(target, () => {
  setTimeout(() => {
    emits("closeModal");
  }, 0);
});
</script>


<template>
 <div class="flex flex-col bg-white box rounded-md p-2 mt-1 w-full items-center " ref="target">
    <div class="flex gap-1">
        <BlueButtons 
        :icon="'nimbus:size-height'" 
        @click="showSizeSetter = !showSizeSetter" 
        :is-btn-clicked="showSizeSetter" 
        :icon-class="'ml-0'"
        class="w-max"
        ></BlueButtons> 

        <BlueButtons
        :icon="'ic:outline-color-lens'"
        @click="showColormapSetter = !showColormapSetter"
        :is-btn-clicked="showColormapSetter"
        :icon-class="'ml-0'"
        :loading="loadingColor"
        ></BlueButtons>
    </div>

    <Transition>
        <SizeSetter
        v-if="showSizeSetter"
        :id="id"
        :visualization="'spectrogram'"
        :loading-visualization="'isSpectrogramLoading'"
        />
    </Transition>

    <Transition>
        <SpectrogramColormap 
        v-if="showColormapSetter"
        :id="id"
        @change-color="loadingColor =! loadingColor"

        />
    </Transition>

 </div>



</template>