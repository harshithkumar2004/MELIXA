const express = require('express');
const multer = require('multer');
const axios = require('axios');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());

const upload = multer({ 
  dest: 'uploads/',
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB limit (increased from 50MB)
  }
});

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

app.get('/health', (req, res) => {
  res.json({ status: 'API Gateway is running', timestamp: new Date().toISOString() });
});

app.post('/predict', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    const FormData = require('form-data');
    const formData = new FormData();
    formData.append('audio', fs.createReadStream(req.file.path), req.file.originalname);

    const response = await axios.post(`${ML_SERVICE_URL}/predict`, formData, {
      headers: {
        ...formData.getHeaders(),
      },
      timeout: 60000 
    });
    
    fs.unlinkSync(req.file.path);

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

app.get('/deam_audio/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    
    const response = await axios.get(`${ML_SERVICE_URL}/deam_audio/${filename}`, {
      responseType: 'stream'
    });

    res.set({
      'Content-Type': 'audio/mpeg',
      'Accept-Ranges': 'bytes',
      'Cache-Control': 'no-cache'
    });
    
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

const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir);
}

app.listen(PORT, () => {
  console.log(`MELIXA API Gateway running on port ${PORT}`);
  console.log(`ML Service URL: ${ML_SERVICE_URL}`);
});

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});
