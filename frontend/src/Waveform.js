

import WaveSurfer from "wavesurfer.js";
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.regions.min.js';
import Cursor from 'wavesurfer.js/dist/plugin/wavesurfer.cursor.min.js';
import Markers from 'wavesurfer.js/dist/plugin/wavesurfer.markers.min.js';
import Spectrogram from 'wavesurfer.js/dist/plugin/wavesurfer.spectrogram.min.js';
import { api } from "../custom";
import {showAlert, closeAlert} from './alerts'
import colormap from './hot-colormap.json'
import { changeBackground, getOnset} from "./filesFunctions";
import { ref } from "vue";
import { getCookie } from "./cookieHandling";




var wavesurfer = []
var track = []
var numberOfBars
var index = 0
var currentAudio = []
var trackFromStart = ref([])

let peaks


function addTextToVisualization(trackID, text){
    document.getElementById(`waveformTextGray-${trackID}`).insertAdjacentText('beforeend', text)
    document.getElementById(`waveformTextGrayHidden-${trackID}`).insertAdjacentText('beforeend', text + ' (w)')
    document.getElementById(`spectrogramTextGray-${trackID}`).insertAdjacentText('beforeend', text)
    document.getElementById(`spectrogramTextGrayHidden-${trackID}`).insertAdjacentText('beforeend', text + ' (s)')
    
}
function makeWaveform(audio,trackName, start, end, fromBar, toBar){
    currentAudio.push(audio)
    track.push([trackName, start, end])
    trackFromStart.value.push([trackName, start, end,fromBar, toBar, audio])
    localStorage.setItem(`trackName`, JSON.stringify(trackFromStart.value))

    // document.getElementById(`waveContainer-${index}`).style.display = "block"
    // addTextToVisualization(index, trackName)
    // let slider = document.querySelector('[data-action="zoom"]');
    
    setTimeout(() => createWavesurfer(audio, trackName),0)
        
    // slider.value = wavesurfer.params.minPxPerSec;
    // slider.value = '1'
    // slider.min = wavesurfer.params.minPxPerSec;
    // slider.min = 10
    // console.log(wavesurfer.params.plugins[1].params.regions[0])

    // slider.addEventListener('input', function() {
    //     wavesurfer.zoom(Number(this.value));
    // });
        
    // // set initial zoom to match slider value
    // wavesurfer.zoom(slider.value);
}
function trimWaveform(start,end, selectedTrackIndex, fromBar, toBar){

   var nameOfCuttedTrack
   if(fromBar && toBar){
       nameOfCuttedTrack = ' - bars (' + fromBar + ' - ' + toBar + ')'
    }else{
        nameOfCuttedTrack = ' - trimmed (' + start.toFixed(2) + 's - ' + end.toFixed(2) + 's)'       
    }

    
    makeWaveform(trackFromStart.value[selectedTrackIndex][5], trackFromStart.value[selectedTrackIndex][0] + nameOfCuttedTrack, start, end, fromBar, toBar)
    
    
    
    var trimmedTrackId = trackFromStart.value.length -2

    var segmentDuration = end - start

    var originalBuffer = wavesurfer[selectedTrackIndex].backend.buffer;
  
    var emptySegment = wavesurfer[trimmedTrackId].backend.ac.createBuffer(
        originalBuffer.numberOfChannels,
        segmentDuration * originalBuffer.sampleRate,
        originalBuffer.sampleRate
    );
    var frameCount = segmentDuration * originalBuffer.sampleRate
  
    for (var i = 0; i < originalBuffer.numberOfChannels; i++) {
        var chanData = originalBuffer.getChannelData(i);
        var segmentChanData = emptySegment.getChannelData(i);
        for (var j = 0, f = Math.round(start*originalBuffer.sampleRate), t = Math.round(0*originalBuffer.sampleRate), len = chanData.length; j < len; j++, f++, t++) {
            segmentChanData[t] = chanData[f];
            
        }
    }
    setTimeout(() => wavesurfer[trimmedTrackId +1].empty(), 0)
    setTimeout(() => wavesurfer[trimmedTrackId + 1].loadDecodedBuffer(emptySegment),0)
    
    wavesurfer[trimmedTrackId].spectrogram.init()

    api.get('/trim-audio/' + trackFromStart.value[selectedTrackIndex][0] + '/' + start + '/' + end + '/' + fromBar + '/' + toBar)
    .then((response) => {  
        getOnset(nameOfCuttedTrack + ' - ' +trackFromStart.value[selectedTrackIndex][0], trackFromStart.value[selectedTrackIndex][0] + nameOfCuttedTrack)
    })

}


