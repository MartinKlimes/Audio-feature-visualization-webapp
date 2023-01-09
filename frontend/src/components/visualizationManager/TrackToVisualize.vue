<script setup>
import { Icon } from '@iconify/vue';



const props = defineProps({
    name: String,
})
</script>


<template>
<div class=" h-55 w-full px-2 py-1 flex-col justify-center bg-light-700  border-2 border-gray-300  rounded-md">
    <div class="flex justify-center items-center relative">
        <button class="absolute left-0 opacity-70 rounded-md hover:opacity-100">
            <Icon icon="ic:outline-color-lens" />
        </button>
        <span class="font-bold font-serif text-gray-500 text-sm">{{name}}</span>
        <div class="w-4 h-4 bg-gray-100 border border-gray-400 hover:bg-gray-400 duration-200 rounded-sm absolute right-0 cursor-pointer" title="Select"></div>
    </div>
    <div class="mt-4 player-buttons h-7 w-full bg-gray-400 flex items-center justify-between px-2 rounded-md">
        <Icon icon="material-symbols:volume-up-outline" width="20" />
        <input type="range" class="slider appearance-none  rounded-lg cursor-pointer w-28">
        <div class="inline-flex rounded-md shadow-sm bg-gray-600 text-white " >
            <button class="w-5 text-sm border-r border-gray-400 rounded-l-md hover:bg-gray-300 hover:text-gray-800 duration-200 ">M</button>
            <button class="w-5 text-sm rounded-r-md hover:bg-gray-300 hover:text-gray-800 duration-200 ">S</button>

        </div>

    </div>
    
    <div class="h-[47%] w-full mt-5 p-2 border border-dashed border-gray-500 rounded-md ">
        <div class="grid grid-cols-2 gap-2">
            <button class="btn-hover-cursor font-semibold w-22 shadow-sm shadow-dark-100">Waveform</button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Spectrogram</button>
            <button class="btn-hover-cursor  w-22 font-semibold shadow-sm shadow-dark-100">Pianoroll</button>
            <div class="flex w-22 h-max">
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-r-none">IOI</button>
                <button class="btn-hover-cursor w-11 font-semibold shadow-sm shadow-dark-100 rounded-l-none">IBI</button>
            </div>

            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">Tempo</button>
            <button class="btn-hover-cursor w-22 font-semibold shadow-sm shadow-dark-100">RMS</button>

        

        </div>
    </div>
    <Icon icon="ph:files" width="18" class="w-8 float-right mt-2 shadow-sm shadow-gray-500 rounded-md hover:bg-gray-300 cursor-pointer"/>
</div>


</template>

<style scoped>


input[type=range]{
    -webkit-appearance: none;
}

input[type=range]::-webkit-slider-runnable-track {
    width: 300px;
    height: 5px;
    background: #ddd;
    border: none;
    border-radius: 3px;
}

input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    border: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: rgb(63, 63, 63);
    margin-top: -4px;
}

input[type=range]:focus {
    outline: none;
}

input[type=range]:focus::-webkit-slider-runnable-track {
    background: #ccc;
}


</style>