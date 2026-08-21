import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getTrips } from '../../services/tripService';
import './TripListPage.css';

const TripListPage = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const data = await getTrips();
        setTrips(data);
      } catch (error) {
        console.error('Error fetching trips:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchTrips();
  }, []);

  const upcoming = trips.filter(t => new Date(t.start_date) > new Date());
  const ongoing = trips.filter(t => new Date(t.start_date) <= new Date() && new Date(t.end_date) >= new Date());
  const past = trips.filter(t => new Date(t.end_date) < new Date());

  if (loading) return <div className="trips-loading">Loading your adventures...</div>;

  return (
    <div className="trips-dashboard">
      <header className="dashboard-hero">
        <div className="hero-content">
          <h1>WanderWorld Trips</h1>
          <p>Plan your journey. Organize every adventure in one place.</p>
          <div className="hero-actions">
            <Link to="/trips/new" className="btn-primary"><span>+</span> Plan a New Trip</Link>
          </div>
        </div>
      </header>

      {trips.length > 0 && (
        <section className="stats-row">
          <div className="stat-card"><h3>{trips.length}</h3><p>Trips Planned</p></div>
          <div className="stat-card"><h3>{upcoming.length}</h3><p>Upcoming</p></div>
          <div className="stat-card"><h3>{ongoing.length}</h3><p>Ongoing</p></div>
          <div className="stat-card"><h3>{past.length}</h3><p>Completed</p></div>
        </section>
      )}

      {trips.length === 0 ? (
        <div className="empty-state">
          <div className="illustration">✈️</div>
          <h2>Your next adventure starts here</h2>
          <p>You haven't planned a trip yet. Create your first personalized itinerary with WanderWorld.</p>
          <div className="actions">
            <Link to="/trips/new" className="btn-primary">✨ Plan with AI</Link>
            <Link to="/trips/new" className="btn-secondary">✦ Create Manually</Link>
          </div>
        </div>
      ) : (
        <div className="trips-list">
          <TripSection title="Ongoing Trips" trips={ongoing} />
          <TripSection title="Upcoming Trips" trips={upcoming} />
          <TripSection title="Past Trips" trips={past} />
        </div>
      )}
    </div>
  );
};

const TripSection = ({ title, trips }) => {
  if (trips.length === 0) return null;
  return (
    <section className="trip-category">
      <h2>{title}</h2>
      <div className="trip-grid">
        {trips.map(trip => (
          <div key={trip.id} className="trip-card">
            <div className="card-image" style={{ backgroundImage: `url(${trip.destination.cover_image_url})` }}></div>
            <div className="card-content">
              <h3>{trip.title}</h3>
              <p className="destination">{trip.destination.name}, {trip.destination.country}</p>
              <p className="dates">{trip.start_date} – {trip.end_date}</p>
              <div className="meta">
                <span>{trip.number_of_travelers} travelers</span>
                <span>{trip.budget} {trip.currency}</span>
              </div>
              <Link to={`/trips/${trip.id}`} className="btn-view">View Trip →</Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default TripListPage;
