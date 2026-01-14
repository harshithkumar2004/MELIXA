import { Play, Pause, SkipBack, SkipForward, Volume2 } from 'lucide-react'
import { useState } from 'react'
import './AudioPlayer.css'

export function AudioPlayer() {
  const [isPlaying, setIsPlaying] = useState(false)

  // Generate waveform data (mock data for visualization)
  const generateWaveformData = () => {
    const bars = 60
    const data = []
    for (let i = 0; i < bars; i++) {
      data.push(Math.random() * 0.8 + 0.2) // Random height between 0.2 and 1
    }
    return data
  }

  const waveform = generateWaveformData()

  return (
    <div className="audio-player">
      <div className="track-info">
        <div className="track-artwork">
          <div className="artwork-placeholder">🎵</div>
        </div>
        <div className="track-details">
          <div className="track-title">Summer Vibes</div>
          <div className="track-artist">Chill Beats Collection</div>
        </div>
      </div>
      
      <div className="player-controls">
        <button className="control-btn">
          <SkipBack size={20} />
        </button>
        <button className="control-btn play-btn" onClick={() => setIsPlaying(!isPlaying)}>
          {isPlaying ? <Pause size={24} /> : <Play size={24} />}
        </button>
        <button className="control-btn">
          <SkipForward size={20} />
        </button>
      </div>
      
      <div className="player-extras">
        <div className="progress-container">
          <div className="waveform-container">
            <div className="waveform">
              {waveform.map((height, index) => (
                <div 
                  key={index}
                  className={`waveform-bar ${index < 36 ? 'played' : ''}`}
                  style={{ height: `${height * 100}%` }}
                ></div>
              ))}
            </div>
            <div className="progress-handle" style={{ left: '60%' }}></div>
          </div>
          <div className="time-display">2:45 / 4:32</div>
        </div>
        <button className="control-btn volume-btn">
          <Volume2 size={20} />
        </button>
      </div>
    </div>
  )
}
