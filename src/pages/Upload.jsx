import { Upload as UploadIcon, Music } from 'lucide-react'
import { useState, useRef } from 'react'
import './Upload.css'

export function Upload() {
  const [showMoodResult, setShowMoodResult] = useState(false)
  const [moodData, setMoodData] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const fileInputRef = useRef(null)

  // Handle file selection
  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      handleUpload(file)
    }
  }

  // Trigger file explorer
  const triggerFileExplorer = () => {
    fileInputRef.current?.click()
  }

  // Mock mood classification function
  const handleUpload = (file) => {
    setIsUploading(true)
    // Simulate upload and processing
    setTimeout(() => {
      setMoodData({
        mood: 'SAD',
        confidence: 82.7,
        tempo: 78,
        loudness: -12.5,
        recommendations: [
          { title: 'Someone Like You', artist: 'Adele', duration: '4:45', mood: 'Sad' },
          { title: 'Fix You', artist: 'Coldplay', duration: '4:55', mood: 'Sad' },
          { title: 'Mad World', artist: 'Gary Jules', duration: '3:08', mood: 'Sad' },
          { title: 'Hurt', artist: 'Johnny Cash', duration: '3:38', mood: 'Sad' },
          { title: 'Black', artist: 'Pearl Jam', duration: '5:43', mood: 'Sad' }
        ]
      })
      setIsUploading(false)
      setShowMoodResult(true)
    }, 2000)
  }

  return (
    <div className="upload">
      {!showMoodResult ? (
        <div className="upload-container">
          <h1>Find Songs That Match Your Mood</h1>
          <p>Upload a track and discover mood-based playlists instantly</p>
          
          <div className="upload-area" onClick={triggerFileExplorer}>
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            <div className="upload-content">
              {isUploading ? (
                <div className="upload-loading">
                  <div className="spinner"></div>
                  <p>Processing your audio...</p>
                </div>
              ) : (
                <>
                  <div className="upload-icon">
                    <UploadIcon size={48} />
                  </div>
                  <h3>
                    {selectedFile ? `Selected: ${selectedFile.name}` : 'Drop your music file here or click to browse'}
                  </h3>
                  <button className="upload-btn" onClick={(e) => { e.stopPropagation(); triggerFileExplorer(); }}>
                    <Music size={20} />
                    Select Audio File
                  </button>
                  <p className="supported-formats">Supports MP3, WAV, FLAC</p>
                </>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="mood-result-container">
          <div className="mood-classification">
            <div className="mood-header">
              <h2>Mood Classification Result</h2>
              <button className="back-button" onClick={() => {
                setShowMoodResult(false)
                setSelectedFile(null)
              }}>
                ← Upload Another
              </button>
            </div>
            
            <div className="mood-display">
              <div className="mood-badge">
                <span className="mood-text">{moodData.mood}</span>
                <span className="confidence">Confidence: {moodData.confidence}%</span>
              </div>
            </div>
            
            <div className="analysis-details">
              <h3>Audio Analysis</h3>
              <div className="analysis-grid">
                <div className="analysis-item">
                  <h4>Tempo Analysis</h4>
                  <p>{moodData.tempo} BPM - Slow tempo detected, indicating calm or melancholic mood</p>
                </div>
                <div className="analysis-item">
                  <h4>Loudness Analysis</h4>
                  <p>{moodData.loudness} dB - Lower dynamic range suggests emotional content</p>
                </div>
              </div>
            </div>
          </div>

          <section className="recommendations-section">
            <h2>🎵 Recommended Songs Based on Your Mood</h2>
            <p>Here are some songs that match the {moodData.mood.toLowerCase()} mood of your uploaded track:</p>
            
            <div className="recommendations-grid">
              {moodData.recommendations.map((song, index) => (
                <div key={index} className="recommendation-card">
                  <div className="song-artwork">
                    <div className="artwork-placeholder">🎵</div>
                  </div>
                  <div className="song-info">
                    <h4>{song.title}</h4>
                    <p>{song.artist}</p>
                    <span className="song-duration">{song.duration}</span>
                  </div>
                  <button className="play-song-btn">
                    ▶
                  </button>
                </div>
              ))}
            </div>
            
            <div className="recommendation-actions">
              <button className="create-playlist-btn">
                Create Playlist from Recommendations
              </button>
              <button className="find-more-btn">
                Find More Songs
              </button>
            </div>
          </section>
        </div>
      )}
    </div>
  )
}
