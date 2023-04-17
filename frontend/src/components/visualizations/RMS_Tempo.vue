<script setup>
import axios from 'axios';
import { api } from '../../../custom';
import { onMounted } from 'vue';
import Chart from 'chart.js/auto';



const props = defineProps({
    id: Number,
    trackName: String,
    visualization: String
})


onMounted(() => {

  api.get("/get-file/" + props.trackName, {
  responseType: 'arraybuffer'
  }).then(response => {
    const audioData = response.data;
    const audioContext = new AudioContext();

    audioContext.decodeAudioData(audioData, decodedData => {
          const numSegments = 500;
          const rmsValues = calculateRMSForSegments(decodedData, numSegments);
          const chart = new Chart(document.getElementById('tempo'), {
        type: 'line',
        data: {
          labels: Array.from({length: numSegments}, (_, i) => i + 1),
          datasets: [{
            label: 'RMS',
            data: rmsValues,
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1
          }]
        },
        options: {
        responsive: true,
        scales: {
          y: {
            title: {
              display: true,
              text: 'RMS value',
            },
          },
          x: {
            title: {
              display: true,
              text: 'Number of segment',
            }, 
            
          },
        },
      },


      });



    })
  })
})






</script>

<template>

<div id="tem">
<canvas id="tempo" :height="100"></canvas>


</div>


</template>