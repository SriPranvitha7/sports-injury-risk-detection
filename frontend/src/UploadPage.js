import React, { useState } from 'react';
import axios from 'axios';

function UploadPage({ onResultsReady }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [activityType, setActivityType] = useState('');
  const [sportType, setSportType] = useState('');
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleUploadAndAnalyze = async () => {
    // Validation
    if (!selectedFile) {
      setError('Please select a video file first.');
      return;
    }
    if (!activityType) {
      setError('Please select an activity type.');
      return;
    }
    if (!sportType) {
      setError('Please select a sport type.');
      return;
    }

    try {
      // Step 1 — Upload video
      setUploading(true);
      setMessage('Uploading video...');

      const formData = new FormData();
      formData.append('file', selectedFile);

      const uploadResponse = await axios.post(
        'http://127.0.0.1:8000/video/upload',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      const videoId = uploadResponse.data.video_id;
      setUploading(false);
      setMessage('Video uploaded successfully. Starting analysis...');

      // Step 2 — Analyze video
      setAnalyzing(true);
      const analyzeResponse = await axios.post(
        `http://127.0.0.1:8000/video/analyze/${videoId}`
      );

      setAnalyzing(false);
      setMessage('Analysis complete! Loading results...');

      // Step 3 — Get full results
      const resultsResponse = await axios.get(
        `http://127.0.0.1:8000/video/results/${videoId}`
      );

      // Pass results to parent component
      onResultsReady(resultsResponse.data);

    } catch (err) {
      setUploading(false);
      setAnalyzing(false);
      setError('Something went wrong. Please make sure backend is running and try again.');
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Upload Sports Video</h2>
      <p style={styles.subtext}>
        Upload a sports video to analyze injury risk from movement patterns
      </p>

      {/* File Upload Box */}
      <div style={styles.uploadBox}>
        <div style={styles.uploadIcon}>📹</div>
        <p style={styles.uploadText}>Select your sports video</p>
        <p style={styles.uploadSub}>Supported formats: MP4, MOV, AVI</p>
        <input
          type="file"
          accept="video/mp4,video/quicktime,video/x-msvideo"
          onChange={handleFileChange}
          style={styles.fileInput}
        />
        {selectedFile && (
          <p style={styles.fileName}>
            Selected: {selectedFile.name}
          </p>
        )}
      </div>

      {/* Activity Type Dropdown */}
      <div style={styles.fieldGroup}>
        <label style={styles.label}>Activity Type</label>
        <select
          value={activityType}
          onChange={(e) => setActivityType(e.target.value)}
          style={styles.select}
        >
          <option value="">Select activity</option>
          <option value="running">Running</option>
          <option value="sprinting">Sprinting</option>
          <option value="jumping">Jumping</option>
          <option value="squatting">Squatting</option>
          <option value="landing">Landing</option>
          <option value="throwing">Throwing</option>
          <option value="cutting">Cutting Movements</option>
        </select>
      </div>

      {/* Sport Type Dropdown */}
      <div style={styles.fieldGroup}>
        <label style={styles.label}>Sport Type</label>
        <select
          value={sportType}
          onChange={(e) => setSportType(e.target.value)}
          style={styles.select}
        >
          <option value="">Select sport</option>
          <option value="football">Football</option>
          <option value="basketball">Basketball</option>
          <option value="cricket">Cricket</option>
          <option value="athletics">Athletics</option>
          <option value="swimming">Swimming</option>
          <option value="tennis">Tennis</option>
          <option value="volleyball">Volleyball</option>
          <option value="gym">Gym / Weightlifting</option>
        </select>
      </div>

      {/* Messages */}
      {error && <p style={styles.error}>{error}</p>}
      {message && <p style={styles.success}>{message}</p>}

      {/* Analyze Button */}
      <button
        onClick={handleUploadAndAnalyze}
        disabled={uploading || analyzing}
        style={uploading || analyzing ? styles.buttonDisabled : styles.button}
      >
        {uploading ? 'Uploading...' : analyzing ? 'Analyzing...' : 'Upload and Analyze Video'}
      </button>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px'
  },
  heading: {
    fontSize: '22px',
    fontWeight: 'bold',
    color: '#1e429f',
    marginBottom: '8px'
  },
  subtext: {
    color: '#6b7280',
    fontSize: '14px',
    marginBottom: '20px'
  },
  uploadBox: {
    border: '2px dashed #9ca3af',
    borderRadius: '12px',
    padding: '30px',
    textAlign: 'center',
    marginBottom: '20px',
    backgroundColor: '#f9fafb'
  },
  uploadIcon: {
    fontSize: '40px',
    marginBottom: '10px'
  },
  uploadText: {
    fontSize: '16px',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '4px'
  },
  uploadSub: {
    fontSize: '12px',
    color: '#9ca3af',
    marginBottom: '12px'
  },
  fileInput: {
    display: 'block',
    margin: '0 auto'
  },
  fileName: {
    marginTop: '10px',
    fontSize: '13px',
    color: '#1e429f',
    fontWeight: '500'
  },
  fieldGroup: {
    marginBottom: '16px'
  },
  label: {
    display: 'block',
    fontSize: '13px',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '6px'
  },
  select: {
    width: '100%',
    padding: '10px',
    borderRadius: '8px',
    border: '1px solid #d1d5db',
    fontSize: '14px',
    color: '#374151'
  },
  button: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#1e429f',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '500',
    cursor: 'pointer',
    marginTop: '8px'
  },
  buttonDisabled: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#9ca3af',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    cursor: 'not-allowed',
    marginTop: '8px'
  },
  error: {
    color: '#dc2626',
    fontSize: '13px',
    marginBottom: '10px'
  },
  success: {
    color: '#16a34a',
    fontSize: '13px',
    marginBottom: '10px'
  }
};

export default UploadPage;