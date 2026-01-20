import axios from "axios";

const BASE_URL = "http://localhost:8000"; // MELIXA API Gateway

// health check
export const checkBackend = async () => {
  const res = await axios.get(`${BASE_URL}/health`);
  return res.data;
};

// audio upload (main feature) - MELIXA predict endpoint
export const uploadAudio = async (file) => {
  const formData = new FormData();
  formData.append("audio", file); // Changed from "file" to "audio" for MELIXA

  const res = await axios.post(
    `${BASE_URL}/predict`, // Changed from "/analyze" to "/predict"
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: 60000 // 60 second timeout
    }
  );

  return res.data;
};

// get recommendations - MELIXA includes recommendations in predict response
export const getRecommendations = async (mood) => {
  // This is handled by the uploadAudio response in MELIXA
  // But keeping for compatibility
  const res = await axios.get(`${BASE_URL}/api/deam-info`);
  return res.data;
};

// get playlists - MELIXA doesn't have playlists, but keeping for compatibility
export const getPlaylists = async () => {
  const res = await axios.get(`${BASE_URL}/api/info`);
  return res.data;
};

// create playlist - MELIXA doesn't have playlists, but keeping for compatibility
export const createPlaylist = async (playlistData) => {
  // Placeholder for MELIXA compatibility
  return { message: "Playlist feature not available in MELIXA" };
};
