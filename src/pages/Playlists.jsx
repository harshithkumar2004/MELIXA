import { Plus, Play, MoreHorizontal } from 'lucide-react'
import './Playlists.css'

export function Playlists() {
  const playlists = [
    {
      id: 1,
      name: 'Sad',
      emoji: '😢',
      songCount: 24,
      duration: '1h 32m',
      color: 'linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%)'
    },
    {
      id: 2,
      name: 'Happy',
      emoji: '😊',
      songCount: 18,
      duration: '1h 5m',
      color: 'linear-gradient(135deg, #FFE66D 0%, #FF6B6B 100%)'
    },
    {
      id: 3,
      name: 'Energetic',
      emoji: '⚡',
      songCount: 32,
      duration: '2h 15m',
      color: 'linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%)'
    },
    {
      id: 4,
      name: 'Calm',
      emoji: '😌',
      songCount: 15,
      duration: '58m',
      color: 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)'
    }
  ]

  return (
    <div className="playlists">
      <div className="playlists-header">
        <h1>Mood-Based Playlists</h1>
        <button className="create-btn">
          <Plus size={20} />
          Create Playlist
        </button>
      </div>
      
      <div className="playlists-grid">
        {playlists.map(playlist => (
          <div key={playlist.id} className="playlist-card">
            <div 
              className="playlist-cover"
              style={{ background: playlist.color }}
            >
              <div className="playlist-emoji">{playlist.emoji}</div>
              <button className="play-overlay">
                <Play size={24} fill="white" />
              </button>
            </div>
            <div className="playlist-info">
              <h3>{playlist.name}</h3>
              <p>{playlist.songCount} songs • {playlist.duration}</p>
            </div>
            <button className="playlist-menu">
              <MoreHorizontal size={20} />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
