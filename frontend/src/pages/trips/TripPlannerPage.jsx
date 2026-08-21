import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { createTrip, generateItinerary } from '../../services/tripService';
import { getDestinations } from '../../services/destinationService';
import { SparklesIcon } from '../../components/Icons';
import './TripPlannerPage.css';

const TripPlannerPage = () => {
  const [destinations, setDestinations] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    destination: '',
    start_date: '',
    end_date: '',
    budget: '',
    number_of_travelers: 1,
    travel_style: 'Relaxation'
  });
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    getDestinations().then(data => {
      const dests = data.results || data;
      setDestinations(dests);
      
      const destinationId = searchParams.get('destination');
      if (destinationId && dests.some(d => d.id === parseInt(destinationId))) {
        setFormData(prev => ({ ...prev, destination: destinationId }));
      }
    });
  }, [searchParams]);

  const handleSubmit = async (useAI = false) => {
    // Client-side validation
    if (!formData.title || !formData.destination || !formData.start_date || !formData.end_date || !formData.budget) {
        alert("Please fill in all required fields, including budget.");
        return;
    }
    
    if (parseFloat(formData.budget) <= 0) {
        alert("Budget must be greater than 0.");
        return;
    }

    setLoading(true);
    setLoadingMessage("Creating your personalized journey...");
    try {
      // Prepare payload
      const payload = {
        title: formData.title,
        destination: parseInt(formData.destination),
        start_date: formData.start_date,
        end_date: formData.end_date,
        budget: parseFloat(formData.budget),
        number_of_travelers: parseInt(formData.number_of_travelers),
        currency: 'INR'
      };

      const trip = await createTrip(payload);
      
      if (useAI) {
        setLoadingMessage("Building your day-by-day itinerary...");
        await generateItinerary(trip.id, { style: formData.travel_style });
      }
      navigate(`/trips/${trip.id}`);
    } catch (error) {
      console.error('Submission error:', error);
      let errorMessage = 'Failed to create trip.';
      if (error.response && error.response.data) {
        const data = error.response.data;
        if (typeof data === 'object') {
          errorMessage = Object.entries(data)
            .map(([field, msg]) => `${field}: ${msg}`)
            .join(' ');
        } else {
          errorMessage = String(data);
        }
      }
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const styles = ['Relaxation', 'Culture', 'Food', 'Adventure', 'Nature', 'Shopping'];

  return (
    <div className="planner-page container">
      <div className="planner-header">
        <h2 className="planner-title">Plan a New Trip</h2>
        <p className="planner-subtitle">Fill in the details below to start your personalized journey.</p>
      </div>
      
      <div className="planner-card">
        <section className="form-section">
          <label className="form-label">Trip Title <span className="required-star">*</span></label>
          <input 
            className="planner-input" 
            type="text" 
            placeholder="e.g., Summer in Goa" 
            value={formData.title}
            onChange={e => setFormData({...formData, title: e.target.value})} 
          />
        </section>

        <section className="form-section">
          <label className="form-label">Where are you going? <span className="required-star">*</span></label>
          <select 
            className="planner-input" 
            value={formData.destination}
            onChange={e => setFormData({...formData, destination: e.target.value})}
          >
            <option value="">Select Destination</option>
            {destinations.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
          </select>
        </section>

        <section className="form-section">
          <label className="form-label">Budget (INR) <span className="required-star">*</span></label>
          <input 
            className="planner-input" 
            type="number" 
            placeholder="e.g., 30000" 
            value={formData.budget}
            onChange={e => setFormData({...formData, budget: e.target.value})} 
          />
        </section>

        <section className="form-section">
          <div className="dates-grid">
            <div>
              <label className="form-label">Start Date <span className="required-star">*</span></label>
              <input 
                className="planner-input" 
                type="date" 
                value={formData.start_date}
                onChange={e => setFormData({...formData, start_date: e.target.value})} 
              />
            </div>
            <div>
              <label className="form-label">End Date <span className="required-star">*</span></label>
              <input 
                className="planner-input" 
                type="date" 
                value={formData.end_date}
                onChange={e => setFormData({...formData, end_date: e.target.value})} 
              />
            </div>
          </div>
        </section>

        <section className="form-section">
          <label className="form-label">Travel Style</label>
          <div className="style-chips">
            {styles.map(s => (
              <button 
                key={s} 
                type="button"
                className={`style-chip ${formData.travel_style === s ? 'active' : ''}`}
                onClick={() => setFormData({...formData, travel_style: s})}
              >
                {s}
              </button>
            ))}
          </div>
        </section>

        <div className="planner-actions">
          <button 
            type="button"
            className="btn btn-secondary planner-btn-secondary" 
            onClick={() => handleSubmit(false)}
          >
            Create Manually
          </button>
          <button 
            type="button"
            className="btn btn-primary planner-btn-primary" 
            onClick={() => handleSubmit(true)}
          >
            <SparklesIcon style={{ width: '18px', height: '18px' }} />
            Generate My AI Itinerary
          </button>
        </div>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>{loadingMessage}</p>
        </div>
      )}
    </div>
  );
};

export default TripPlannerPage;
