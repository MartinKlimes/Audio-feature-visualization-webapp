<script setup>

import {ref} from 'vue'
import { Icon } from '@iconify/vue';
import {showAlert, closeAlert} from '../../composables/alerts'

// import Vue router for redirects
import router from '../../router.js'
import { userInfo } from '../../stores/globalStores';
import { onClickOutside } from '@vueuse/core'
// import axios
import { api } from '../../composables/custom';
import { useI18n } from 'vue-i18n';
import PlayerBtn from './AudioPlayer.vue';


const { t, locale } = useI18n();
const currentUserInfo = userInfo();

const props = defineProps({
    uploadModalVisible: Boolean
})

function logoutUser(data)
{
    api.post('logout', data)
    .then(function (response) {
        if (response.data.message === 'logout successful') 
        {
            // if the logout was successful, redirect user to the sign in page
            showAlert('Successfully logged out.');
            setTimeout(closeAlert, 1500);
            router.push('/signin');
            
        }
    })
    .catch(function (error) {
        console.log(error);
    });
}

const menuOpen = ref(false);
const target = ref(null);

onClickOutside(target, () => 
{
    
    menuOpen.value = false;
})

const emits = defineEmits(['openUploadModal'])

</script>

<template>
    <div id="navbar" class="h-13  border-b  pl-12 pr-12 bg-white ">
        <div class="flex">
            <button title="Upload files" class="hover:bg-gray-300 rounded-md mb-1" :class="{'shadow-inner shadow-dark-200' : uploadModalVisible}"><Icon icon="ic:baseline-drive-folder-upload" :inline="true" width="35"    @click="$emit('openUploadModal')"/></button> 
    
            <PlayerBtn/>

        </div>

        <div id="user-icon" class="flex h-full items-center gap-1 hover:text-dark-50 cursor-pointer" @click="menuOpen = !menuOpen">
            <span class="font-semibold hover:text-dark-50">{{currentUserInfo.username}}</span>
            <Icon icon="ph:user-circle-light" :inline="true" width="40"/>    
        </div>
    </div>

    <div v-if="menuOpen" id="user-menu" class="absolute right-0 top-0 bg-white z-25 mt-12 mr-12 rounded-md pt-3 pb-3 text-sm flex flex-col" ref="target">
        <div class="pl-5 pr-5 pt-1 pb-1 text-sm hover:bg-true-gray-200 cursor-pointer flex gap-1">
            <Icon icon="carbon:settings" :inline="true" width="20"/>
            Profile settings
        </div>
        
        <div @click="logoutUser()" class="pl-5 pr-5 pt-1 pb-1 text-sm hover:bg-true-gray-200 cursor-pointer flex gap-1">
            <Icon icon="clarity:sign-out-line" :inline="true" width="20"/>
            {{t('button.signout')}}
        </div>
    </div>


</template>

<style scoped>
#navbar{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

</style>