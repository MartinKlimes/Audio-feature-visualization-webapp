

import { api } from './custom';

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


function loggedIn() {
    const axiosConfig = {
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            'Content-Type': 'application/json',
        }
    }
    
    const response = api.get('login-check', axiosConfig);
    return response;
}

export {getCookie, loggedIn};