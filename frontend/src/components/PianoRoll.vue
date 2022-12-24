<script setup>
import { changeBackground} from '../filesFunctions';
import { trackList } from '../globalStores';
import { ref} from 'vue';
import { Icon } from '@iconify/vue';
const globalTrackIndex = trackList()

const props = defineProps({
    id: Number,
    trackname: Array
})

const clickOnPianoRoll = (id) => {
    window.eventBus.emit('select', id)
    globalTrackIndex.selTrackIndex = id
}

const isPianorollHidden = ref(false)

</script>





<template>

<div  @click="changeBackground(trackname[0]); clickOnPianoRoll(id)">
    <div v-show="isPianorollHidden"  :id="`showPianorollBtn-${id}`" @click="isPianorollHidden = false">
        <Icon icon="ep:arrow-down" :inline="true" width="18" class="btn-hover-cursor" :id="`showPianorollBtn-${id}`"/>
        <div class="inline text-gray-400 text-sm ml-3">{{trackname[0]}} (pr)</div>
    </div>
    <div v-show="!isPianorollHidden" :id="`pianoroll-${id}`" class="relative h-300px" >
        <Icon icon="ep:arrow-up" :inline="true" width="18" class="btn-hover-cursor" @click="isPianorollHidden = true" :id="`hidePianorollBtn-${id}`"/>
        <div class="inline text-gray-400 text-sm ml-3">{{trackname[0]}}</div>
        <div :id="`pianoroll-cursor-${id}`" class="h-70  absolute border-l-1 border-white z-10 "></div>
        <img :id="`IMGpianoroll-${id}`" class="imagePR overflow-hidden">
    </div>
</div>

</template>