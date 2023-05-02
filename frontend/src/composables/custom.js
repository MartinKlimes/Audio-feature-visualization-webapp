import axios from "axios";
import { getCookie } from "./cookieHandling";

export const api = axios.create({
  withCredentials: true,
  baseURL: "https://audio-feature-visualization.onrender.com/",
});

export const updateRecording = (record_id, column, new_value, visualization_type) => {
  api
    .put(
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
