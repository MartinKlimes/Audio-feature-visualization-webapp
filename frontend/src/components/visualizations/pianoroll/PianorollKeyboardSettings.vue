<script setup>
import { Icon } from "@iconify/vue";
import { useHideBtn } from "../../../composables/useHideBtn";
import { ref } from "vue";
import { trackList } from "../../../globalStores";

const showKeyboardSetting = ref(false);
const { hide } = useHideBtn(showKeyboardSetting);
const hideKeyboard = ref(false);
const hideNotes = ref(false);
const currentTrackList = trackList()
const props = defineProps({
  id: Number,
});

const keyboardHide = () => {
  hideKeyboard.value = !hideKeyboard.value;
  document.querySelector(`#keyboard-${props.id}`).classList.toggle("hidden");
};
const noteNamesHide = () => {
    hideNotes.value =! hideNotes.value
    currentTrackList.selectTrack(props.id).pianoroll.dynamicNames = false;
 setTimeout(() => {
     const noteNames = document.querySelectorAll(`#keyboard-${props.id} div #noteName`);
     noteNames.forEach((noteName) => {
       noteName.classList.toggle("hidden");
     });
 }, 0);

};

</script>

<template>
  <div @mouseenter="hide" class="w-15 h-full absolute z-5"></div>

  <transition>
    <div v-if="showKeyboardSetting" class="absolute text-sm  w-10  bg-gray-500 rounded-md flex z-10 cursor-pointer flex items-center justify-between">
      <Icon
        :icon="hideKeyboard ? 'mdi:show' : 'mdi:hide'"
        class="hover:bg-white w-full hover:border hover:border-black rounded-l-md z-20"
        @click="keyboardHide()"
        :title="'hide keyboard'"
      />
      <Icon
        :icon="hideNotes ? 'mdi:show' : 'mdi:hide'"
        class="hover:bg-white w-full  hover:border hover:border-black rounded-r-md"
        @click="noteNamesHide()"
      />
    </div>
  </transition>
</template>
