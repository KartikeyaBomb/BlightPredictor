function Zip38127() {
  return (
    <div style={{ lineHeight: 1.6 }}>
      {/* Top Section: Title/Description Left, Graph Right */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 400px', 
        gap: '2rem', 
        marginBottom: '2rem',
        alignItems: 'start'
      }}>
        {/* Left: Title and Short Description */}
        <div>
          <h2 style={{ 
            marginTop: 0, 
            fontSize: '2rem',
            marginBottom: '1rem',
            color: '#ffffff'
          }}>
            ZIP 38127: Frayser
          </h2>
          <p style={{ 
            fontSize: '1.1rem', 
            color: '#a0a0b2',
            lineHeight: 1.7,
            marginBottom: '1.5rem'
          }}>
            Frayser demonstrates critical blight risk patterns with multi-factor indicators 
            showing strong predictive correlations. The neighborhood faces compounding challenges 
            requiring comprehensive intervention strategies and resource allocation.
          </p>
          <div style={{
            background: 'rgba(255, 255, 255, 0.08)',
            padding: '1rem',
            borderRadius: '8px',
            border: '1px solid rgba(255, 255, 255, 0.15)'
          }}>
            <h4 style={{ marginTop: 0, marginBottom: '0.75rem', color: '#ffffff' }}>Key Indicators</h4>
            <ul style={{ margin: 0, paddingLeft: '1.5rem', color: '#a0a0b2' }}>
              <li>Concentrated clusters of repeat code violations</li>
              <li>Rising vacancy rates linked to eviction patterns</li>
              <li>Correlation between crime hotspots and property decline</li>
              <li>Accelerating deterioration in targeted zones</li>
            </ul>
          </div>
        </div>

        {/* Right: Smaller Graph */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.08)',
          backdropFilter: 'blur(14px)',
          border: '1px solid rgba(255, 255, 255, 0.25)',
          borderRadius: '16px',
          padding: '1.5rem',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.45)'
        }}>
          <img 
            src="/images/plots/Frayser_predictors_vs_blight.png" 
            alt="Frayser Neighborhood Analysis" 
            style={{
              width: '100%',
              height: 'auto',
              borderRadius: '8px',
              marginBottom: '1rem'
            }}
          />
          <h3 style={{ 
            fontSize: '1.2rem', 
            marginBottom: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            color: '#ffffff'
          }}>
            Frayser
            <span style={{
              display: 'inline-block',
              padding: '0.25rem 0.75rem',
              background: '#ef4444',
              color: '#ffffff',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: 600,
              textTransform: 'uppercase'
            }}>High Risk</span>
          </h3>
          <p style={{ fontSize: '0.9rem', color: '#a0a0b2', margin: 0 }}>
            Multi-factor correlation analysis
          </p>
        </div>
      </div>

      {/* Bottom Section: Larger Text Box */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.06)',
        border: '1px solid rgba(255, 255, 255, 0.15)',
        borderRadius: '12px',
        padding: '2rem',
        marginTop: '2rem'
      }}>
        <h3 style={{ 
          marginTop: 0, 
          marginBottom: '1.5rem',
          fontSize: '1.5rem',
          color: '#ffffff'
        }}>
          Detailed Analysis & Recommendations
        </h3>
        
        <div style={{ fontSize: '1rem', color: '#d0d0e0', lineHeight: 1.8 }}>
          <h4 style={{ color: '#ffffff', marginTop: '0', marginBottom: '0.75rem' }}>
            Current Situation
          </h4>
          <p>
            The Frayser neighborhood faces complex, interconnected blight challenges. Analysis 
            reveals concentrated areas where property deterioration accelerates due to combinations 
            of evictions, crime, and code violations. Properties within identified clusters show 
            an 85% correlation between these factors and rapid decline.
          </p>

          <h4 style={{ color: '#ffffff', marginTop: '1.5rem', marginBottom: '0.75rem' }}>
            Predictive Insights
          </h4>
          <p>
            Our predictive model identifies properties at immediate risk by analyzing temporal 
            patterns across data sources. Areas showing increased police activity combined with 
            nearby evictions demonstrate a 3.1x higher probability of code violations within 
            6 months. Early detection enables proactive intervention before conditions worsen.
          </p>

          <h4 style={{ color: '#ffffff', marginTop: '1.5rem', marginBottom: '0.75rem' }}>
            Recommended Actions
          </h4>
          <ul style={{ paddingLeft: '1.5rem', marginTop: '0.5rem' }}>
            <li>Deploy concentrated enforcement resources to identified high-risk zones</li>
            <li>Establish rapid response protocols for properties entering decline phase</li>
            <li>Create targeted community revitalization programs in cluster areas</li>
            <li>Implement predictive inspection schedules based on risk scoring</li>
            <li>Coordinate with social services to address underlying housing instability</li>
            <li>Monitor and respond to emerging hotspots using real-time data</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Zip38127;