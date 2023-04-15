<script setup>
import axios from 'axios';
import { api } from '../../../custom';
import { onMounted } from 'vue';
import Chart from 'chart.js/auto';



const props = defineProps({
    id: Number,
    trackName: String
})


onMounted(() => {
  api.get("/get-file/" + props.trackName, {
  responseType: 'arraybuffer'
}).then(response => {
  const audioData = response.data;
  const audioContext = new AudioContext();

  audioContext.decodeAudioData(audioData, decodedData => {
        const audioBuffer = decodedData;
        const rms = calculateRMS(audioBuffer)
        console.log(rms);


        // const signal = audioBuffer.getChannelData(0);
        // const dataPoints = [];
    


        // const bufferSize = 32768
      
        // const numberOfBuffers = Math.floor(signal.length / bufferSize);

        // for (let i = 0; i < numberOfBuffers; i++) {
        // let signal1 = signal.slice(i * bufferSize, (i + 1) * bufferSize);
        // let rms = Meyda.extract("rms", signal1);
        // dataPoints.push({ x: i, y: rms });
        // }
        // const chartData = {

        // labels: dataPoints.map(d => d.x),
        // datasets: [
        //     {
        //     label: "RMS",
        //     data: dataPoints.map(d => d.y),
        //     borderColor: "rgb(255, 99, 132)",
        //     borderWidth: 1,
        //     fill: false
        //     }
        // ]
        // };

// const chartOptions = {
//   responsive: true,
//   maintainAspectRatio: false,
//   scales: {
//     xAxes: [
//       {
//         display: true,
//         scaleLabel: {
//           display: true,
//           labelString: "Time"
//         }
//       }
//     ],
//     yAxes: [
//       {
//         display: true,
//         scaleLabel: {
//           display: true,
//           labelString: "RMS"
//         }
//       }
//     ]
//   }
// };
    // const chart = new Chart(document.getElementById(`tempo`), {
    //     type: "bar",
    //     data: chartData,
    //     options: chartOptions
    //     });

    // console.log('Tempo:', tempo);
  })
  
})
})


function calculateRMS(audioBuffer) {
        let sumOfSquares = 0;
        for (let channel = 0; channel < audioBuffer.numberOfChannels; channel++) {
            const channelData = audioBuffer.getChannelData(channel);
            for (let i = 0; i < channelData.length; i++) {
            sumOfSquares += channelData[i] * channelData[i];
            }
        }
        const rms = Math.sqrt(sumOfSquares / (audioBuffer.numberOfChannels * audioBuffer.length));
        return rms;
        }
</script>

<template>

<div id="tem">
<canvas id="tempo" :height="200"></canvas>


</div>


</template>