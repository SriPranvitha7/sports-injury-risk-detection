import React, { useState } from 'react';
import UploadPage from './UploadPage';
import ResultsPage from './ResultsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [results, setResults] = useState(null);

  const handleResultsReady = (data) => {
    setResults(data);
    setCurrentPage('results');
  };

  const handleBackToUpload = () => {
    setCurrentPage('upload');
    setResults(null);
  };

  return (
    <div style={{ fontFamily: 'Arial', padding: '20px', maxWidth: '800px', margin: '0 auto' }}>

      {/* Header */}
      <div style={{ borderBottom: '2px solid #1e429f', paddingBottom: '12px', marginBottom: '20px' }}>
        <h1 style={{ color: '#1e429f', margin: 0, fontSize: '22px' }}>
          🏃 Sports Injury Risk Detection Platform
        </h1>
        <p style={{ color: '#6b7280', margin: '4px 0 0', fontSize: '13px' }}>
          AI-powered sports injury risk analysis using MediaPipe Pose and biomechanical analysis
        </p>
      </div>

      {/* Navigation */}
      <nav style={{ marginBottom: '24px', display: 'flex', gap: '10px' }}>
        {['home', 'upload', 'login', 'register'].map((page) => (
          <button
            key={page}
            onClick={() => setCurrentPage(page)}
            style={{
              padding: '8px 16px',
              backgroundColor: currentPage === page ? '#1e429f' : 'white',
              color: currentPage === page ? 'white' : '#374151',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: currentPage === page ? '600' : 'normal'
            }}
          >
            {page.charAt(0).toUpperCase() + page.slice(1)}
          </button>
        ))}
      </nav>

      {/* Pages */}
      {currentPage === 'home' && (
        <div>
          <h2 style={{ color: '#1e429f' }}>Welcome</h2>
          <p style={{ color: '#374151', lineHeight: '1.6' }}>
            Upload a sports video to detect potential injury risks using AI.
            Our platform analyzes joint movements, calculates biomechanical angles,
            and provides personalized risk assessment and recommendations.
          </p>
          <h3 style={{ color: '#374151', marginTop: '20px' }}>How it works:</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[
              '1. Upload your sports video (MP4, MOV, AVI)',
              '2. AI detects 33 body joint positions using MediaPipe Pose',
              '3. Joint angles are calculated using biomechanical analysis',
              '4. Risk score is generated based on movement patterns',
              '5. Personalized recommendations are provided'
            ].map((step, i) => (
              <div key={i} style={{
                backgroundColor: '#f0f9ff',
                border: '1px solid #bae6fd',
                borderRadius: '8px',
                padding: '10px 14px',
                fontSize: '14px',
                color: '#374151'
              }}>
                {step}
              </div>
            ))}
          </div>
          <h3 style={{ color: '#374151', marginTop: '20px' }}>Roles Available:</h3>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {['Athlete', 'Coach', 'Physiotherapist', 'Sports Scientist', 'Administrator'].map((role) => (
              <span key={role} style={{
                backgroundColor: '#e0e7ff',
                color: '#1e429f',
                padding: '4px 12px',
                borderRadius: '99px',
                fontSize: '13px',
                fontWeight: '500'
              }}>
                {role}
              </span>
            ))}
          </div>
          <button
            onClick={() => setCurrentPage('upload')}
            style={{
              marginTop: '24px',
              padding: '12px 24px',
              backgroundColor: '#1e429f',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '15px',
              cursor: 'pointer',
              fontWeight: '500'
            }}
          >
            Start Analysis →
          </button>
        </div>
      )}

      {currentPage === 'upload' && (
        <UploadPage onResultsReady={handleResultsReady} />
      )}

      {currentPage === 'results' && (
        <ResultsPage results={results} onBack={handleBackToUpload} />
      )}

      {currentPage === 'login' && (
        <div style={{ maxWidth: '360px' }}>
          <h2 style={{ color: '#1e429f' }}>Login</h2>
          <label style={{ fontSize: '13px', color: '#374151' }}>Email</label>
          <input
            type="email"
            placeholder="Enter email"
            style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '12px', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
          />
          <label style={{ fontSize: '13px', color: '#374151' }}>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
          />
          <button style={{ width: '100%', padding: '10px', backgroundColor: '#1e429f', color: 'white', border: 'none', borderRadius: '8px', fontSize: '14px', cursor: 'pointer' }}>
            Login
          </button>
        </div>
      )}

      {currentPage === 'register' && (
        <div style={{ maxWidth: '360px' }}>
          <h2 style={{ color: '#1e429f' }}>Register</h2>
          <label style={{ fontSize: '13px', color: '#374151' }}>Username</label>
          <input
            type="text"
            placeholder="Enter username"
            style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '12px', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
          />
          <label style={{ fontSize: '13px', color: '#374151' }}>Email</label>
          <input
            type="email"
            placeholder="Enter email"
            style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '12px', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
          />
          <label style={{ fontSize: '13px', color: '#374151' }}>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '12px', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}
          />
          <label style={{ fontSize: '13px', color: '#374151' }}>Role</label>
          <select style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '8px', border: '1px solid #d1d5db', boxSizing: 'border-box' }}>
            <option value="">Select Role</option>
            <option value="athlete">Athlete</option>
            <option value="coach">Coach</option>
            <option value="physiotherapist">Physiotherapist</option>
            <option value="sports_scientist">Sports Scientist</option>
            <option value="admin">Administrator</option>
          </select>
          <button style={{ width: '100%', padding: '10px', backgroundColor: '#1e429f', color: 'white', border: 'none', borderRadius: '8px', fontSize: '14px', cursor: 'pointer' }}>
            Register
          </button>
        </div>
      )}

    </div>
  );
}

export default App;