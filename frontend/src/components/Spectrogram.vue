<script setup>
import SpectrogramSetting from "./SpectrogramSetting.vue";
import { ref, reactive } from "vue";
import { Icon } from "@iconify/vue";
import { wavesurfer, trackFromStart, track } from "../Waveform";
import { trackIndex } from "../globalStores";
import { changeBackground } from "../filesFunctions";
import { api } from "../../custom";

const globalTrackIndex = trackIndex();

const state = reactive({
  isSpectrogramHide: false,
  isSetting: false,
});

const props = defineProps({
  id: Number,
  trackname: Array,
});

const clickOnSpectrogram = (id) => {
  window.eventBus.emit("select", id);
  globalTrackIndex.selTrackIndex = id;
};

const getSpectrogram = (id) => {
  console.time;
  api.get("get-spectrogram").then((response) => {
    console.log(response);

    document.getElementById(`Spectrogram-${id}`).src =
      response.request.responseURL;
    console.timeEnd;
  });
};
// document.getElementById(`IMGpianoroll-${selectedTrackIndex}`).src = response.request.responseURL
</script>

<template>
  <div>
    <div id="spectrograms" class="relative">
      <img :id="`Spectrogram-${id}`" class="h-80" />
      <div
        :class="{ hide: !state.isSpectrogramHide }"
        :id="`showSpectBtn-${id}`"
        @click="state.isSpectrogramHide = false"
      >
        <Icon
          icon="ep:arrow-down"
          :inline="true"
          width="18"
          :id="`showSpectBtn-${id}`"
          class="btn-hover-cursor"
        />
        <div class="inline text-gray-400 text-sm ml-3">
          {{ trackname[0] }} (s)
        </div>
      </div>

      <transition name="spectrogram">
        <div
          :id="`spectrogram-${trackname[0].replace(/\.|\(|\)|\ /g, '')}`"
          class="relative"
          v-show="!state.isSpectrogramHide"
          @click="
            changeBackground(trackname[0]);
            clickOnSpectrogram(id);
          "
        >
          <button class="bg-dark-100 text-base" @click="getSpectrogram(id)">
            Get Spectrogram
          </button>
          <Icon
            icon="ep:arrow-up"
            :inline="true"
            width="18"
            @click="state.isSpectrogramHide = true"
            class="btn-hover-cursor"
          />
          <Icon
            icon="ant-design:setting-outlined"
            width="18"
            :class="{ picker: state.isSetting }"
            class="btn-hover-cursor -mb-0.1"
            @click="state.isSetting = !state.isSetting"
          />

          <transition name="specSettings">
            <SpectrogramSetting
              :id="`spect-setting-${id}`"
              v-if="state.isSetting"
            />
          </transition>

          <div class="inline text-gray-400 text-sm ml-3">
            {{ trackname[0] }}
          </div>
          <div
            :id="`spectCursor-${id}`"
            class="h-70 absolute border-l-1 border-white z-10"
          ></div>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.specSettings-enter-active,
.specSettings-leave-active {
  transition: all 0.15s;
}

.specSettings-enter-from,
.specSettings-leave-to {
  opacity: 0;
  transform: scale(0.75);
  transform: translateX(-20px);
}

.spectrogram-enter-active,
.spectrogram-leave-active {
  transition: all 0.2s;
}

.spectrogram-enter-from,
.spectrogram-leave-to {
  opacity: 0;
  transform: scale(0.75);
}
</style>
