import axios from "axios";
import { getCookie } from "./cookieHandling";


let baseURL;
if (process.env.NODE_ENV === "production") {
  baseURL = "https://audio-feature-visualization.onrender.com/";
} else {
  baseURL = "http://127.0.0.1:5000/";
}

export const api = axios.create({
  withCredentials: true,
  baseURL: baseURL,
});

export const updateRecording = (record_id, column, new_value, visualization_type) => {
api.put(
      "/update-recording",
      {
        record_id: record_id,
        column: column,
        new_value: new_value,
        visualization_type: visualization_type,
      },
      {
        headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token"),
          "Content-Type": "application/json",
        },
      }
    )
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
};
