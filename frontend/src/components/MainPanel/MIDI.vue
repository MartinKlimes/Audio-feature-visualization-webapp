<script setup>
import { trackIndex } from '../../globalStores';
import { api } from '../../../custom';
import { getCookie } from '../../cookieHandling';
import { wavesurfer } from '../../Waveform';

const globalTrackIndex = trackIndex()

const axiosConfig = {
    headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        'Content-Type': 'multipart/form-data'
        },
}

function addMidiToUpload(selectedTrackIndex){
    
    const file = document.getElementById("added-midiFile").files;
    let formData = new FormData();
    formData.append("file", file[0]);


    api.post('/get-midi', formData, axiosConfig)
    .then((response) =>  {
        getPianoroll(selectedTrackIndex)
    })
}
function getPianoroll(selectedTrackIndex, from, to){
    document.getElementById(`pianoroll-${selectedTrackIndex}`).style.width = `${(wavesurfer[selectedTrackIndex].drawer.wrapper.scrollWidth -86)}px`
    api.get('get-pianoroll/' + from + '/' + to)
    .then((response) => {
        console.log(response)
        
        document.getElementById(`IMGpianoroll-${selectedTrackIndex}`).src = response.request.responseURL
    })
}

</script>






<template>
<div>
    <label for="added-midiFile" class="hover:cursor-pointer">
        <div id="add-midi-btn" class="btn-hover">Upload MIDI</div>
    </label>
    <input id="added-midiFile" type="file" class="hidden" accept=".mid" multiple
    @change="addMidiToUpload(globalTrackIndex.selTrackIndex)">
</div>
</template>