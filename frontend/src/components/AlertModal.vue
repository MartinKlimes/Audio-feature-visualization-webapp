<script setup>
import { Icon } from '@iconify/vue';
import { alertState } from '../stores/globalStores';
import { storeToRefs } from 'pinia'

const alertGlobalState = alertState();
const {show, message} = storeToRefs(alertGlobalState);

</script>

<template>

<Transition name="fade">
    <div v-if="show" id="alert-container" class="z-50 h-18 top-0 absolute flex justify-center items-center w-[100%]">
        <div id="alert-modal" class="text-white font-semibold bg-dark-800 py-2 px-4 rounded-xl text-sm">
            <Icon icon="akar-icons:circle-alert" :inline="true"/> {{ message }}
        </div>
    </div>
</Transition>

</template>

<style scoped>

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>