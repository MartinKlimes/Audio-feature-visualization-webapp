<script setup>
import { ref, onMounted } from 'vue';
import { wavesurfer, trackFromStart } from '../../Waveform';
import { trackIndex, trackList } from '../../globalStores';
import Chart from 'chart.js/auto';


const globalTrackIndex = trackIndex()


const props = defineProps({
    showIMI: Boolean,
    isIMIvisible: Boolean,
    selectedTimeAnnotation: Array
})
function interMeasureInterval (selectedTimeAnnotations, id){
    // only show/hide if IMI has already been created
    if(document.getElementById(`myChart-${id}`).style.display == 'block'){
        document.getElementById(`myChart-${id}`).style.display = 'none'
    }else if(document.getElementById(`myChart-${id}`).style.display == 'none'){
        document.getElementById(`myChart-${id}`).style.display = 'block'
    }else{
        // create IMI chart
        let lengthOfBars = [selectedTimeAnnotations[0]]
        for (let i = 0; i < selectedTimeAnnotations.length - 1; i++){
            lengthOfBars.push(selectedTimeAnnotations[i+1] - selectedTimeAnnotations[i])
        }
        const numberOfBarsArray = Array.from(Array(selectedTimeAnnotations.length), (_, index) => index + 1);
        var ctx = document.getElementById(`myChart-${id}`).getContext('2d');
    
        var chartIMI = new Chart(ctx, {
            type: 'line',
            data: {
        
                labels: numberOfBarsArray,
                datasets: [{
                    label: 'Length',
                    data: lengthOfBars,
                    tension: 0.2,
                    fill: 'red',
        
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: { 
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: `Inter-Measure-Interval - ${trackFromStart.value[id][0]}`
                    }
                },
                responsive: true,
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Bar duration [s]'                      
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Number of bar'
                            
                        }
                    } 
                }
            }
        }
    )  
}
    
    

}

</script>


<template>
<button v-show="showIMI" :class="{picker : isIMIvisible}" title="Inter-Measure-Interval" class="btn-hover" @click="interMeasureInterval(selectedTimeAnnotation[1], globalTrackIndex.selTrackIndex); isIMIvisible =! isIMIvisible">IMI</button>

</template>
