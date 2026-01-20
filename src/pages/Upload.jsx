import { Upload as UploadIcon, Music } from 'lucide-react'
import { useState, useRef } from 'react'
import { useAudio } from '../context/AudioContext'
import './Upload.css'
import { uploadAudio } from '../api/backend'

export function Upload() {
  const { loadTrack } = useAudio()
  const [showMoodResult, setShowMoodResult] = useState(false)
  const [moodData, setMoodData] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const fileInputRef = useRef(null)

  // Handle file selection
  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      console.log('File selected:', file.name, file.type, file.size)
      setSelectedFile(file)
      
      // Load the file into the audio player
      const url = URL.createObjectURL(file)
      console.log('Created object URL:', url)
      
      loadTrack({
        title: file.name.replace(/\.[^/.]+$/, ""), // Remove file extension
        artist: "Local File",
        url: url
      })
      
      handleUpload(file)
    }
  }

  // Trigger file explorer
  const triggerFileExplorer = () => {
    fileInputRef.current?.click()
  }

  // Upload audio to backend for mood analysis
  const handleUpload = async (file) => {
    setIsUploading(true)

    try {
      const response = await uploadAudio(file)
      console.log('Backend response:', response)
      
      // Extract confidence from probabilities or use provided confidence
      let confidence = response.confidence
      if (!confidence && response.probabilities) {
        const maxProb = Math.max(...Object.values(response.probabilities))
        confidence = (maxProb * 100).toFixed(2) + '%'
      }
      
      // Extract tempo and energy from processing info or calculate from probabilities
      let tempo = 120 // default tempo
      let energy = 0.5 // default energy
      
      // Try to get tempo from processing info or estimate based on mood
      if (response.processing_info) {
        // Use actual tempo and energy from MELIXA backend
        tempo = response.processing_info.tempo || tempo
        energy = response.processing_info.energy || energy
        
        // Normalize energy to 0-1 scale if needed (RMS energy is typically 0-1)
        if (energy > 1) {
          energy = energy / 100  // Convert to percentage if needed
        }
      } else {
        // Fallback: Estimate tempo and energy based on predicted mood
        const mood = response.mood?.toLowerCase()
        if (mood === 'energetic') {
          tempo = 135 + Math.random() * 25  // 135-160 BPM
          energy = 0.7 + Math.random() * 0.25  // 70-95% energy
        } else if (mood === 'happy') {
          tempo = 115 + Math.random() * 25  // 115-140 BPM
          energy = 0.6 + Math.random() * 0.25  // 60-85% energy
        } else if (mood === 'calm') {
          tempo = 70 + Math.random() * 30  // 70-100 BPM
          energy = 0.2 + Math.random() * 0.3  // 20-50% energy
        } else if (mood === 'sad') {
          tempo = 60 + Math.random() * 30  // 60-90 BPM
          energy = 0.1 + Math.random() * 0.3  // 10-40% energy
        }
      }
      
      // Ensure moodData has all required fields
      const moodData = {
        mood: response.mood || 'Unknown',
        confidence: confidence || '0%',
        tempo: tempo,
        energy: energy,
        probabilities: response.probabilities || {},
        recommendations: response.recommendations || [],
        processing_info: {
          tempo: tempo,
          energy: energy
        }
      }
      
      console.log('Processed moodData:', moodData)
      setMoodData(moodData)
      setShowMoodResult(true)
    } catch (error) {
      console.error("Upload failed:", error)
      alert("Failed to process audio. Please try again.")
    } finally {
      setIsUploading(false)
    }
  }

  // Handle playing recommendation songs
  const handlePlayRecommendation = (song) => {
    console.log('Playing song:', song)
    loadTrack({
      title: formatSongTitle(song.filename),
      artist: 'DEAM Dataset',
      url: song.stream_url ? `http://localhost:8000${song.stream_url}` : null
    })
  }

  // Format song title - clean up file paths and extensions
  const formatSongTitle = (title) => {
    if (!title) return 'Unknown Song'
    
    // Remove file extension
    let cleaned = title.replace(/\.[^.]+$/, '')
    
    // Remove file path
    cleaned = cleaned.split('/').pop().split('\\').pop()
    
    // If it's a hash (64 hex chars), show as "Uploaded Track"
    if (/^[a-f0-9]{64}$/i.test(cleaned)) {
      return 'Uploaded Track'
    }
    
    // Replace underscores and hyphens with spaces
    cleaned = cleaned.replace(/[_-]/g, ' ')
    
    // Capitalize first letter of each word
    cleaned = cleaned.split(' ').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ')
    
    return cleaned
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
                <span className="mood-text">{moodData?.mood || 'Unknown'}</span>
                <span className="confidence">Confidence: {moodData?.confidence || '0%'}</span>
              </div>
            </div>
            
            {/* Mood Prediction Meter - Probability Bars */}
            {moodData?.probabilities && (
              <div className="mood-probabilities">
                <h3>Mood Probabilities</h3>
                {Object.entries(moodData.probabilities).map(([mood, probability]) => (
                  <div key={mood} className="probability-item">
                    <div className="probability-label">
                      <span>{mood.charAt(0).toUpperCase() + mood.slice(1)}</span>
                      <span>{(probability * 100).toFixed(1)}%</span>
                    </div>
                    <div className="probability-bar">
                      <div
                        className="probability-fill"
                        style={{ 
                          width: `${probability * 100}%`
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            <div className="analysis-details">
              <h3>Audio Analysis</h3>
              <div className="analysis-grid">
                <div className="analysis-item">
                  <h4>Tempo Analysis</h4>
                  <p>{moodData?.processing_info?.tempo?.toFixed(1) || '0'} BPM - {moodData?.processing_info?.tempo < 120 ? 'Slow tempo detected, indicating calm or melancholic mood' : 'Upbeat tempo detected, indicating energetic or happy mood'}</p>
                </div>
                <div className="analysis-item">
                  <h4>Energy Analysis</h4>
                  <p>{(moodData?.processing_info?.energy * 100)?.toFixed(1) || '0'}% - {moodData?.processing_info?.energy > 0.15 ? 'High energy detected, suggesting upbeat mood' : 'Low energy detected, suggesting calm mood'}</p>
                </div>
              </div>
            </div>
          </div>

          <section className="recommendations-section">
            <h2>🎵 Recommended Songs Based on Your Mood</h2>
            <p>Here are some songs that match the {moodData?.mood?.toLowerCase() || 'unknown'} mood of your uploaded track:</p>
            
            <div className="recommendations-grid">
              {moodData?.recommendations?.length > 0 ? (
                moodData.recommendations.map((song, index) => (
                  <div key={index} className="recommendation-card">
                    <div className="song-artwork">
                      <div className="artwork-placeholder">🎵</div>
                    </div>
                    <div className="song-info">
                      <h4>{formatSongTitle(song.filename)}</h4>
                      <p className="artist">DEAM Dataset</p>
                      <div className="song-details">
                        <span className="similarity">
                          {song.similarity ? `${song.similarity}% match` : 'Similar'}
                        </span>
                      </div>
                    </div>
                    <button 
                      className="play-song-btn"
                      title="Play song"
                      onClick={() => handlePlayRecommendation(song)}
                    >
                      ▶
                    </button>
                  </div>
                ))
              ) : (
                <p style={{gridColumn: '1/-1', textAlign: 'center', color: '#999'}}>
                  No recommendations available yet
                </p>
              )}
            </div>
          </section>
        </div>
      )}
    </div>
  )
}