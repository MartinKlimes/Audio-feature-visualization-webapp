<script setup>
import { trackList, uploadModalState } from '../globalStores';
import { storeToRefs } from 'pinia'
import { Icon } from '@iconify/vue';
import { reactive } from 'vue'

import {getCookie} from '../cookieHandling'
import { api } from '../../custom';
// import { useDraggable } from '@vueuse/core'
// import { ref } from 'vue'
import { getAudioFile, getTrackList } from '../filesFunctions'

const uploadModalGlobalState = uploadModalState();
const { uploadModalVisible } = storeToRefs(uploadModalGlobalState);


function closeUploadModal() {
    uploadModalGlobalState.uploadModalVisible = false;
    getTrackList();
    clearFileList();
}

let fileNameList = reactive([]);
let fileList = [];
let isUploaded = [];

function addFilesToUpload()
{  
    const files = document.getElementById("added-files").files;
    
    
    for (let i = 0; i < files.length; i++)
    {
        if(!fileNameList.includes(files[i].name))
        {
            fileNameList.push(files[i].name);
            fileList.push(files[i]);
            isUploaded.push(false);
        }
    }
    
}


function removeFileFromList(filename)
{
    const fileToRemove = fileNameList.indexOf(filename);
    fileList.splice(fileToRemove, 1);
    isUploaded.splice(fileToRemove, 1);
    fileNameList.splice(fileToRemove, 1);
}


function clearFileList()
{
    fileNameList.splice(0);
    fileList = [];
    isUploaded = [];
}

function uploadAllFiles()
{
    
    if (fileList.length > 0)
    {
        for (let i = 0; i < fileList.length; i++)
        {
            uploadOneFile(fileList[i], i);
        }
    }
}

function uploadOneFile(file, id) 
{
    
    if (!isUploaded[id])
    {
        let formData = new FormData();
        formData.append("file", file);
        const fileProgressBar = document.getElementById(`progress-bar-${id}`);
        const uploadCheck = document.getElementById(`upload-check-${id}`);
        
        function fileUploadProgress (event) {
            const percentage = Math.round((100 * event.loaded) / event.total);
            fileProgressBar.style.width = percentage + "%";
        }
        // axios request config
        const axiosConfig = {
            headers: {
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: fileUploadProgress
        }
        // axios.post(url, data, config)
        api.post('upload-audio-file', formData, axiosConfig)
        .then(function (response) {
            uploadCheck.style.visibility = 'visible';
            isUploaded[id] = true;
        });
 

    }
    
}




// const uploadModalElement = ref(null);
// const { x, y, style } = useDraggable(uploadModalElement, {
//    initialValue: { x: 40, y: 40 },
// })

</script>

<template>
<div v-if="uploadModalVisible" class="flex justify-center items-center absolute top-0 left-0 w-full h-full  z-22 bg-dark-600 bg-opacity-50">
    <div id="upload-modal" class=" bg-white w-[60rem] h-[40rem] z-20 rounded-md flex flex-col justify-center items-center">
        <div class="h-[3rem] w-full rounded-t-md border-b flex justify-between items-center pl-5 pr-5">
            <span class="text-base select-none">Add new tracks</span>
            <Icon @click="closeUploadModal()"  icon="ci:close-big" :inline="true" width="20" class="cursor-pointer hover:text-dark-50 transition"/>
        </div>

        <div class="h-[calc(100%-6rem)] w-full rounded-b-md overflow-y-scroll flex flex-col items-left p-5 select-none">
            <div v-for="(filename, i) in fileNameList" :id="`file-${i}`" :key="filename" class="bg-true-gray-200 pt-1 pb-1 pl-2 pr-2 mb-1 rounded-md w-full text-sm flex">
                <div class="w-70">
                    {{ filename }}
                </div>
                <div class="w-[calc(100%-17.5rem)] h-full flex items-center">
                    <div class="bg-true-gray-400 m-1 rounded-md h-[40%] w-full">
                        <div :id="`progress-bar-${i}`" class="bg-dark-100 rounded-md h-full progress-bar"></div>
                    </div>
                </div>
                <div class="w-[1.5rem] flex items-center justify-center check-icon" :id="`upload-check-${i}`">
                    <Icon icon="bi:check" :inline="true" width="20"/>
                </div>
                <div class="w-[1.5rem] flex items-center justify-center hover:text-dark-50 transition cursor-pointer" @click="removeFileFromList(filename)">
                    <Icon icon="fluent:delete-48-regular" :inline="true" width="18"/>
                </div>
            </div>
        </div>

        <div class="h-[3rem] w-full rounded-b-md flex justify-between items-center pl-5 pr-5 border-t">
            <label for="added-files" class="hover:cursor-pointer">
                <div id="add-files-btn" class="btn btn-blue">Add audio files from disk</div>
            </label>
            <!-- accept only audio files -->
            <input id="added-files" type="file" class="hidden" accept="audio/*" multiple 
                @change="addFilesToUpload()" 
                @click="$event.target.value=''">
            <button id="delete-all-btn" class="btn btn-blue" @click="clearFileList()">Remove all files</button>
            <button id="upload-btn" class="btn btn-blue" @click="uploadAllFiles()">Upload</button>


        </div>
    </div>
</div>
</template>

<style scoped>
.check-icon{
    visibility: hidden;
}
.progress-bar{
    width: 0%;
    transition: width 0.1s linear;
}

</style>