import { useState, useEffect } from 'react';
import { getTravelDNA, recalculateTravelDNA } from '../../services/travelDnaService';
import './TravelDnaPage.css';

const TravelDnaPage = () => {
  const [dna, setDna] = useState([]);
  const [loading, setLoading] = useState(true);
  const [recalculating, setRecalculating] = useState(false);

  useEffect(() => {
    fetchDNA();
  }, []);

  const fetchDNA = async () => {
    setLoading(true);
    try {
      const data = await getTravelDNA();
      setDna(data);
    } catch (error) {
      console.error('Error fetching Travel DNA:', error);
    } finally {
      setLoading(false);
    }
  };
const handleRecalculate = async () => {
  setRecalculating(true);
  try {
    await recalculateTravelDNA();
    const freshDNA = await getTravelDNA();
    if (freshDNA.length === 0) {
      alert("Travel DNA could not be calculated. Please explore more destinations or leave reviews to build your profile.");
    }
    setDna(freshDNA);
  } catch (error) {
    console.error('Error recalculating DNA:', error);
    alert("Failed to recalculate Travel DNA. Please try again later.");
  } finally {
    setRecalculating(false);
  }
};


  if (loading) return <div className="travel-dna-page">Loading your profile...</div>;

  return (
    <div className="travel-dna-page">
      <header className="hero-section">
        <h1>Your Travel DNA</h1>
        <p>This profile reflects your unique travel preferences based on your past journeys and interests.</p>
        <button className="btn-primary" onClick={handleRecalculate} disabled={recalculating}>
          {recalculating ? 'Recalculating...' : 'Recalculate Travel DNA'}
        </button>
      </header>

      {dna.length === 0 ? (
        <div className="empty-state">
          <div className="illustration" style={{fontSize: '3rem', marginBottom: '1rem'}}>🧬</div>
          <h2>Your Travel DNA isn't ready yet</h2>
          <p>Explore more destinations and build your travel profile to generate your unique Travel DNA.</p>
        </div>
      ) : (
        <div className="dna-grid">
          {dna.map((item, index) => (
            <div key={index} className="dna-card">
              <h3>{item.category}</h3>
              <p><strong>Score:</strong> {item.score}</p>
              <p><strong>Confidence:</strong> {(item.confidence * 100).toFixed(0)}%</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TravelDnaPage;
