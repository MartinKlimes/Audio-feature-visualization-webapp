<script setup>
import BarSelection from './BarSelection.vue';
import TimeSelection from './TimeSelection.vue';
import { trackList } from '../../../../stores/globalStores';
import { shallowRef, ref } from 'vue';
import { showAlert, closeAlert } from '../../../../composables/alerts';
import { getCookie } from '../../../../composables/cookieHandling';
import { api } from '../../../../composables/custom';
import BlueButtons from '../../../buttons/BlueButtons.vue';
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n();

const currentSetting = shallowRef();
const loading = ref(false);
const currentTrackList = trackList();

const props = defineProps({
    id: Number,
    trackName: String,
})


const trimAudio = (event) => {
  loading.value = true;
  const record_name = props.trackName;
  const start = event[0];
  const end = event[1];
  const fromBar = event[2] || false;
  const toBar = event[3] || false;
  api
    .post(
      "/trim-audio",
      {
        record_name,
        start,
        end,
        fromBar,
        toBar,
      },
      {
        headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token"),
          "Content-Type": "multipart/form-data",
        },
      }
    )
    .then((response) => {
      currentTrackList.fetchRecordings().then(() => {
        const track = currentTrackList.selectTrack(response.data.id);
        track.waveform.isWaveform = true;
        track.waveform.isWaveformDisplayed = true;
        loading.value = false;
        currentSetting.value = null;
      });
    });
};
const showBarsToSelect = () => {
  if (document.querySelector(`#bars-marker-${props.id}`)) {
    currentSetting.value === BarSelection ? (currentSetting.value = "") : (currentSetting.value = BarSelection);
  } else {
    showAlert(t('Visualization.displayBars'));
    setTimeout(closeAlert, 1500);
  }
};

</script>


<template>
<span class="text-xs opacity-50 mt-2">{{ t('Visualization.selectPart') }}</span>
    <div class="flex border border-dashed border-gray-400 rounded-md p-1 justify-center items-center mb-1">
      <BlueButtons
        class="mr-1"
        @click="showBarsToSelect()"
        :icon="'material-symbols:content-cut-rounded'"
        :is-btn-clicked="currentSetting === BarSelection"
        >{{ t('Visualization.bars') }}</BlueButtons
      >
      <BlueButtons
        @click="currentSetting === TimeSelection ? (currentSetting = '') : (currentSetting = TimeSelection)"
        :icon="'material-symbols:content-cut-rounded'"
        :is-btn-clicked="currentSetting === TimeSelection"
        >{{ t('Visualization.time') }}</BlueButtons
      >
</div>

<transition>
      <KeepAlive>
        <component :is="currentSetting" :trackName="trackName" :id="id" :loading="loading" @trim-audio="trimAudio($event)" />
      </KeepAlive>
    </transition>


</template>