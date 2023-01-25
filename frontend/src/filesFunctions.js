
import { api } from '../custom';
import {getCookie} from './cookieHandling'
import { trackList } from './globalStores';
import { track, makeWaveform, wavesurfer, trackFromStart } from './Waveform'



let timeAnnotation = []
let onset_detection = []

const axiosConfig = {
    headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        'Content-Type': 'multipart/form-data',    
      

    },
}

if(JSON.parse(localStorage.getItem('onset_detection'))){
    onset_detection = JSON.parse(localStorage.getItem('onset_detection'))
}
if(JSON.parse(localStorage.getItem('timeAnnotation'))){
    timeAnnotation = JSON.parse(localStorage.getItem('timeAnnotation'))
}


export const changeBackground = name => {
    trackFromStart.value.forEach(element => {
        document.getElementById(`waveform-${element[0].replace(/\.|\(|\)|\ /g, '')}`).style.backgroundColor = "white"
        if(document.getElementById(`audioList-${element[0]}`)){
            document.getElementById(`audioList-${element[0]}`).style.backgroundColor = "rgba(221, 225, 227)"
        }
    })
    if(document.getElementById(`waveform-${name.replace(/\.|\(|\)|\ /g, '')}`)){
        document.getElementById(`waveform-${name.replace(/\.|\(|\)|\ /g, '')}`).style.backgroundColor = "rgba(221, 225, 227)"
        if(document.getElementById(`audioList-${name}`)){
        document.getElementById(`audioList-${name}`).style.backgroundColor = "gray"
        }
    }
}

// export function getTrackList(){
//     const currentTrackList = trackList();
//     api.get('http://127.0.0.1:5000/get-track-list')
//     .then((response) => {   
//         let trackName = []
//         trackName.push(response.data) 
//         currentTrackList.trackName = trackName
//         // currentTrackList.addToTrackList(response.data)
//     })
// }

// function hideWaveform(id){ 
//     document.getElementById(`timeline-${id}`).style.display = "none"
//     document.getElementById(`waveform-${id}`).style.display = "none"
//     document.getElementById(`showWaveBtn-${id}`).style.display = "block"

// }
// function showWaveform(id){ 
//     document.getElementById(`timeline-${id}`).style.display = "block"
//     document.getElementById(`waveform-${id}`).style.display = "block"
//     document.getElementById(`hideWaveBtn-${id}`).style.display = "inline"
//     document.getElementById(`showWaveBtn-${id}`).style.display = "none"
// }
// function hideSpectrogram(id){ 
//     document.getElementById(`spectrogram-${id}`).style.display = "none"
//     document.getElementById(`showSpectBtn-${id}`).style.display = "block"
// }
// function showSpectrogram(id){ 
//     document.getElementById(`spectrogram-${id}`).style.display = "block"
//     document.getElementById(`hideSpectBtn-${id}`).style.display = "inline"
//     document.getElementById(`showSpectBtn-${id}`).style.display = "none"
    
// }
export function showVolume(id){
    if(id == undefined){
        document.getElementById("volume-showed").style.display = "inline"
        document.getElementById("volume-btnOn").style.display = "none"
        document.getElementById("volume-btnOff").style.display = "inline"

        var volumeInput = document.getElementById("volume-slider");
        var onChangeVolume = function (e) {
            for (let i = 0; i < wavesurfer.length; i++){
                wavesurfer[i].setVolume(e.target.value);
                
            }
        };
        volumeInput.addEventListener('input', onChangeVolume);
        volumeInput.addEventListener('change', onChangeVolume);
    }else{
        document.getElementById(`volume-showed-${id}`).style.display = "inline"
        document.getElementById(`volume-btnOff-${id}`).style.display = "inline"
        document.getElementById(`volume-btnOn-${id}`).style.display = "none"

        var volumeInput = document.getElementById(`volume-slider-${id}`);
        var onChangeVolume = function (e) {
        wavesurfer[id].setVolume(e.target.value);

        };
        volumeInput.addEventListener('input', onChangeVolume);
        volumeInput.addEventListener('change', onChangeVolume);
    }
}
export function hideVolume(id){
    if(id == undefined){
    
        document.getElementById("volume-showed").style.display = "none"
        document.getElementById("volume-btnOn").style.display = "inline"
        document.getElementById("volume-btnOff").style.display = "none"

    }else{
    document.getElementById(`volume-showed-${id}`).style.display = "none"
    document.getElementById(`volume-btnOff-${id}`).style.display = "none"
    document.getElementById(`volume-btnOn-${id}`).style.display = "inline"
}

}
// function muteVolumeBtn(id){
//     document.getElementById(`volume-mute-${id}`).style.display = "none"
//     document.getElementById(`volume-unMute-${id}`).style.display = "inline"
// }
// function unMuteVolumeBtn(id){
//     document.getElementById(`volume-mute-${id}`).style.display = "inline"
//     document.getElementById(`volume-unMute-${id}`).style.display = "none"
// }
// function playVolumeBtn(id){
    
