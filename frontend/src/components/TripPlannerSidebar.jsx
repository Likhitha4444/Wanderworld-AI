import React from 'react';
import { Link } from 'react-router-dom';

const TripPlannerSidebar = ({ destination }) => {
  return (
    <div className="card" style={{ 
      position: 'sticky', 
      top: 'calc(var(--spacing-xl) + 60px)' 
    }}>
      <h3 style={{ margin: '0 0 var(--spacing-sm)' }}>Plan your trip to {destination.name}</h3>
      <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--spacing-md)' }}>
        Build a personalized itinerary with WanderWorld AI.
      </p>
      <div style={{ marginBottom: 'var(--spacing-md)', color: 'var(--text-secondary)' }}>
        <p>✓ AI-powered itinerary</p>
        <p>✓ Personalized recommendations</p>
      </div>
      <Link to={`/trips/new?destination=${destination.id}`} className="btn btn-primary" style={{ width: '100%', display: 'inline-block', textAlign: 'center' }}>
        Plan My Trip
      </Link>
    </div>
  );
};

export default TripPlannerSidebar;
