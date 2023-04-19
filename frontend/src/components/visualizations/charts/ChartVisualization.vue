<script setup>
import { onMounted, watch, ref } from "vue";
import { api } from "../../../composables/custom";
import ChartManager from "../../../functions/charts/charts";
import LoadingOverlay from "../../globalTools/LoadingOverlay.vue";
import { wavesurfer } from "../../../functions/waveform/waveform";
import { calculateRMSForSegments } from "../../../functions/charts/charts";
import { trackList } from "../../../stores/globalStores";
import NameVisualization from "../../globalTools/NameVisualization.vue";

const currentTrackList = trackList();
const isLoading = ref(false);
const props = defineProps({
  props: Object,
});

let chartManager;
let data;
onMounted(() => {
  loadChart();
});
const loadChart = () => {
  isLoading.value = true;
  if (props.props.intervalsType == "measure") {
    api.get("/get-file/" + props.props.txtFileName).then((response) => {
      data = response.data
        .trim()
        .split("\n")
        .map((str) => parseFloat(str));
      createInstance(data);
    });
  } else if (props.props.intervalsType == "Tempo") {
    api.get(`/get-tempo/${props.props.trackName}/${props.props.numOfFrames}`).then((response) => {
      data = response.data;
      createInstance(data, wavesurfer[props.props.id].getDuration());
    });
  } else if (props.props.intervalsType == "RMS") {
    watch(
      () => currentTrackList.selectTrack(props.props.id).waveform.isWaveformReady,
      () => {
        if (currentTrackList.selectTrack(props.props.id).waveform.isWaveformReady) {
         
          data = calculateRMSForSegments(wavesurfer[props.props.id].backend.buffer, props.props.numOfFrames);

          createInstance(data, wavesurfer[props.props.id].getDuration());
        }
      },
      { immediate: true }
    );
  } else {
    api.get("/get-event-detection/" + props.props.trackName, { params: { data_type: props.props.intervalsType } }).then((response) => {
      data = response.data[props.props.intervalsType];
      createInstance(data);
    });
  }
};
const createInstance = (data, duration) => {
  chartManager = new ChartManager(
    data,
    props.props.id,
    props.props.intervalsType,
    props.props.graph_color,
    props.props.graph_type,
    duration
  );
  isLoading.value = false;
};
watch(
  () => props.props.showHorizontalAverage,
  () => {
    chartManager.averageHorizontalLine();
  }
);
watch(
  () => props.props.movingAverageWindowSize,
  () => {
    chartManager.updateWindowSize(props.props.movingAverageWindowSize);
  }
);
watch(
  () => props.props.histogramLengthFrameSize,
  () => {
    chartManager.createHistogramLength(props.props.histogramLengthFrameSize);
    if (props.props.showMovingAverage) {
      chartManager.createMovingAverage();
    }
  }
);
watch(
  () => props.props.histogramTimeFrameSize,
  () => {
    chartManager.createHistogramTime(props.props.histogramTimeFrameSize);
    if (props.props.showMovingAverage) {
      chartManager.createMovingAverage();
    }
  }
);

watch(
  () => props.props.showMovingAverage,
  () => {
    if (props.props.showMovingAverage) {
      chartManager.createMovingAverage();
    } else {
      chartManager.deleteMovingAverage();
    }
  }
);
watch(
  () => props.props.graph_color,
  () => {
    chartManager.changeColor(props.props.graph_color);
  }
);
watch(
  () => props.props.graph_type,
  () => {
    chartManager.changeChartType(props.props.graph_type);
  }
);
watch(
  () => props.props.height,
  () => {
    chartManager.resetChart();
    setTimeout(() => {
      createInstance(data);
      // loadChart();
    }, 0);
  }
);
watch(
  () => props.props.numOfFrames,
  () => {
    chartManager.resetChart();
    setTimeout(() => {
      // createInstance(data)
      loadChart();
    }, 0);
  }
);
</script>

<template>
  <div class="relative">
    <NameVisualization :track-name=currentTrackList.selectTrack(props.props.id).trackName class="top-0 left-15 z-20 text-gray-500"/>
    

    <LoadingOverlay v-if="isLoading" :style="{ height: props.props.height + 'px' }" />

    <canvas :id="`chart-${props.props.intervalsType}-${props.props.id}`" :height="props.props.height"></canvas>
  </div>
</template>
