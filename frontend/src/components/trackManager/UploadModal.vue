<script setup>
import TrackManager from "./TrackManager.vue";
import { trackList} from "../../stores/globalStores";
import { storeToRefs } from "pinia";
import { Icon } from "@iconify/vue";
import { onMounted, reactive } from "vue";
import { ref } from "vue";
import { getCookie } from "../../cookieHandling";
import { api } from "../../../custom";
import { showAlert, closeAlert } from "../../alerts";
import { onClickOutside } from "@vueuse/core";

const currentTrackList = trackList();

const emits = defineEmits(['closeUploadModal'])


let fileNameList = reactive([]);
let fileList = [];
let isUploaded = ref([]);
const target = ref(null);

const isDragover = ref(false);

function addFilesToUpload() {
  const files = document.getElementById("added-files").files;

  for (let i = 0; i < files.length; i++) {
    if (!fileNameList.includes(files[i].name)) {
      fileNameList.push(files[i].name);
      fileList.push(files[i]);
      isUploaded.value.push(false);
    }
  }
}

function removeFileFromList(filename) {
  const fileToRemove = fileNameList.indexOf(filename);
  fileList.splice(fileToRemove, 1);
  isUploaded.value.splice(fileToRemove, 1);
  fileNameList.splice(fileToRemove, 1);
}

function clearFileList() {
  fileNameList.splice(0);
  fileList = [];
  isUploaded.value = [];
}

function uploadAllFiles() {
  if (fileList.length > 0) {
    for (let i = 0; i < fileList.length; i++) {
      uploadOneFile(fileList[i], i);
    }
  }
}
// progress bar načítání podle dat ze serveru ne podle css třídy

function uploadOneFile(file, id) {
  if (!isUploaded[id]) {
    let formData = new FormData();
    formData.append("file", file);
    const fileProgressBar = document.getElementById(`progress-bar-${id}`);

    const uploadCheck = document.getElementById(`upload-check-${id}`);

    function fileUploadProgress(event) {
      const percentage = Math.round((100 * event.loaded) / event.total);
      fileProgressBar.style.width = percentage + "%";
    }
    // axios request config
    const axiosConfig = {
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: fileUploadProgress,
    };
    
    // axios.post(url, data, config)
    // let type
    // if (file.type.match("audio/*")) {
    //   type = 'audio'
    // } else if (file.type == 'text/plain'){
    //   type = 'txt'
    // } else if (file.type == 'audio')
    api
      .post("upload-audio-file/" + file.type.split('/'), formData, axiosConfig)
      .then(function (response) {
        
        // uploadCheck.style.visibility = "visible";
        isUploaded.value[id] = true;
        currentTrackList.fetchRecordings();
      });
  }
}

const upload = ($event) => {
  isDragover.value = false;
  const files = $event.dataTransfer
    ? [...$event.dataTransfer.files]
    : [...$event.target.files];
    let audioTypes = "audio/*";
  console.log(files);
    for (let i = 0; i < files.length; i++) {

      if ((files[i].type.match(audioTypes) && !currentTrackList.trackState.includes(files[i].name))
        || (files[i].type == 'text/plain' && !currentTrackList.barsList.includes(files[i].name))
        || (files[i].type == 'audio/mid' && !currentTrackList.midiList.includes(files[i].name))
      ) {
        fileNameList.push(files[i].name);
        fileList.push(files[i]);
        isUploaded.value.push(false);
        }
      else {
        showAlert(`${files[i].name} is already uploaded`);
        setTimeout(closeAlert, 1500);
      } 

  }
  setTimeout(() => {
    uploadAllFiles();
  }, 0);
};


// const uploadModalElement = ref(null);
// const { x, y, style } = useDraggable(uploadModalElement, {
//    initialValue: { x: 40, y: 40 },
// })
onClickOutside(target, () => 
{
    emits('closeUploadModal')
  
})
</script>

