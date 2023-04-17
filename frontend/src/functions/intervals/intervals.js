import Chart from 'chart.js/auto';

export default class ChartManager {
  constructor(data, id, type, graph_color,graph_type, duration) {
  

    this.graph_color = graph_color
    this.intervals = [];
    this.times = [];
    this.labels = []
    if(type == 'Tempo' || type == 'RMS'){
      this.intervals = data
      const intervalSize = duration / data.length;
      for (let i = 0; i < data.length; i++) {
        const start = i * intervalSize;
        const startDate = new Date(start * 1000);
        const startMinutes = startDate.getUTCMinutes();
        const startSeconds = startDate.getUTCSeconds();
  
        const binLabel = `${startMinutes.toString().padStart(2, '0')}:${startSeconds.toString().padStart(2, '0')}`;
        this.labels.push(binLabel);
      }
    } else{
      for (let i = 0; i < data.length - 1; i++) {
        const interval = data[i + 1] - data[i];
        this.intervals.push(interval);
        this.times.push(data[i]);
      }
      this.intervals.push(data[data.length - 1] - data[data.length - 2]);
      this.times.push(data[data.length - 1]);
      this.labels = Array.from({ length: this.intervals.length }, (_, i) => i + 1)
    }
    this.type = type
    // Add the last interval and its time as well
    

    this.chart = new Chart(document.getElementById(`${type}-${id}`), {
      type: graph_type || 'bar',
      data: {
        labels:  this.labels,
        datasets: [{
          label: 'IOI',
          backgroundColor: graph_color == 'rgba(0, 0, 255, 0.5)'? 'rgba(0, 0, 255, 0.5)' : hexToRGBA(graph_color, 0.8),
          data: this.intervals,
          borderColor: graph_color == 'rgba(0, 0, 255, 0.5)'? 'rgba(0, 0, 255, 0.5)' : hexToRGBA(graph_color, 0.8),
            tension: 0.1,
            pointRadius: 2,
     

        }],
      },
      
      options: {
        plugins: {
          legend: {
            display: false,
          },
          title: {
            display: true,
            text:( type == 'Tempo' || type == 'RMS') ? type :  `Inter-${type.charAt(0).toUpperCase() + type.slice(1)}-Interval`,
          },
        },
        responsive: true,
        scales: {
          y: {
            title: {
              display: true,
              text: type === 'measure' ? 'Bar duration [s]' : type === 'onset' ? 'Onset duration [s]' : type === 'Tempo' ? 'BPM' : type === 'RMS' ? 'RMS value [db]' : 'Beats duration [s]',
            },
          },
          x: {
            title: {
              display: true,
              text: type === 'measure' ? 'Number of bar' : type === 'onset' ? 'Number of onset' : (type === 'Tempo' || type === 'RMS')  ? 'Time [min:sec]' : 'Number of beat',
            }, 
            
          },
        },
      },
    });
    this.movingAvg = [];
    this.windowSize = 20;
  }

  averageHorizontalLine() {
  const average = this.chart.data.datasets[0].data.reduce((a, b) => a + b) / this.chart.data.datasets[0].data.length;
  const existingDatasetIndex = this.chart.data.datasets.findIndex(dataset => dataset.label === 'Average');
  if (existingDatasetIndex > -1) {
    // toggle off if already exists
    this.chart.data.datasets.splice(existingDatasetIndex, 1);
  } else {
    // toggle on if not exists
    this.chart.data.datasets.push({
      type: 'line',
      label: 'Average',
      borderDash: [6, 6],
      borderDashOffset: 0,
      borderColor: 'rgba(255, 0, 0, 1)',
      borderWidth: 3,
      pointRadius: 0,
      data: Array(this.chart.data.datasets[0].data.length).fill(average),
    });
  }
  this.chart.update();
}


createMovingAverage(windowSize = this.windowSize) {
    this.windowSize = windowSize;
    this.movingAvg = [];

    for (let i = 0; i < this.chart.data.datasets[0].data.length; i++) {
      let sum = 0;
      let count = 0;
      for (let j = Math.max(0, i - windowSize + 1); j <= i; j++) {
        sum += this.chart.data.datasets[0].data[j];
        count++;
      }
      this.movingAvg.push(sum / count);
    }

    const datasets = this.chart.data.datasets;
    const movingAvgIndex = datasets.findIndex(dataset => dataset.label === 'Moving Average');
    if (movingAvgIndex !== -1) {
      datasets[movingAvgIndex].data = this.movingAvg;
    } else {
      datasets.push({
        label: 'Moving Average',
        borderColor: 'rgba(255, 0, 0, 1)',
        type: 'line',
        pointRadius: 0,
        data: this.movingAvg,
      });
    }
    this.chart.update();
  }

