<script setup>
import { Icon } from '@iconify/vue';
import { ref } from 'vue';
import BarSelection from '../MainPanel/BarSelection.vue';
import TimeSelection from '../MainPanel/TimeSelection.vue';

const showTimeSelection = ref(false)
const showBarSeletion = ref(false)

const props = defineProps({
    trackName: String,
    id: Number,
})

</script>




<template>
<div class=" flex flex-col items-center">
    <span class="font-serif text-sm font-bold border-b border-dotted border-gray-400 rounded-md px-1">{{trackName}}</span>
   

    <div class="flex mt-2">
        <button class="p-1 buttons btn-hover-cursor font-semibold w-max  shadow-sm shadow-dark-100 flex">Bars <Icon icon="mdi:eye-off-outline" class="mt-1 ml-1"/></button>
        <span class="text-xs opacity-50 ml-3">Name of file</span>
    </div>
    <span class="text-xs opacity-50 mt-3">Select part</span>
    <div class="flex  border border-dashed border-gray-400 rounded-md p-1 justify-center items-center" >
        <button class=" p-1 btn-hover-cursor font-semibold w-max shadow-sm shadow-dark-100 flex" @click="showBarSeletion = !showBarSeletion">Bars<Icon icon="material-symbols:content-cut-rounded" class="mt-1 ml-1" /></button>
        <button class="p-1 btn-hover-cursor font-semibold w-max shadow-sm shadow-dark-100 flex ml-3" @click="showTimeSelection = !showTimeSelection">Time<Icon icon="material-symbols:content-cut-rounded" class="mt-1 ml-1" /></button>
    </div>
    <transition>
        <TimeSelection v-if="showTimeSelection" :trackName="trackName" :id="id"/>
    </transition>
    <transition>
        <BarSelection v-if="showBarSeletion"/>
    </transition>

    <button class="p-1 btn-hover-cursor font-semibold w-max shadow-sm shadow-dark-100 flex mt-3">Color<Icon icon="ic:outline-color-lens" class="mt-1 ml-1"/></button>


   
</div>



</template>

<style scoped>

.v-enter-active,
.v-leave-active {
    transition: all 0.2s;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: scale(0.5);
}


</style>