<script setup>
import { Icon } from '@iconify/vue';
const props = defineProps({
    isBtnClicked: Boolean,
    isDisabled: Boolean,
    icon: String,
    iconClass: String,
    rotate: Number,
})

</script>


<template>

<button class="btn btn-blue p-1 font-semibold flex items-center justify-center" :class="{'bg-blue-500 shadow-inner shadow-dark-500 hover:bg-blue-500' : isBtnClicked, 'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-gray-300' : isDisabled}">
    <slot></slot><Icon :icon="icon" :class="iconClass" :rotate="rotate" class=" text-lg ml-1" :inline="true"/>
</button>




</template>