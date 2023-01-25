<script setup>

const props = defineProps({
    active: Boolean
})

</script>


<template>
<button class="btn btn-blue mr-1" :class="{'bg-blue-500 shadow-inner drop-shadow-sm shadow-dark-50 hover:bg-blue-500' : active}">
<slot></slot>
</button>




</template>