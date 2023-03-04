
import axios from 'axios';
import { getCookie }from '../frontend/src/cookieHandling'

export const api = axios.create({
    withCredentials: true,
    baseURL: 'http://127.0.0.1:5000/',
    

    
});

export const updateRecording = (record_name, column, new_value) => {
    api.post('/update-recording', {
    record_name: record_name,
    column: column,
    new_value: new_value
    }, { 
    headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
        'Content-Type': 'application/json',
    }})
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }