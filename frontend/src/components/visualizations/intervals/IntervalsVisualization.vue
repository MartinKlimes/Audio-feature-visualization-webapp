<script setup>
import { onMounted, watch, ref} from 'vue';
import { api } from '../../../../custom';
import  ChartManager  from '../../../functions/intervals/intervals'
import { trackList } from '../../../stores/globalStores';
import LoadingOverlay from '../../tools/LoadingOverlay.vue';
const currentTrackList = trackList()
const isLoading = ref(false)
const heightValue = ref()
const props = defineProps({
    props: Object
    // id: Number,
    // txtFileName: String,
    // intervalsType: String,
    // trackName: String,
    // graph_color: String,
    // showHorizontalAverage: Boolean
})

let chartManager

onMounted(() => {
  loadChart()
})
const loadChart = () => {
  if(props.props.intervalsType == 'measure'){
      api.get("/get-file/" + props.props.txtFileName).then((response) => {
        //   createChart(response.data.trim().split("\n").map(str => parseFloat(str)), props.id, props.intervalsType )
        chartManager  = new ChartManager(response.data.trim().split("\n").map(str => parseFloat(str)), props.props.id, props.props.intervalsType)
      })
  } else{
      isLoading.value = true
      api.get("/get-onset-detection/" + props.props.trackName, {params: { data_type: props.props.intervalsType },})
      .then((response) => {
        console.log(response.data);
        chartManager  = new ChartManager(response.data[props.props.intervalsType], props.props.id, props.props.intervalsType)
        isLoading.value = false
      })
      
  }
}
watch(() => props.props.showHorizontalAverage, () => {
    chartManager.averageHorizontalLine()
 })
watch(() => props.props.movingAverageWindowSize, () => {
    chartManager.updateWindowSize(props.props.movingAverageWindowSize)
 })

watch(() => props.props.showMovingAverage, () => {
  chartManager.createHistogram(20)

  // if(props.props.showMovingAverage){
  //   chartManager.createMovingAverage()
  // }else{
  //   chartManager.deleteMovingAverage()
  // }
 })
watch(() => props.props.graph_color, () => {
  chartManager.createHistogramFrame(100)
    // chartManager.changeColor(props.props.graph_color)
 })

watch(() =>props.props.height, () =>{
  
  chartManager.resetChart()
  setTimeout(() => {
    loadChart()
  }, 0);
} )


</script>


<template>

    <div class="" >
      <!-- <LoadingOverlay v-if="isLoading" :style="{ height: props.props.height + 'px' }"/> -->

  <canvas :id="`${props.props.intervalsType}-${props.props.id}`" :height="props.props.height"></canvas>
</div>



</template>