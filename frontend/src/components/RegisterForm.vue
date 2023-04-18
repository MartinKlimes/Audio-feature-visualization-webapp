<script setup>

import { useI18n } from 'vue-i18n';

import { reactive, ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs } from '@vuelidate/validators'
import { api } from '../composables/custom';

import {showAlert, closeAlert} from '../composables/alerts'

// import Vue router for redirects
import router from '../router.js'


// localization
const { t, locale } = useI18n();

// validation
const formData = reactive({
    email: '',
    username: '',
    password: '',
    passwordRepeat: '',
});

// validation rules must be also reactive
const rules = computed(() => {
    return {
    email: {required, email},
    username: { required, lengthCheck: minLength(3) },
    password: { required, lengthCheck: minLength(6), passwordMatch: sameAs(formData.passwordRepeat)},
    passwordRepeat: { required, lengthCheck: minLength(6), passwordMatch: sameAs(formData.password)}
    }
});

const v$ = useVuelidate(rules, formData);

function registerNewUser(data)
{
    api.post('register', data)
    .then(function (response) {
        if (response.data.message === 'registration successful') {
            // if the register was successful, redirect user to login page
            router.push('/signin');
            // 
            showAlert(t('register.registersuccess'));
            setTimeout(closeAlert, 3500);
        }

        // if (response.data.message === 'email and username aleready exist') {
        //     alertData.message = t('alert.wrongpassword')
        //     setTimeout(closeAlert, 1500);
        // }

        if (response.data.message === 'email already exists') {
            showAlert(t('alert.emailexists'))
            setTimeout(closeAlert, 1500);
        }
        if (response.data.message === 'username already exists') {
            showAlert(t('alert.usernameexists'));
            setTimeout(closeAlert, 1500);
        }
    })
    .catch(function (error) {
        // handle register error
        showAlert(error.message + '.');
        setTimeout(closeAlert, 1500);
    });
};

</script>

<template>

<form class="w-full bg-dark-500 bg-opacity-50 blur-sm pl-25 pr-25 pt-5 pb-5 text-white" id="register-form">

    <span class="text-3xl mb-5">{{t('form.register')}}</span>
    <input v-model="v$.email.$model" type="email" class="input-field-nomargin border-2" :placeholder="t('form.email')"
    :class="{'border-green-400 transition duration-500': !v$.email.$invalid,
             'border-2 border-gray-300': v$.email.$invalid}"
              autocomplete="email"/>

    <div class="h-5 text-xs text-white mb-1 mt-1">
        <div v-if="v$.email.$error">
            <span v-if="v$.email.$errors[0].$validator === 'email'">
                {{t('register.emailbadformat')}}
            </span>
        </div>
    </div>
    
    <input v-model="v$.username.$model" type="text" class="input-field-nomargin border-2" :placeholder="t('form.username')"
    :class="{'border-green-400 transition duration-500': !v$.username.$invalid,
             'border-2 border-gray-300': v$.username.$invalid}"
              autocomplete="username"/>
    
    <div class="h-5 text-xs text-white mb-1 mt-1">
        <div v-if="v$.username.$error">
            <span v-if="v$.username.$errors[0].$validator === 'lengthCheck'">
                {{t('register.usernametooshort')}}
            </span>
        </div>
    </div>
    
    <input v-model="v$.password.$model" type="password" class="input-field-nomargin border-2" :placeholder="t('form.pswd')"
    :class="{'border-green-400 transition duration-500': !v$.password.$invalid,
             'border-2 border-gray-300': v$.password.$invalid}"
              autocomplete="new-password"/>

    <div class="h-5 text-xs text-white mb-1 mt-1">
        <div v-if="v$.password.$error">
            <span v-if="v$.password.$errors[0].$validator === 'lengthCheck'">
                {{t('register.pswdtooshort')}}
            </span>
            <span v-if="v$.password.$errors[0].$validator === 'passwordMatch'">
                {{t('register.pswdnomatch')}}
            </span>
        </div>
    </div>
    
    <input v-model="v$.passwordRepeat.$model" type="password" class="input-field-nomargin border-2" :placeholder="t('form.pswdagain')" 
    :class="{'border-green-400 transition duration-500': !v$.passwordRepeat.$invalid,
             'border-2 border-gray-300': v$.passwordRepeat.$invalid}"
              autocomplete="new-password"/>

    <div class="h-5 text-xs text-white mb-1 mt-1">
        <div v-if="v$.passwordRepeat.$error">
            <span v-if="v$.passwordRepeat.$errors[0].$validator === 'lengthCheck'">
                {{t('register.pswdtooshort')}}
            </span>
            <span v-if="v$.passwordRepeat.$errors[0].$validator === 'passwordMatch'">
                {{t('register.pswdnomatch')}}
            </span>
        </div>
    </div>


    <div v-if="!v$.email.$invalid && !v$.username.$invalid && !v$.password.$invalid && !v$.passwordRepeat.$invalid">
        <button type="button" @click="registerNewUser(formData)" class="btn btn-blue">{{t('button.signup')}}</button>
    </div>
    <div v-else>
        <button type="button" class="btn btn-disabled">{{t('button.signup')}}</button>
    
    </div>
        <div class="text-white mt-10 font-semibold">
        {{t('register.alreadyregistered')}}
        <router-link :to="{name: 'Login'}" class="text-green-400 hover:text-white">{{t('register.gologin')}}</router-link>
    </div>
</form>

</template>

<style scoped>

#register-form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

input:focus {
    outline: 2px solid rgba(255, 255, 255, 0.2);
}


</style>