//     document.getElementById(`playPause-btnOn-${id}`).style.display = "none"
//     document.getElementById(`playPause-btnOff-${id}`).style.display = "inline"
// }
// function pauseVolumeBtn(id){
//     document.getElementById(`spectCursor-${id}`).style.marginLeft =`0px` 
//     document.getElementById(`playPause-btnOn-${id}`).style.display = "inline"
//     document.getElementById(`playPause-btnOff-${id}`).style.display = "none"
// }

export function playAll(){
    document.getElementById("playBtn").style.display = "none"
    document.getElementById("pauseBtn").style.display = "inline"
    for (let i = 0; i < wavesurfer.length; i++){
        wavesurfer[i].play()
        document.getElementById(`playPause-btnOn-${i}`).style.display = "none"
        document.getElementById(`playPause-btnOff-${i}`).style.display = "inline"

        wavesurfer[i].on('finish', function () {
            document.getElementById("playBtn").style.display = "inline"
            document.getElementById("pauseBtn").style.display = "none"
            document.getElementById(`playPause-btnOn-${i}`).style.display = "inline"
            document.getElementById(`playPause-btnOff-${i}`).style.display = "none"
        });
    }
}
export function pauseAll(){
    
    document.getElementById("playBtn").style.display = "inline"
    document.getElementById("pauseBtn").style.display = "none"
    for (let i = 0; i < wavesurfer.length; i++){
        wavesurfer[i].pause()
        document.getElementById(`playPause-btnOn-${i}`).style.display = "inline"
        document.getElementById(`playPause-btnOff-${i}`).style.display = "none"
    }
}
export function stopAll(){
    document.getElementById("playBtn").style.display = "inline"
    document.getElementById("pauseBtn").style.display = "none"
    console.log(wavesurfer[0].drawer.lastPos)
    for (let i = 0; i < wavesurfer.length; i++){
        wavesurfer[i].stop()
        document.getElementById(`playPause-btnOn-${i}`).style.display = "inline"
        document.getElementById(`playPause-btnOff-${i}`).style.display = "none"
        document.getElementById(`spectCursor-${i}`).style.marginLeft = `0px` 
    }
}
export function muteAll(){
    for (let i = 0; i < wavesurfer.length; i++){
        wavesurfer[i].toggleMute()
    }
    if(document.getElementById("volume-unMute").style.display == "inline"){
        document.getElementById("volume-unMute").style.display = "none"
        document.getElementById("volume-mute").style.display = "inline"
    }else{
        document.getElementById("volume-mute").style.display = "none"
        document.getElementById("volume-unMute").style.display = "inline"
    }
}
export function showIOIBtnIBIBtn(id){
    if (document.getElementById(`onset-line-${id}`)){
        if (document.getElementById(`onset-line-${id}`).hidden == false){
            document.getElementById('IOIbtn').className = 'btn-hover picker'
            document.getElementById('showVolumeIOI').className = ''
        } else {
            document.getElementById('IOIbtn').className = 'btn-hover'
            document.getElementById('showVolumeIOI').className = 'hidden'
        }
    }else {
        document.getElementById('showVolumeIOI').className = 'hidden'
        document.getElementById('IOIbtn').className = 'btn-hover'
        
    }

    if (document.getElementById(`beats-line-${id}`)){
        if (document.getElementById(`beats-line-${id}`).hidden == false){
            document.getElementById('IBIbtn').className = 'btn-hover picker'
            document.getElementById('showVolumeIBI').className = ''
        } else {
            document.getElementById('IBIbtn').className = 'btn-hover'
            document.getElementById('showVolumeIBI').className = 'hidden'
        }
    } else{
        document.getElementById('IBIbtn').className = 'btn-hover'
        document.getElementById('showVolumeIBI').className = 'hidden'

    }
}