// function marker(beatDuration, selectedTrackIndex){
//     numberOfBars = beatDuration
//     beatDuration.forEach(function(oneBeat, id){
//         wavesurfer[selectedTrackIndex].addMarker({
//             time: oneBeat,
//             label: id+1,
//             color: "black",
//         })
//     })
//     beatDuration.forEach(function(oneBeat, id){
//         if (id == beatDuration.length-1){
//             wavesurfer[selectedTrackIndex].addRegion({
//                 id: id+1,
//                 start: beatDuration[id],
//                 end: wavesurfer[selectedTrackIndex].getDuration(),
//                 drag: false,
//                 resize: false,
//                 color: "rgba(0, 0, 0, 0)"   
//             })
//         }

//         if(id > 0){       
//             wavesurfer[selectedTrackIndex].addRegion({
//                 id: id,
//                 start: beatDuration[id-1],
//                 end: oneBeat,
//                 drag: false,
//                 resize: false,
//                 color: "rgba(0, 0, 0, 0)"   
//             })
//         }
//     })
//     // wavesurfer[selectedTrackIndex].on("region-dblclick", (region) => {  
//     //     // e.stopPropagation();
//     //     // wavesurfer.play(region.start, region.end)
//     //     axios.get('/get-trimmed-audio/' + track[selectedTrackIndex] + '/' + region.start + '/' + region.end + '/' + fromBar + '/' + toBar)
//     //     .then((response) => {   
//     //         console.log(response)
//     //         let audio = new Audio(response.request.responseURL);
//     //         makeWaveform(audio,track[selectedTrackIndex])    
//     //     })
//     // })

    
// }

function createWavesurfer(audio,trackName){

    wavesurfer.push(WaveSurfer.create({
    container: `#waveform-${trackName.replace(/\.|\(|\)|\ /g, '')}`,
    backend: 'WebAudio',
    waveColor: 'violet',
    progressColor: 'purple',
    backgroundColor: 'white',
    loopSelection: true,
    scrollParent: true,
    autoCenter: true,
    responsive: true, 
    normalize: true,
    pixelRatio: 1,
    height: 200,
    xhr: {credentials: "include"},
 
    plugins: [

        Spectrogram.create({
            
            container: `#spectrogram-${trackName.replace(/\.|\(|\)|\ /g, '')}`,
            colorMap: colormap,
            fftSamples: 1024,
            height: 256,
            labels: true,
            frequencyMax: 12000,
            windowFunc: 'hann'
            
            
        
            }),
        Markers.create({
            opacity: 1,
        }),
        TimelinePlugin.create({
            container: `#timeline-${trackName.replace(/\.|\(|\)|\ /g, '')}`,
        }),
        RegionsPlugin.create({}),
        Cursor.create({
            showTime: true,
            opacity: 1,

            
            customShowTimeStyle: {
                'background-color': '#000',
                color: '#fff',
                padding: '2px',
                'font-size': '10px'
                
            }
        }),
    ],
    }))
    

    wavesurfer[trackFromStart.value.length - 1].load(audio)
 
    wavesurfer[trackFromStart.value.length - 1].on('ready', function(){
    
        
     
        // const curentSpecLabels = document.querySelector(".spec-labels")
        // curentSpecLabels.id = `spec-labels-${index}`
        // console.log(index, ':', curentSpecLabels)
    
        // nastaveno ve wavesurfer.spectrogram.min.js
        // var labels = document.querySelectorAll(".spec-labels")
        // labels.forEach(label => {
        //     label.style.position = 'absolute'
        //   });

        var labels = document.querySelectorAll(".spec-labels")
        labels.forEach((label, index) => {
            label.id = `spec-labels-${index}`
            });
    })
    

    index += 1  
}


export { makeWaveform, track, trackFromStart, wavesurfer, numberOfBars}

