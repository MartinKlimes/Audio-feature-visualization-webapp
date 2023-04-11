<script setup>
import { onMounted, watch, ref } from "vue";
import { api } from "../../../../custom";
import ChartManager from "../../../functions/intervals/intervals";
const isLoading = ref(false);
const props = defineProps({
  props: Object,
  // id: Number,
  // txtFileName: String,
  // intervalsType: String,
  // trackName: String,
  // graph_color: String,
  // showHorizontalAverage: Boolean
});

let chartManager;

onMounted(() => {
  loadChart();
});
const loadChart = () => {
  if (props.props.intervalsType == "measure") {
    api.get("/get-file/" + props.props.txtFileName).then((response) => {

      chartManager = new ChartManager(
        response.data
          .trim()
          .split("\n")
          .map((str) => parseFloat(str)),
        props.props.id,
        props.props.intervalsType,
        props.props.graph_color,
        props.props.graph_type
      );
    });
  } else {
    isLoading.value = true;
    api.get("/get-onset-detection/" + props.props.trackName, { params: { data_type: props.props.intervalsType } }).then((response) => {
      chartManager = new ChartManager(
        response.data[props.props.intervalsType],
        props.props.id,
        props.props.intervalsType,
        props.props.graph_color,
        props.props.graph_type,
      );
      isLoading.value = false;
    });
  }
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
    if(props.props.showMovingAverage){
      chartManager.createMovingAverage();
    }
  }
);
watch(
  () => props.props.histogramTimeFrameSize,
  () => {
    chartManager.createHistogramTime(props.props.histogramTimeFrameSize);
    if(props.props.showMovingAverage){
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
      loadChart();
    }, 0);
  }
);
</script>

<template>
  <div >
    <div class="text-gray-400 ml-2 text-sm " >{{ props.props.trackName }} </div>

    <!-- <LoadingOverlay v-if="isLoading" :style="{ height: props.props.height + 'px' }"/> -->

    <canvas :id="`Inter-${props.props.intervalsType}-${props.props.id}`" :height="props.props.height"></canvas>
  </div>
</template>
