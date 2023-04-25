<script setup>
import { ref } from "vue";
import { Icon } from "@iconify/vue";
import { userInfo } from "../../stores/globalStores";
import { useI18n } from "vue-i18n";
import AudioPlayer from "./AudioPlayer.vue";
import UserSetting from "./UserSetting.vue";

const { t, locale } = useI18n();
const currentUserInfo = userInfo();

const props = defineProps({
  uploadModalVisible: Boolean,
});



const menuOpen = ref(false);


const emits = defineEmits(["openUploadModal"]);
</script>

<template>
  <div id="navbar" class="h-13 border-b pl-12 pr-12 bg-white">
    <div class="flex">
      <button
        title="Upload files"
        class="hover:bg-gray-300 rounded-md mb-1"
        :class="{ 'shadow-inner shadow-dark-200': uploadModalVisible }"
      >
        <Icon icon="ic:baseline-drive-folder-upload" :inline="true" width="35" @click="$emit('openUploadModal')" />
      </button>

      <AudioPlayer />
    </div>

    <div id="user-icon" class="flex h-full items-center gap-1 hover:text-dark-50 cursor-pointer" @click="menuOpen = !menuOpen">
      <span class="font-semibold hover:text-dark-50">{{ currentUserInfo.username }}</span>
      <Icon icon="ph:user-circle-light" :inline="true" width="40" />
    </div>
  </div>

  <UserSetting
  v-if="menuOpen"
  @close-user-setting="menuOpen = false"
  />
  
</template>

<style scoped>
#navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
</style>
