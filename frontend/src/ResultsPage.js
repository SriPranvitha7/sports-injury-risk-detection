import React from 'react';

function ResultsPage({ results, onBack }) {

  if (!results) {
    return (
      <div style={styles.container}>
        <p>No results found. Please upload and analyze a video first.</p>
        <button onClick={onBack} style={styles.backButton}>Go Back</button>
      </div>
    );
  }

  const { summary, joint_details, recommendations } = results;

  const riskColor = {
    'Low Risk':      '#16a34a',
    'Moderate Risk': '#d97706',
    'High Risk':     '#dc2626',
    'Critical Risk': '#7f1d1d'
  };

  const riskBg = {
    'Low Risk':      '#f0fdf4',
    'Moderate Risk': '#fffbeb',
    'High Risk':     '#fef2f2',
    'Critical Risk': '#fef2f2'
  };

  const color = riskColor[summary.risk_category] || '#374151';
  const bg    = riskBg[summary.risk_category]    || '#f9fafb';

  return (
    <div style={styles.container}>
      <button onClick={onBack} style={styles.backButton}>← Back to Upload</button>

      <h2 style={styles.heading}>Risk Assessment Results</h2>

      {/* Overall Risk Score Card */}
      <div style={{ ...styles.scoreCard, backgroundColor: bg, borderColor: color }}>
        <p style={styles.scoreLabel}>Overall Risk Category</p>
        <p style={{ ...styles.scoreValue, color: color }}>
          {summary.risk_category}
        </p>
        <p style={styles.scoreNumber}>
          Risk Score: <strong>{summary.overall_risk_score} / 100</strong>
        </p>
        <p style={styles.scoreDetail}>
          Symmetry Score: {summary.symmetry_score}/100 &nbsp;|&nbsp;
          Detection Rate: {summary.detection_rate}% &nbsp;|&nbsp;
          Frames Analyzed: {summary.total_frames_analyzed}
        </p>
      </div>

      {/* Joint Risk Breakdown */}
      <h3 style={styles.sectionHeading}>Joint Risk Breakdown</h3>
      <div style={styles.jointsGrid}>
        {Object.entries(joint_details).map(([joint, data]) => {
          const jointColor = {
            low:      '#16a34a',
            moderate: '#d97706',
            high:     '#dc2626',
            critical: '#7f1d1d',
            unknown:  '#6b7280'
          }[data.risk_level] || '#374151';

          return (
            <div key={joint} style={styles.jointCard}>
              <p style={styles.jointName}>
                {joint.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </p>
              <p style={{ ...styles.jointRisk, color: jointColor }}>
                {data.risk_level.toUpperCase()}
              </p>
              <p style={styles.jointAngle}>Avg: {data.average_angle}°</p>
              <p style={styles.jointAngle}>Min: {data.minimum_angle}°</p>
              <p style={styles.jointAngle}>Max: {data.maximum_angle}°</p>
            </div>
          );
        })}
      </div>

      {/* Recommendations */}
      <h3 style={styles.sectionHeading}>Recommendations</h3>
      <div style={styles.recommendationsBox}>
        {recommendations.map((rec, index) => (
          <div key={index} style={styles.recommendationItem}>
            <span style={styles.recIcon}>💡</span>
            <p style={styles.recText}>{rec}</p>
          </div>
        ))}
      </div>

    </div>
  );
}

const styles = {
  container: {
    maxWidth: '700px',
    margin: '0 auto',
    padding: '20px'
  },
  heading: {
    fontSize: '22px',
    fontWeight: 'bold',
    color: '#1e429f',
    marginBottom: '16px'
  },
  backButton: {
    background: 'none',
    border: '1px solid #d1d5db',
    padding: '8px 14px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '13px',
    color: '#374151',
    marginBottom: '16px'
  },
  scoreCard: {
    border: '2px solid',
    borderRadius: '12px',
    padding: '20px',
    textAlign: 'center',
    marginBottom: '24px'
  },
  scoreLabel: {
    fontSize: '13px',
    color: '#6b7280',
    marginBottom: '4px'
  },
  scoreValue: {
    fontSize: '28px',
    fontWeight: 'bold',
    marginBottom: '4px'
  },
  scoreNumber: {
    fontSize: '16px',
    color: '#374151',
    marginBottom: '4px'
  },
  scoreDetail: {
    fontSize: '12px',
    color: '#6b7280'
  },
  sectionHeading: {
    fontSize: '17px',
    fontWeight: '600',
    color: '#1e429f',
    marginBottom: '12px'
  },
  jointsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '12px',
    marginBottom: '24px'
  },
  jointCard: {
    backgroundColor: '#f9fafb',
    border: '1px solid #e5e7eb',
    borderRadius: '10px',
    padding: '12px',
    textAlign: 'center'
  },
  jointName: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '4px'
  },
  jointRisk: {
    fontSize: '13px',
    fontWeight: 'bold',
    marginBottom: '6px'
  },
  jointAngle: {
    fontSize: '11px',
    color: '#6b7280',
    margin: '2px 0'
  },
  recommendationsBox: {
    backgroundColor: '#f0fdf4',
    border: '1px solid #bbf7d0',
    borderRadius: '10px',
    padding: '16px'
  },
  recommendationItem: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '10px',
    marginBottom: '10px'
  },
  recIcon: {
    fontSize: '16px',
    flexShrink: 0
  },
  recText: {
    fontSize: '13px',
    color: '#374151',
    margin: 0
  }
};

export default ResultsPage;