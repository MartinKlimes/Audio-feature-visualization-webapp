<script setup>
import { trackList } from "../../stores/globalStores";
import { Icon } from "@iconify/vue";
import { onClickOutside } from "@vueuse/core";
import { ref } from "vue";


const currentTrackList = trackList();

const props = defineProps({
  files: Array,
  id: Number,
  selectedFile: String,
  isDivClass: {
    type: Boolean,
    default: false
  },
  isImage: {
    type: Boolean,
    default: false
  }

});

const emits = defineEmits(["selectFile", "closeModal"]);
const target = ref(null)

onClickOutside(target, () => 
{   
    setTimeout(() => {
    emits('closeModal')
}, 0);
})

</script>

<template>
  <div class=" bg-white border border-black rounded-md overflow-y-auto" ref="target" >
    <div
      class="min-h-6 flex items-center justify-center bg-light-blue-400 border border-black m-1 text-sm font-bold rounded-md hover hover:border-gray-400 cursor-pointer shadow-md shadow-gray-700"
      :class="{ 'shadow-inner shadow-dark-500 bg-light-blue-300 hover:border-black': selectedFile == file }"
      v-for="file in files"
      @click="$emit('selectFile', file)"
    >
    <img
        v-if="isImage"
        :src="file"
        class="object-cover w-full h-full rounded-md"
        :class="{ 'border-2 border-dotted border-blue-200': selectedFile == file }"
      


    

      />
      <div v-else-if="isDivClass" class="" :class="file">
      </div>
      <div v-else >
        {{ file }}
      </div>

    </div>
  </div>
</template>
<style scoped>
.shadow-inner {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 1);
}


</style>