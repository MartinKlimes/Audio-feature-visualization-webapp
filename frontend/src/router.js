import {createRouter, createWebHistory} from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'

import {loggedIn} from './composables/cookieHandling'

import {showAlert, closeAlert} from './composables/alerts'
import { userInfo } from './stores/globalStores';





const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        
    
        beforeEnter: async (to, from) => {
      
            let loginCheck; 
            const currentUserInfo = userInfo();

            await loggedIn()
            .then(response => {
                if (response.data.message === 'jwt is valid')
                {
                    loginCheck = true;
                    currentUserInfo.username = response.data.username;
                 
 
                    // console.log(response.data.exp);
                    
                }
            })
            // if user tries to access the home page without a valid jwt
            .catch(() => {
                loginCheck = false;
                showAlert('You need to be logged in!');
                setTimeout(closeAlert, 1500);
            });
            
            // return user to login page
            if (!loginCheck)
            {   
                currentUserInfo.username = '';
                return {name: 'Login'};
            }
        }
    
    },
    {
        path: '/signin',
        name: 'Login',
        component: Login,
    },
    {
        path: '/signup',
        name: 'Register',
        component: Register
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
