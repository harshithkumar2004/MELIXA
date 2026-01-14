import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Home } from './pages/Home'
import { Upload } from './pages/Upload'
import { Playlists } from './pages/Playlists'
import { About } from './pages/About'
import { AudioPlayer } from './components/AudioPlayer'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/playlists" element={<Playlists />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <AudioPlayer />
      </div>
    </Router>
  )
}

export default App
