<script setup>
import { Icon } from '@iconify/vue';
import { computed } from 'vue';
const props = defineProps({
    isBtnClicked: Boolean,
    isDisabled: Boolean,
    icon: String,
    iconClass: String,
    rotate: Number,
    loading: {
        type: Boolean,
        default: false
    }
})

const iconClass = computed (() =>{
    return !props.icon ? 'hidden' : props.iconClass
})

</script>


<template>

<button class="btn btn-blue p-1 font-semibold flex items-center justify-center" :class="{'bg-blue-500 shadow-inner shadow-dark-500 hover:bg-blue-500' : isBtnClicked, 'bg-transparent text-black shadow-sm shadow-dark-50 hover:bg-gray-300' : isDisabled}">
    <slot></slot>
    <Icon v-if="!loading" :icon="icon" :class="iconClass" :rotate="rotate" class=" text-lg ml-1" :inline="true"/>
    <Icon v-if="loading" :icon="'fa:spinner'" class="spin"/>
</button>




</template>