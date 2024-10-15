import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to include the JWT token in the header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const getEntries = () => api.get("/entries");
export const getEntry = (id) => api.get(`/entries/${id}`);
export const createEntry = (data) => api.post("/entries", data);
export const updateEntry = (id, data) => api.put(`/entries/${id}`, data);
export const deleteEntry = (id) => api.delete(`/entries/${id}`);
export const getEntryPhotos = (id) => api.get(`/entries/${id}/photos`);
// export const uploadPhoto = (id, formData) =>
//   api.post(`/entries/${id}/photos`, formData, {
//     headers: {
//       "Content-Type": "multipart/form-data",
//     },
//   });
export const uploadPhoto = (entryId, photoData) =>
  api.post(`/entries/${entryId}/photos`, photoData);
export const getTags = () => api.get("/tags");
export const getUserProfile = () => api.get("/users/profile");

export default api;
