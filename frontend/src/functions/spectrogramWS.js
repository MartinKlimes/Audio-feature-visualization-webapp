import Spectrogram from 'wavesurfer.js/src/plugin/spectrogram/index';
import {wavesurfer} from './waveform'
import FFT from 'wavesurfer.js/src/plugin/spectrogram/fft'

export const createSpectrogramWS = async () => {

    // Spectrogram.create({
    //     container: `#spectrogram`,
    //     colorMap: colormap,
    //     fftSamples: 1024,
    //     height: 256,
    //     labels: true,
    //     frequencyMax: 12000,
    //     windowFunc: 'hann'
    // })
//     const my = {
//         buffer: wavesurfer[31].backend.buffer,
//         fftSamples: 512,
//         height: 256,
//         width: 5000,
//         freqFrom: 5000,
//         freqMin: 1500,
//         freqMax: 12000,
//         colorMap: []
                
//     }

//     const canvas = document.querySelector('canvas')
//     const ctx = canvas.getContext('2d')
//     const windowFunc = 'hann'
//     let alpha 


// const drawSpectrogram = (frequenciesData) => {
 
//     if (!isNaN(frequenciesData[0][0])) { // data is 1ch [sample, freq] format
//         // to [channel, sample, freq] format
//         frequenciesData = [frequenciesData];
//     }

//     const spectrCc = ctx
//     const height = my.fftSamples / 2;
//     const width = my.width;
//     const freqFrom = my.buffer.sampleRate / 2;
//     const freqMin = my.freqMin;
//     const freqMax = my.freqMax;

//     if (!spectrCc) {
//         return;
//     }
//     for (let i = 0; i < 256; i++) {
//         const val = (255 - i) / 256;
//         my.colorMap.push([val, val, val, 1]);
//     }

//     for (let c = 0; c < frequenciesData.length; c++) { // for each channel
//         // const pixels = my.resample(frequenciesData[c]);
//         const pixels = frequenciesData[c]
//         const imageData = new ImageData(width, height);
       
//         for (let i = 0; i < pixels.length; i++) {
//             for (let j = 0; j < pixels[i].length; j++) {
//                 const colorMap = my.colorMap[pixels[i][j]];
//                 const redIndex = ((height - j) * width + i) * 4;
//                 imageData.data[redIndex] = colorMap[0] * 255;
//                 imageData.data[redIndex + 1] = colorMap[1] * 255;
//                 imageData.data[redIndex + 2] = colorMap[2] * 255;
//                 imageData.data[redIndex + 3] = colorMap[3] * 255;
//             }
//         }

//         // scale and stack spectrograms
//         createImageBitmap(imageData).then(renderer =>
//             spectrCc.drawImage(renderer,
//                 0, height * (1 - freqMax / freqFrom), // source x, y
//                 width, height * (freqMax - freqMin) / freqFrom, // source width, height
//                 0, height * c, // destination x, y
//                 width, height // destination width, height
//             )
//         );
//     }
// }

// const getFrequencies = (callback) => {
//     const fftSamples = my.fftSamples
//     const buffer = my.buffer
//     const channels = 1

//     if (!buffer) {
//         this.fireEvent('error', 'Web Audio buffer is not available');
//         return;
//     }

//     // // This may differ from file samplerate. Browser resamples audio.
//     const sampleRate = buffer.sampleRate;
//     const frequencies = [];

//     let noverlap
//     if (!noverlap) {
//         const uniqueSamplesPerPx = buffer.length / canvas.width;
//         noverlap = Math.max(0, Math.round(fftSamples - uniqueSamplesPerPx));
//     }
    
//     const fft = new FFT(
//         fftSamples,
//         sampleRate,
//         windowFunc,
//         alpha
//     );

//     for (let c = 0; c < channels; c++) { // for each channel
//         const channelData = buffer.getChannelData(c);
//         const channelFreq = [];
//         let currentOffset = 0;

//         while (currentOffset + fftSamples < channelData.length) {
//             const segment = channelData.slice(
//                 currentOffset,
//                 currentOffset + fftSamples
//             );
//             const spectrum = fft.calculateSpectrum(segment);
           
//             const array = new Uint8Array(fftSamples / 2);
//             let j;
//             for (j = 0; j < fftSamples / 2; j++) {
//                 array[j] = Math.max(-255, Math.log10(spectrum[j]) * 45);
//             }
//             channelFreq.push(array);
            
//             // channelFreq: [sample, freq]

//             currentOffset += fftSamples - noverlap;
//         }
//         frequencies.push(channelFreq);
        
//         // frequencies: [channel, sample, freq]
//     }
   
//         callback(frequencies);
        
   
// }
// getFrequencies(drawSpectrogram)

}