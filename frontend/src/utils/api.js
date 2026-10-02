import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:3000",
});

export const uploadFiles = async (formData) => {
  const response = await API.post("/api/upload", formData);
  return response.data;
};

export const fetchMatchingScores = async () => {
  const response = await API.get("/matching-scores");
  return response.data;
};
