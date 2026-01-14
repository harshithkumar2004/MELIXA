import './About.css'

export function About() {
  return (
    <div className="about">
      <div className="about-container">
        <h1>About Smart Playlist Matcher</h1>
        
        <section className="about-section">
          <h2>Our Mission</h2>
          <p>
            Smart Playlist Matcher uses advanced AI technology to analyze your music and create 
            perfectly curated playlists based on your mood. Whether you're looking for energy, 
            relaxation, or inspiration, we've got the perfect soundtrack for every moment.
          </p>
        </section>
        
        <section className="about-section">
          <h2>How It Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎵</div>
              <h3>Upload Your Music</h3>
              <p>Simply upload any audio file to get started</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🧠</div>
              <h3>AI Analysis</h3>
              <p>Our AI analyzes tempo, key, and mood indicators</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Perfect Match</h3>
              <p>Get personalized playlists that match your vibe</p>
            </div>
          </div>
        </section>
        
        <section className="about-section">
          <h2>Why Choose Us?</h2>
          <ul className="benefits-list">
            <li>Lightning-fast mood detection</li>
            <li>Support for multiple audio formats</li>
            <li>Personalized recommendations</li>
            <li>Beautiful, intuitive interface</li>
          </ul>
        </section>
      </div>
    </div>
  )
}