<template>
  <section  class="flex justify-center items-center absolute top-0 left-0 w-full h-full z-22 bg-dark-600 bg-opacity-50" >
    <section class="container mx-auto mt-6" ref="target">
      <div class="md:grid md:grid-cols-3 md:gap-4">
        <div class="col-span-2">
          <TrackManager />
        </div>
        <div class="col-span-1">
          <div
            class="bg-white rounded border border-gray-200 relative flex flex-col"
          >
            <div class="px-6 pt-6 pb-5 font-bold border-b border-gray-200">
              <span class="card-title">Upload</span>
              <Icon
                icon="material-symbols:close"
                class="float-right text-2xl -m-3 hover:bg-gray-300 transition cursor-pointer"
                @click="$emit('closeUploadModal')"
              />
            </div>
            <div class="p-6">
              <label for="added-files">
                <!-- Upload Dropbox -->
                <div
                  class="w-full px-10 py-20 rounded text-center cursor-pointer border border-dashed border-gray-400 text-gray-400 transition duration-500 hover:text-white hover:bg-green-400 hover:border-green-400 hover:border-solid"
                  :class="{
                    'bg-green-400 border-green-400 border-solid': isDragover,
                  }"
                  @drag.prevent.stop=""
                  @dragstart.prevent.stop=""
                  @dragend.prevent.stop="isDragover = false"
                  @dragover.prevent.stop="isDragover = true"
                  @dragenter.prevent.stop="isDragover = true"
                  @dragleave.prevent.stop="isDragover = false"
                  @drop.prevent.stop="upload($event)"
                >
                  <Icon icon="uil:upload" class="text-2xl" /> <br />
                  <h5>Choose a file or drag it here</h5>
                  <input
                    id="added-files"
                    type="file"
                    class="hidden"
                    accept="audio/*, .txt, .mid"
                    multiple
                    @change="upload($event), ($event.target.value = '')"
                  />
                </div>
              </label>
              <hr class="my-6 "  />
              <!-- Progess Bars -->
              <div class="h-auto max-h-72 overflow-y-auto">
              <div
                v-for="(filename, i) in fileNameList"
                :id="`file-${i}`"
                :key="filename"
                
              >
                <div class="mb-4">
                  <!-- File Name -->
                  <div
                    class="font-bold text-sm"
                    :class="{ 'text-green-600': isUploaded[i] }"
                  >
                    <Icon
                      icon="fa:spinner"
                      class="spin"
                      :class="{ hidden: isUploaded[i] }"
                    />
                    {{ filename }}
                    <Icon icon="fa:check" :class="{ hidden: !isUploaded[i] }" />
                  </div>
                  <div class="flex h-4 overflow-hidden bg-gray-200 rounded">
                    <!-- Inner Progress Bar -->
                    <div
                      :id="`progress-bar-${i}`"
                      class="transition-all progress-bar bg-blue-400"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- <div id="upload-modal" class=" bg-white w-[60rem] h-[40rem] z-20 rounded-md flex flex-col justify-center items-center">
        <div class="h-[3rem] w-full rounded-t-md border-b flex justify-between items-center px-5">
            <span class="text-base select-none">Add new tracks</span>
            <Icon @click="closeUploadModal()"  icon="ci:close-big" :inline="true" width="20" class="cursor-pointer hover:text-dark-50 transition"/>
        </div>

        <div class="h-[calc(100%-6rem)] w-full rounded-b-md overflow-y-scroll flex flex-col items-left p-5 select-none">
            <div v-for="(filename, i) in fileNameList" :id="`file-${i}`" :key="filename" class="bg-true-gray-200 py-1 px-2 mb-1 rounded-md w-full text-sm flex">
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

        <div class="h-3rem w-full rounded-b-md flex justify-between items-center px-5 border-t">
            <label for="added-files" class="hover:cursor-pointer">
                <div id="add-files-btn" class="btn btn-blue">Add audio files from disk</div>
            </label>
            
            <input id="added-files" type="file" class="hidden" accept="audio/*" multiple 
                @change="addFilesToUpload()" 
                @click="$event.target.value=''">
            <button id="delete-all-btn" class="btn btn-blue" @click="clearFileList()">Remove all files</button>
            <button id="upload-btn" class="btn btn-blue" @click="uploadAllFiles()">Upload</button>


        </div>
    </div> -->
  </section>
</template>

<style scoped>
.check-icon {
  visibility: hidden;
}
/* .progress-bar {
  width: 0%;
  transition: width 0.01s linear;
} */

a {
  transition: all 0.15s ease;
}

/* text-yellow-500 */
a:hover {
  color: #f59e0b;
  text-decoration: none;
}

.text-orange {
  color: #f59e0b !important;
  fill: #f59e0b !important;
}

.card-header .fa.text-orange,
.card .card-header .fas.text-orange {
  color: #ff5e3a;
  fill: #ff5e3a;
}

.introduction-bg {
  animation: slide 50s linear infinite;
  will-change: background-position;
  z-index: -1;
}

#playlist li:first-child {
  padding-top: 25px;
}

.upload-dropbox.upload-dropbox-drag {
  color: #fff;
  background-color: #20d862;
  border-color: #20d862;
  border-style: solid;
}

input[type="file"] {
  margin-top: 20px;
}

.progress-bar {
  background-size: 1rem 1rem;
  background-image: linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.15) 75%,
    transparent 75%,
    transparent
  );
  animation: progress-bar-stripes 1s linear infinite;
}

.music-bg {
  animation: slide 50s linear infinite;
  will-change: background-position;
}

@keyframes progress-bar-stripes {
  0% {
    background-position: 1rem 0;
  }
  100% {
    background-position: 0 0;
  }
}

@keyframes slide {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: -4000px 0;
  }
}
</style>
<style>
.spin {
  animation-name: spin;
  animation-duration: 2000ms;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

</style>

