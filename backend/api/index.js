const express = require('express');
const multer = require('multer');
const axios = require('axios');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Enable CORS for all origins
app.use(cors());

// Configure multer for file uploads
const upload = multer({ 
  dest: 'uploads/',
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB limit (increased from 50MB)
  }
});

// FastAPI ML service URL
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'API Gateway is running', timestamp: new Date().toISOString() });
});

// Proxy prediction endpoint
app.post('/predict', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    // Create form data to forward to ML service
    const FormData = require('form-data');
    const formData = new FormData();
    formData.append('audio', fs.createReadStream(req.file.path), req.file.originalname);

    // Forward request to FastAPI ML service
    const response = await axios.post(`${ML_SERVICE_URL}/predict`, formData, {
      headers: {
        ...formData.getHeaders(),
      },
      timeout: 60000 // 60 second timeout
    });

    // Clean up uploaded file
    fs.unlinkSync(req.file.path);

    // Return the ML service response
    res.json(response.data);

  } catch (error) {
    // Clean up uploaded file if it exists
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }

    console.error('Prediction error:', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: 'ML service is unavailable' });
    } else if (error.code === 'ECONNABORTED') {
      res.status(408).json({ error: 'Request timeout' });
    } else {
      res.status(500).json({ 
        error: 'Internal server error',
        details: error.message 
      });
    }
  }
});

// Proxy DEAM audio streaming endpoint
app.get('/deam_audio/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    
    // Stream audio from ML service
    const response = await axios.get(`${ML_SERVICE_URL}/deam_audio/${filename}`, {
      responseType: 'stream'
    });

    // Set appropriate headers
    res.set({
      'Content-Type': 'audio/mpeg',
      'Accept-Ranges': 'bytes',
      'Cache-Control': 'no-cache'
    });

    // Pipe the audio stream
    response.data.pipe(res);

  } catch (error) {
    console.error('Audio streaming error:', error.message);
    
    if (error.response && error.response.status === 404) {
      res.status(404).json({ error: 'Audio file not found' });
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: 'ML service is unavailable' });
    } else {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});

// Proxy info endpoints
app.get('/api/info', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/api/info`);
    res.json(response.data);
  } catch (error) {
    console.error('Info endpoint error:', error.message);
    res.status(500).json({ error: 'Failed to fetch info' });
  }
});

app.get('/api/deam-info', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/api/deam-info`);
    res.json(response.data);
  } catch (error) {
    console.error('DEAM info endpoint error:', error.message);
    res.status(500).json({ error: 'Failed to fetch DEAM info' });
  }
});

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir);
}

// Start server
app.listen(PORT, () => {
  console.log(`MELIXA API Gateway running on port ${PORT}`);
  console.log(`ML Service URL: ${ML_SERVICE_URL}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});
