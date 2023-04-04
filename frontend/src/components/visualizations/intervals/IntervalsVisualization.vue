<script setup>
import { onMounted } from 'vue';
import { api } from '../../../../custom';
import Chart from 'chart.js/auto';

const props = defineProps({
    id: Number,
    txtFileName: String
})

onMounted(() => {
    api.get("/get-file/" + props.txtFileName).then((response) => {
            console.log(response.data.split("\n").map(str => parseFloat(str)));
            const intervalStartTimes = response.data.split("\n").map(str => parseFloat(str))
            const intervals = [];
            for (let i = 0; i < intervalStartTimes.length - 1; i++) {
                const interval = intervalStartTimes[i + 1] - intervalStartTimes[i];
                intervals.push(interval);
            }
            console.log(intervals);

       

    })
})

// const ioiChart = new Chart(document.getElementById("myChart"), {
//             type: "bar",
//             data: {
//                 labels: Array.from({ length: intervals.length }, (_, i) => i + 1), // popisky osy X pro každý IOI
//                 datasets: [
//                 {
//                     label: "IOI", // název datové sady
//                     backgroundColor: "rgba(0, 0, 255, 0.5)", // barva sloupců
//                     data: intervals, // hodnoty IOI pro každý sloupec
//                 },
//                 ],
//             },
//             });
</script>


<template>

<div>
  <canvas id="myChart"></canvas>
</div>



</template>