  deleteMovingAverage() {
    const datasets = this.chart.data.datasets;
    const movingAvgIndex = datasets.findIndex(dataset => dataset.label === 'Moving Average');
    if (movingAvgIndex !== -1) {
      datasets.splice(movingAvgIndex, 1);
      this.chart.update();
    }
  }

  updateWindowSize(windowSize) {
    this.createMovingAverage(windowSize);
  }

  changeChartType(newType) {
    this.chart.config.type = newType;
    this.chart.update();
  }
  
  changeColor(newColor) {
    const datasets = this.chart.data.datasets;
    for (let i = 0; i < datasets.length; i++) {
      datasets[i].backgroundColor = hexToRGBA(newColor, 0.5);
      datasets[i].borderColor = hexToRGBA(newColor, 0.5);
  
    }
    this.chart.update();
  }
  resetChart() {
    this.chart.destroy(); // zničí aktuální graf
  }
  createHistogramLength(numBins) {
    // Create bins for the histogram
    const minInterval = Math.min(...this.intervals);
    const maxInterval = Math.max(...this.intervals);
    const binWidth = (maxInterval - minInterval) / numBins;
    const bins = Array(numBins).fill(0);
  
    // Count the number of intervals in each bin
    for (let i = 0; i < this.intervals.length; i++) {
      const binIndex = Math.floor((this.intervals[i] - minInterval) / binWidth);
      bins[binIndex]++;
    }
  
    // Create the labels for the x-axis
    const labels = [];
    for (let i = 0; i < numBins; i++) {
      const lowerBound = minInterval + i * binWidth;
      const upperBound = minInterval + (i + 1) * binWidth;
      labels.push(`${lowerBound.toFixed(2)} - ${upperBound.toFixed(2)}`);
    }
  
    // Update the chart data
    // this.chart.config.type = 'bar';
    this.chart.data = {
      labels: labels,
      datasets: [{
        label: 'Histogram',
        backgroundColor:  this.graph_color,
        data: bins,
      }],
    };
    this.chart.options.scales.x.title.text = `Length Interval [min:sec]`;

    this.chart.update();
  }
  createHistogramTime(numBins) {
    const startTime = this.times[0]
    const endTime = this.times[this.times.length - 1];
    const intervalSize = (endTime - startTime) / numBins;
    const binCounts = Array(numBins).fill(0);
  
    for (let i = 0; i < this.intervals.length; i++) {
      const interval = this.intervals[i];
      const time = this.times[i];
      const binIndex = Math.floor((time - startTime) / intervalSize);
      if (binIndex < numBins) {
        binCounts[binIndex]++;
      }
    }

    const binLabels = [];
    for (let i = 0; i < numBins; i++) {
      const start = startTime + i * intervalSize;
      const end = startTime + (i + 1) * intervalSize;

      const startDate = new Date(start * 1000);
      const startMinutes = startDate.getUTCMinutes();
      const startSeconds = startDate.getUTCSeconds();

      const endDate = new Date(end * 1000);
      const endMinutes = endDate.getUTCMinutes();
      const endSeconds = endDate.getUTCSeconds();

      const binLabel = `${startMinutes.toString().padStart(2, '0')}:${startSeconds.toString().padStart(2, '0')} - ${endMinutes.toString().padStart(2, '0')}:${endSeconds.toString().padStart(2, '0')}`;
      binLabels.push(binLabel);
    }
  
    // this.chart.config.type = 'bar';
    this.chart.data.datasets[0].data = binCounts;
    this.chart.data.labels = binLabels;
    this.chart.data.datasets.backgroundColor = this.graph_color,
    this.chart.options.scales.x.title.text = `Time Interval [min:sec]`;
    this.chart.options.scales.y.title.text = `Interval Count`;
    this.chart.update();
  }

}

function hexToRGBA(hex, alpha) {
  const r = parseInt(hex.substring(1, 3), 16);
  const g = parseInt(hex.substring(3, 5), 16);
  const b = parseInt(hex.substring(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

const calculateRMS = (audioBuffer) => {
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

export const calculateRMSForSegments = (audioBuffer, numSegments) =>  {
  const segmentLength = Math.floor(audioBuffer.length / numSegments);
  const rmsValues = [];
  for (let i = 0; i < numSegments; i++) {
    const segmentStart = i * segmentLength;
    const segmentEnd = (i + 1) * segmentLength;
    const segment = {
      numberOfChannels: audioBuffer.numberOfChannels,
      length: segmentEnd - segmentStart,
      getChannelData(channel) {
        return audioBuffer.getChannelData(channel).subarray(segmentStart, segmentEnd);
      }
    };
    const rms = calculateRMS(segment);
    rmsValues.push(rms);
  }
  return rmsValues;
}