
import WaveSurfer from "wavesurfer.js";
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.regions.min.js';
import Cursor from 'wavesurfer.js/dist/plugin/wavesurfer.cursor.min.js';
import Markers from 'wavesurfer.js/dist/plugin/wavesurfer.markers.min.js';
import Spectrogram from 'wavesurfer.js/dist/plugin/wavesurfer.spectrogram.min.js';
import colormap from '../hot-colormap.json'
import { api } from "../../custom";
import { trackList } from "../globalStores";




export var wavesurfer = []
export function createWavesurfer(audio,trackName, id){
    wavesurfer[id] = WaveSurfer.create({
    container: `#waveform-${id}`,
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

        // Spectrogram.create({
            
        //     container: `#spectrogram-${trackName.replace(/\.|\(|\)|\ /g, '')}`,
        //     colorMap: colormap,
        //     fftSamples: 1024,
        //     height: 256,
        //     labels: true,
        //     frequencyMax: 12000,
        //     windowFunc: 'hann'
            
            
        
        //     }),
        Markers.create({
            opacity: 1,
        }),
        TimelinePlugin.create({
            container: `#timeline-${id}`,
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
    })
    

    wavesurfer[id].load(audio)

    wavesurfer[id].on('ready', function () {
        const currentTrackList = trackList()
        currentTrackList.selectUsedTrack(id).isWaveformLoading = false
        
    });
    // const currentTrackList = trackList()

    // api.get("/change-track-status/isWaveform/" + trackName)
    // .then(
    //   (currentTrackList.trackState[trackId].isWaveform =
    //     !currentTrackList.trackState[trackId].isWaveform)
    // );

    
    
        
     
    //     // const curentSpecLabels = document.querySelector(".spec-labels")
    //     // curentSpecLabels.id = `spec-labels-${index}`
    //     // console.log(index, ':', curentSpecLabels)
    
    //     // nastaveno ve wavesurfer.spectrogram.min.js
    //     // var labels = document.querySelectorAll(".spec-labels")
    //     // labels.forEach(label => {
    //     //     label.style.position = 'absolute'
    //     //   });

    //     var labels = document.querySelectorAll(".spec-labels")
    //     labels.forEach((label, index) => {
    //         label.id = `spec-labels-${index}`
    //         });
    // })
    

    // index += 1  
    
}

export function trimWaveform(trackname, start,end, selectedTrackIndex, fromBar, toBar){
    
    var nameOfCuttedTrack

    if(fromBar && toBar){
        nameOfCuttedTrack = ' - bars (' + fromBar + ' - ' + toBar + ')'
    }else{
        nameOfCuttedTrack = ' - trimmed (' + start.toFixed(2) + 's - ' + end.toFixed(2) + 's)'       
    }

    // const currentTrackList = trackList()
    // currentTrackList.addTrack(nameOfCuttedTrack)
     
    //  makeWaveform(trackFromStart.value[selectedTrackIndex][5], trackFromStart.value[selectedTrackIndex][0] + nameOfCuttedTrack, start, end, fromBar, toBar)
     
     
     
    //  var trimmedTrackId = trackFromStart.value.length -2
 
    
     var segmentDuration = end - start
 
     var originalBuffer = wavesurfer[selectedTrackIndex].backend.buffer;
    

    
     var emptySegment = wavesurfer[17].backend.ac.createBuffer(
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
     wavesurfer[17].empty()
    setTimeout(() => wavesurfer[17].loadDecodedBuffer(emptySegment),0)
     
    //  wavesurfer[trimmedTrackId].spectrogram.init()
 
     api.get('/trim-audio/' + trackname + '/' + start + '/' + end + '/' + fromBar + '/' + toBar)
     .then((response) => {  
        //  getOnset(nameOfCuttedTrack + ' - ' +trackFromStart.value[selectedTrackIndex][0], trackFromStart.value[selectedTrackIndex][0] + nameOfCuttedTrack)
     })
 
 }
 export function marker(beatDuration, selectedTrackIndex){
    // numberOfBars = beatDuration
    console.log(selectedTrackIndex);
    beatDuration.forEach(function(oneBeat, id){
        wavesurfer[selectedTrackIndex].addMarker({
            time: oneBeat,
            label: id+1,
            color: "black",
        })
    })
    beatDuration.forEach(function(oneBeat, id){
        if (id == beatDuration.length-1){
            wavesurfer[selectedTrackIndex].addRegion({
                id: id+1,
                start: beatDuration[id],
                end: wavesurfer[selectedTrackIndex].getDuration(),
                drag: false,
                resize: false,
                color: "rgba(0, 0, 0, 0)"   
            })
        }

        if(id > 0){       
            wavesurfer[selectedTrackIndex].addRegion({
                id: id,
                start: beatDuration[id-1],
                end: oneBeat,
                drag: false,
                resize: false,
                color: "rgba(0, 0, 0, 0)"   
            })
        }
    })
}