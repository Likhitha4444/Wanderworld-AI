import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getTripDetail } from '../../services/tripService';
import './TripDetailPage.css';

const TripDetailPage = () => {
  const { id } = useParams();
  const [trip, setTrip] = useState(null);
  const [activeTab, setActiveTab] = useState('itinerary');

  useEffect(() => {
    getTripDetail(id).then(setTrip);
  }, [id]);

  if (!trip) return <div>Loading...</div>;

  return (
    <div className="trip-detail-page">
      <div className="hero-section">
        <h1>{trip.title}</h1>
        <p>{trip.destination.name} • {trip.start_date} to {trip.end_date}</p>
      </div>

      <nav className="tab-bar">
        <button className={activeTab === 'overview' ? 'active' : ''} onClick={() => setActiveTab('overview')}>Overview</button>
        <button className={activeTab === 'itinerary' ? 'active' : ''} onClick={() => setActiveTab('itinerary')}>Itinerary</button>
      </nav>

      <div className="content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="overview-header">
              <h3>Trip Overview</h3>
              <p>Everything you need to know about your trip at a glance.</p>
            </div>
            <div className="overview-grid">
              <div className="overview-card">
                <span>📍</span>
                <h4>Destination</h4>
                <p>{trip.destination.name}</p>
                <small>{trip.destination.country}</small>
              </div>
              <div className="overview-card">
                <span>📅</span>
                <h4>Travel Dates</h4>
                <p>{new Date(trip.start_date).toLocaleDateString('en-US', {month: 'short', day: 'numeric'})} – {new Date(trip.end_date).toLocaleDateString('en-US', {month: 'short', day: 'numeric'})}</p>
              </div>
              <div className="overview-card">
                <span>💰</span>
                <h4>Budget</h4>
                <p>{trip.budget} {trip.currency}</p>
              </div>
              <div className="overview-card">
                <span>👥</span>
                <h4>Travelers</h4>
                <p>{trip.number_of_travelers} Traveler{trip.number_of_travelers > 1 ? 's' : ''}</p>
              </div>
              <div className="overview-card">
                <span>✈️</span>
                <h4>Travel Style</h4>
                <p>{trip.planning_source}</p>
              </div>
            </div>
          </div>
        )}
        {activeTab === 'itinerary' && (
          <div className="timeline">
            {trip.days.map(day => (
              <div key={day.id} className="day-group">
                <h3>Day {day.day_number}: {day.title}</h3>
                <p>{day.summary}</p>
                {day.activities.map(act => (
                  <div key={act.id} className="timeline-item">
                    <span className="time">{act.start_time.substring(0, 5)}</span>
                    <div className="card">
                      <h4>{act.title}</h4>
                      <p>{act.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TripDetailPage;
