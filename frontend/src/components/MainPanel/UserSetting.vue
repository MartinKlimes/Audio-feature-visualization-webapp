<script setup>
import { api } from '../../composables/custom';
import { showAlert, closeAlert } from '../../composables/alerts';
import router from '../../router';
import { useI18n } from "vue-i18n";
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { Icon } from '@iconify/vue';
import LangSwitch from '../LangSwitch.vue';

const { t, locale } = useI18n();
const target = ref(null);
const emits = defineEmits(["closeUserSetting"]);

function logoutUser(data) {
  api
    .post("logout", data)
    .then(function (response) {
      if (response.data.message === "logout successful") {
        // if the logout was successful, redirect user to the sign in page
        showAlert(t("alert.logoutsuccessful"));
        setTimeout(closeAlert, 1500);
        router.push("/signin");
      }
    })
    .catch(function (error) {
      console.log(error);
    });
}


onClickOutside(target, () => {
    setTimeout(() => {
        emits('closeUserSetting')
        
    }, 10);
});

</script>


<template>

    <div
        
        id="user-menu"
        class="absolute right-0 top-0  bg-white z-25 mt-12 mr-12 rounded-md pt-3 pb-3 text-sm flex flex-col items-center"
        ref="target"
      >
        <!-- <div class="pl-5 pr-5 pt-1 pb-1 text-sm hover:bg-true-gray-200 cursor-pointer flex gap-1">
          <Icon icon="carbon:settings" :inline="true" width="20" />
          Profile settings
        </div> -->
    
        <LangSwitch/>
        <div @click="logoutUser()" class="py-1 pt-1 pb-1 text-sm hover:bg-true-gray-200 cursor-pointer flex gap-1">
          <Icon icon="clarity:sign-out-line" :inline="true" width="20" />
          {{ t("button.signout") }}
        </div>
      </div>



</template>

