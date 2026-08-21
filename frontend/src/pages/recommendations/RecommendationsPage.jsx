import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getRecommendations } from '../../services/recommendationService';
import './RecommendationsPage.css';

const RecommendationsPage = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [type, setType] = useState('attraction');
  const navigate = useNavigate();

  useEffect(() => {
    fetchRecommendations();
  }, [type]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const data = await getRecommendations(type);
      
      // Deduplicate recommendations: keep the highest score for the same ID
      const uniqueRecsMap = new Map();
      
      data.forEach(rec => {
        const item = rec.destination || rec.hotel || rec.attraction;
        if (!item || !item.id) return;
        
        const id = item.id;
        
        if (!uniqueRecsMap.has(id) || uniqueRecsMap.get(id).score < rec.score) {
          uniqueRecsMap.set(id, rec);
        }
      });
      
      const uniqueRecs = Array.from(uniqueRecsMap.values())
        .sort((a, b) => b.score - a.score)
        .slice(0, 6); // Limit to top 6
        
      setRecommendations(uniqueRecs);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'attraction', label: 'Attractions' },
    { id: 'destination', label: 'Destinations' },
    { id: 'hotel', label: 'Hotels' },
  ];

  if (loading) return <div className="loading">Loading recommendations...</div>;

  return (
    <div className="recommendations-page container" style={{ padding: 'var(--spacing-xl) 0' }}>
      <div className="recommendations-header" style={{ textAlign: 'center', marginBottom: 'var(--spacing-xl)' }}>
        <h2 style={{ fontSize: 'var(--font-size-h2)', marginBottom: 'var(--spacing-sm)' }}>Personalized Recommendations</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Discover places and stays selected based on your Travel DNA.</p>
      </div>
      
      <div className="tabs-container" style={{ display: 'flex', justifyContent: 'center', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-xl)' }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-button ${type === tab.id ? 'active' : ''}`}
            onClick={() => setType(tab.id)}
            style={{ padding: 'var(--spacing-sm) var(--spacing-md)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)', background: type === tab.id ? 'var(--accent)' : 'var(--bg-card)', color: type === tab.id ? 'var(--bg-primary)' : 'var(--text-primary)', cursor: 'pointer', fontWeight: 500 }}
          >
            {tab.label}
          </button>
        ))}
      </div>
      
      {recommendations.length === 0 && <p className="empty-state" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No recommendations available yet.</p>}
      
      <div className="grid-container">
        {recommendations.map((rec, index) => {
          const item = rec.destination || rec.hotel || rec.attraction;
          // Use cover_image_url for destinations, fallback for others
          const imageUrl = item.cover_image_url || item.image_url || '/placeholder.jpg';
          
          return (
            <div key={item.id || index} className="card" style={{ display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
              <img 
                src={imageUrl}
                alt={item.name} 
                style={{ width: '100%', height: '200px', objectFit: 'cover' }}
                onError={(e) => { 
                  if (e.target.src !== window.location.origin + '/placeholder.jpg') {
                    e.target.src = '/placeholder.jpg'; 
                  }
                }}
              />
              <div style={{ padding: 'var(--spacing-md)' }}>
                <div style={{ color: 'var(--accent)', fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--spacing-xs)' }}>{(rec.score * 100).toFixed(0)}% Match</div>
                <h4 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--spacing-xs)' }}>{item.name}</h4>
                <p style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)', marginBottom: 'var(--spacing-sm)' }}>📍 {item.city}, {item.country}</p>
                <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-muted)', marginBottom: 'var(--spacing-md)', height: '40px', overflow: 'hidden' }}>{item.short_description || item.description}</p>
                
                {rec.reasons && rec.reasons.length > 0 && (
                  <div style={{ backgroundColor: 'var(--bg-secondary)', padding: 'var(--spacing-sm)', borderRadius: 'var(--radius-sm)', fontSize: 'var(--font-size-sm)', marginBottom: 'var(--spacing-md)' }}>
                    <p style={{ color: 'var(--text-secondary)' }}>✨ {rec.reasons[0]}</p>
                  </div>
                )}
                
                <button 
                  className="btn btn-primary" 
                  style={{width: '100%'}}
                  onClick={() => navigate(
                    type === 'destination' ? `/destinations/${item.slug}` : 
                    type === 'hotel' ? `/hotels/${item.slug}` : 
                    `/attractions/${item.slug}`
                  )}
                >
                  View Details →
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RecommendationsPage;
