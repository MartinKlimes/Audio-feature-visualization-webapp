<script setup>
import { ref } from 'vue';
import { onClickOutside } from "@vueuse/core";
import BlueButtons from '../../../buttons/BlueButtons.vue';
import PianorollColor from './PianorollColor.vue';
import SizeSetter from '../../../tools/SizeSetter.vue';


const target = ref(null);
const emits = defineEmits(['closeModal'])
const showSizeSetter = ref(false);
const showColorSetter = ref(false)


const props = defineProps({
    id: Number,
    trackName: String,
})



onClickOutside(target, () => {
  setTimeout(() => {
    emits("closeModal");
  }, 0);
});
</script>


<template>
 <div class="flex flex-col bg-white box rounded-md py-2 px-1 mt-1 w-full items-center " ref="target">
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
        @click="showColorSetter = !showColorSetter"
        :is-btn-clicked="showColorSetter"
        :icon-class="'ml-0'"
        ></BlueButtons>
    </div>

    <Transition>
        <SizeSetter
        v-if="showSizeSetter"
        :id="id"
        :visualization="'pianoroll'"
        :loading-visualization="'isPianorollLoading'"
        />
    </Transition>

    <Transition>
        <PianorollColor
        v-if="showColorSetter"
        :id="id"
        />
    </Transition>

 </div>



</template>