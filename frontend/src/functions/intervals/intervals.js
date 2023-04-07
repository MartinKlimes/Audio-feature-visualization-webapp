import Chart from 'chart.js/auto';

export default class ChartManager {
  constructor(data, id, type) {

    this.intervals = [];
    const times = [];
    for (let i = 0; i < data.length - 1; i++) {
      const interval = data[i + 1] - data[i];
      this.intervals.push(interval);
      times.push(data[i]);
    }

    // Add the last interval and its time as well
    this.intervals.push(data[data.length - 1] - data[data.length - 2]);
    times.push(data[data.length - 1]);

    this.chart = new Chart(document.getElementById(`${type}-${id}`), {
      type: 'bar',
      data: {
        labels: times,
        datasets: [{
          label: 'IOI',
          backgroundColor: 'rgba(0, 0, 255, 0.5)',
          data: this.intervals,
        }],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
          title: {
            display: true,
            text: `Inter-${type.charAt(0).toUpperCase() + type.slice(1)}-Interval`,
          },
        },
        responsive: true,
        scales: {
          y: {
            title: {
              display: true,
              text: type === 'measure' ? 'Bar duration [s]' : type === 'onset' ? 'Onset duration [s]' : 'Beats duration [s]',
            },
          },
          x: {
            title: {
              display: true,
              text: type === 'measure' ? 'Number of bar' : type === 'onset' ? 'Number of onset' : 'Number of beat',
            }, 
            
          },
        },
      },
    });
    this.movingAvg = [];
    this.windowSize = 20;
  }

  averageHorizontalLine() {
  const average = this.intervals.reduce((a, b) => a + b) / this.intervals.length;
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
      data: Array(this.chart.data.labels.length).fill(average),
    });
  }
  this.chart.update();
}


createMovingAverage(windowSize = this.windowSize) {
  console.log('object');

    this.windowSize = windowSize;
    this.movingAvg = [];

    for (let i = 0; i < this.intervals.length; i++) {
      let sum = 0;
      let count = 0;
      for (let j = Math.max(0, i - windowSize + 1); j <= i; j++) {
        sum += this.intervals[j];
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
      datasets[i].backgroundColor = newColor;
    }
    this.chart.update();
  }
  resetChart() {
    this.chart.destroy(); // zničí aktuální graf
  }
  createHistogram(numBins) {
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
    this.chart.config.type = 'bar';
    this.chart.data = {
      labels: labels,
      datasets: [{
        label: 'Histogram',
        backgroundColor: 'rgba(0, 0, 255, 0.5)',
        data: bins,
      }],
    };
    this.chart.update();
  }
  createHistogramFrame(numBins) {
    const startTime = this.chart.data.labels[0];
    const endTime = this.chart.data.labels[this.chart.data.labels.length - 1];
    const intervalSize = (endTime - startTime) / numBins;
    const binCounts = Array(numBins).fill(0);
  
    for (let i = 0; i < this.intervals.length; i++) {
      const interval = this.intervals[i];
      const time = this.chart.data.labels[i];
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
  
    this.chart.config.type = 'bar';
    this.chart.data.datasets[0].data = binCounts;
    this.chart.data.labels = binLabels;
    this.chart.options.scales.x.title.text = `Time Interval [min:sec]`;
    this.chart.options.scales.y.title.text = `Interval Count`;
    this.chart.update();
  }

  
}
