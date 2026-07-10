import React, { useState } from 'react';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div style={{ fontFamily: 'Arial', padding: '20px' }}>
      <h1>🏃 Sports Injury Risk Detection Platform</h1>
      <p>AI-powered platform for detecting sports injury risks from video analysis</p>
      
      <nav style={{ marginBottom: '20px' }}>
        <button onClick={() => setCurrentPage('home')} style={{ marginRight: '10px' }}>Home</button>
        <button onClick={() => setCurrentPage('login')} style={{ marginRight: '10px' }}>Login</button>
        <button onClick={() => setCurrentPage('register')}>Register</button>
      </nav>

      {currentPage === 'home' && (
        <div>
          <h2>Welcome</h2>
          <p>Upload a sports video to detect potential injury risks using AI.</p>
          <h3>Roles Available:</h3>
          <ul>
            <li>Athlete</li>
            <li>Coach</li>
            <li>Physiotherapist</li>
            <li>Sports Scientist</li>
            <li>Administrator</li>
          </ul>
        </div>
      )}

      {currentPage === 'login' && (
        <div>
          <h2>Login</h2>
          <input type="email" placeholder="Email" style={{ display: 'block', marginBottom: '10px', padding: '8px' }} />
          <input type="password" placeholder="Password" style={{ display: 'block', marginBottom: '10px', padding: '8px' }} />
          <button>Login</button>
        </div>
      )}

      {currentPage === 'register' && (
        <div>
          <h2>Register</h2>
          <input type="text" placeholder="Username" style={{ display: 'block', marginBottom: '10px', padding: '8px' }} />
          <input type="email" placeholder="Email" style={{ display: 'block', marginBottom: '10px', padding: '8px' }} />
          <input type="password" placeholder="Password" style={{ display: 'block', marginBottom: '10px', padding: '8px' }} />
          <select style={{ display: 'block', marginBottom: '10px', padding: '8px' }}>
            <option value="">Select Role</option>
            <option value="athlete">Athlete</option>
            <option value="coach">Coach</option>
            <option value="physiotherapist">Physiotherapist</option>
            <option value="sports_scientist">Sports Scientist</option>
            <option value="admin">Administrator</option>
          </select>
          <button>Register</button>
        </div>
      )}
    </div>
  );
}

export default App;