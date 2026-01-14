import { NavLink } from 'react-router-dom'
import { Home, Upload, ListMusic, Info } from 'lucide-react'
import './Sidebar.css'

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Smart Playlist</h2>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/" className="nav-item">
          <Home size={20} />
          <span>Home</span>
        </NavLink>
        <NavLink to="/upload" className="nav-item">
          <Upload size={20} />
          <span>Upload</span>
        </NavLink>
        <NavLink to="/playlists" className="nav-item">
          <ListMusic size={20} />
          <span>Playlists</span>
        </NavLink>
        <NavLink to="/about" className="nav-item">
          <Info size={20} />
          <span>About</span>
        </NavLink>
      </nav>
      <div className="sidebar-footer">
        <p>© 2026 Smart Playlist Matcher</p>
      </div>
    </aside>
  )
}