// function getTrimmedAudio(from,to,selectedTrackIndex, fromBar, toBar){

//     axios.get('/get-trimmed-audio/' + track[selectedTrackIndex] + '/' + from + '/' + to + '/' + fromBar + '/' + toBar)
//     .then((response) => {   

//         getTrackList()
//         let audio = new Audio(response.request.responseURL);
       

//         if(fromBar && toBar){
//             makeWaveform(audio,'_'+track[selectedTrackIndex] + '(bars ' + fromBar + '-' + toBar + ')')
//         }else{
//             makeWaveform(audio,'_'+track[selectedTrackIndex] + '(trim. ' + from.toFixed(2) + '-' + to.toFixed(2) + ')')
//         }
//         hideWaveform(selectedTrackIndex)
     

//         if (document.getElementById(`spectrogram-${selectedTrackIndex}`).style.display = "block"){
//             hideSpectrogram(selectedTrackIndex)
//         } 
//     })
//     getPianoroll(selectedTrackIndex, from, to)
// }

export function addTxtFilesToUpload(selectedTrackIndex, trackName){

    const file = document.getElementById("added-textFile").files;
    let formData = new FormData();
    formData.append("file", file[0]);
    
    api.post('/upload-text-file/' + trackName, formData, axiosConfig)
    .then(function (response) {
    
        let oneAnnotationFile = timeAnnotation.filter(oneFile => oneFile[0] == trackName)
  
        if(oneAnnotationFile.length != 0){
            wavesurfer[selectedTrackIndex].clearRegions()
            wavesurfer[selectedTrackIndex].clearMarkers()
            timeAnnotation.splice(timeAnnotation.indexOf(oneAnnotationFile[0]),1)
        }

        timeAnnotation.push([trackName, response.data])
        localStorage.setItem(`timeAnnotation`, JSON.stringify(timeAnnotation))

        marker(response.data, selectedTrackIndex)
        document.getElementById("added-textFile").value = ""    
});
}
export function getAudioFile(trackname){ 

    let trackAlreadyExist = trackFromStart.value.filter(oneTrack => oneTrack[0] == trackname && oneTrack[1] == undefined) //only one same record can be loaded
 
    if (trackAlreadyExist.length == 0){
     
        getOnset(trackname, trackname)
        api.get('/get-audio-file/' + trackname,axiosConfig)
        .then((response) => {
            console.log(response)
            let audioSrc = response.request.responseURL
         
            makeWaveform(audioSrc,trackname)

            api.post('/upload-text-file/' + trackname,null, axiosConfig)
            .then((response) => {
            
                if(response.data.length != 0){
                    let oneAnnotationFile = timeAnnotation.filter(oneFile => oneFile[0] == trackname)
                    if(oneAnnotationFile.length != 0){
                        timeAnnotation.splice(timeAnnotation.indexOf(oneAnnotationFile[0]),1)   
                    }
                    timeAnnotation.push([trackname, response.data])
                    localStorage.setItem(`timeAnnotation`, JSON.stringify(timeAnnotation))  
                }
            })
        })
    }
}
export const getOnset = (trackname, nameInStorage) => {
    api.get('get-onset-detection/' + trackname)
    .then((response) => {
           
        onset_detection.push([nameInStorage, response.data])
        localStorage.setItem(`onset_detection`, JSON.stringify(onset_detection))  
    })
}
 
    // let trackNameWithoutExtension = trackname.substring(0, trackname.lastIndexOf('.')) || trackname)
    


