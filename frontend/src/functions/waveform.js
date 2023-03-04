
import WaveSurfer from "wavesurfer.js";
import TimelinePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.min.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.regions.min.js';
import Cursor from '../functions/cursor/index';
import Markers from 'wavesurfer.js/dist/plugin/wavesurfer.markers.min.js';
import Spectrogram from '../functions/index';
import {createVerticalKeyboard} from './useMidiPianoroll'
// import colormapJSON from '../hot-colormap.json'
import { api } from "../../custom";
import { trackList } from "../globalStores";
import colormap from "colormap"


let colors = colormap({
    colormap: 'jet',
    nshades: 256,
    format: 'float',
    alpha: 1
})

export var wavesurfer = []
export function createWavesurfer(audio,trackName, id, setwaveColor = 'violet', setprogressColor = 'purple', isSplitChannels = false){
   
    wavesurfer[id] = WaveSurfer.create({
    container: `#waveform-${id}`,
    backend: 'WebAudio',
    splitChannels: isSplitChannels,
    waveColor: setwaveColor,
    progressColor: setprogressColor,
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
            
        //     container: `#spectrogram`,
        //     colorMap: colors,
        //     fftSamples: 2048,
        //     height: 256,
        //     labels: true,
        //     frequencyMax: 12000,
        //     windowFunc: 'hann',
        //     splitChannels: false,
        //     frequenciesDataUrl: 'http://127.0.0.1:5000/get-spectrogram/9904__snoman__grass1.wav',
        
            
        
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
        currentTrackList.selectTrack(id).waveform.isWaveformLoading = false
        currentTrackList.selectTrack(id).spectrogram.plotSpectrogram = true

        if(document.getElementById(`pianoroll-${id}`)){
            const width = wavesurfer[id].drawer.width / document.getElementById(`pianoroll-player-${id}`).duration
            createVerticalKeyboard(id, width)
            // pianorollPlayer.addVisualizer(pianoroll);
        }
        
    });

    // wavesurfer[id].on('scroll', function (e) {
    //     const pianoroll = document.getElementById(`pianoroll-${id}`)
    //     const xpos = `${wavesurfer[id].drawer.lastPos - wavesurfer[id].drawer.wrapper.scrollLeft}px`

    //     if(pianoroll){
    //         pianoroll.getElementsByTagName('div')[2].scrollLeft = e.target.scrollLeft
    //         document.getElementById(`pianoroll-liveCursor-${id}`).style.left = xpos

    //     }
    //     if(wavesurfer[id].spectrogram){
    //         document.getElementById(`spectrogram-liveCursor-${id}`).style.left = xpos
    //         document.querySelector(`.spec-labels-${id}`).style.marginLeft  = `${(e.target.scrollLeft)}px` 
    //         document.querySelector(`.spec-legend-${id}`).style.marginRight  = `${-(e.target.scrollLeft)}px` 
    //     }

    // });
   
    // wavesurfer[id].on('interaction', () => {
    //     setTimeout(() => {
    //         const xpos = `${wavesurfer[id].drawer.lastPos - wavesurfer[id].drawer.wrapper.scrollLeft}px`
    //         if (document.getElementById(`spectrogram-liveCursor-${id}`)) {
    //             document.getElementById(`spectrogram-liveCursor-${id}`).style.left = xpos
    //         }
    //         if (document.getElementById(`pianoroll-liveCursor-${id}`)) {
    //             document.getElementById(`pianoroll-liveCursor-${id}`).style.left = xpos
    //         }
    //     }, 0);
    // })
    wavesurfer[id].on('scroll', updateCursorPosition.bind(this, id));
wavesurfer[id].on('interaction', () => setTimeout(updateCursorPosition.bind(this, id), 0));

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
const updateCursorPosition = (id) => {
    const xpos = `${wavesurfer[id].drawer.lastPos - wavesurfer[id].drawer.wrapper.scrollLeft}px`;
    const liveCursorSpec = document.getElementById(`spectrogram-liveCursor-${id}`);
    
    const liveCursorPiano = document.getElementById(`pianoroll-liveCursor-${id}`);
    const pianoroll = document.getElementById(`pianoroll-${id}`)
    if (liveCursorSpec) {
      liveCursorSpec.style.left = xpos;
      document.querySelector(`.spec-labels-${id}`).style.marginLeft = `${wavesurfer[id].drawer.wrapper.scrollLeft}px`;
      document.querySelector(`.spec-legend-${id}`).style.marginRight = `${-wavesurfer[id].drawer.wrapper.scrollLeft}px`;
    }
    if (liveCursorPiano) {
      liveCursorPiano.style.left = xpos;
      pianoroll.getElementsByTagName('div')[2].scrollLeft = wavesurfer[id].drawer.wrapper.scrollLeft;
    }
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