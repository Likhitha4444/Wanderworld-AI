import { useState } from 'react';
import { generateItinerary } from '../services/tripService';

const GenerateItineraryButton = ({ tripId, onGenerated }) => {
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setGenerating(true);
    setError(null);
    try {
      await generateItinerary(tripId);
      onGenerated();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate itinerary.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div>
      <button onClick={handleGenerate} disabled={generating}>
        {generating ? 'Generating your itinerary...' : 'Generate AI Itinerary'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default GenerateItineraryButton;
