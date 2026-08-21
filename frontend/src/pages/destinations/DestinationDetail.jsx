import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDestinationDetail } from '../../services/destinationService';
import HotelCard from '../../components/HotelCard';
import AttractionCard from '../../components/AttractionCard';
import ReviewList from '../../components/ReviewList';
import ReviewForm from '../../components/ReviewForm';
import DestinationHero from '../../components/DestinationHero';
import TripPlannerSidebar from '../../components/TripPlannerSidebar';

const DestinationDetail = () => {
  const { slug } = useParams();
  const [destination, setDestination] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDestination = async () => {
      try {
        const response = await getDestinationDetail(slug);
        setDestination(response.data || response);
      } catch (error) {
        console.error('Error fetching destination detail:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDestination();
  }, [slug]);

  if (loading) return <div className="page-container">Loading...</div>;
  if (!destination) return <div className="page-container">Destination not found</div>;

  return (
    <div className="destination-detail-page">
      <div className="page-container">
        <nav style={{ padding: 'var(--spacing-md) 0' }}>
          <Link to="/" className="navbar-link">Home</Link> / <Link to="/destinations" className="navbar-link">Destinations</Link> / <span>{destination.name}</span>
        </nav>

        <DestinationHero destination={destination} />

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: 'var(--spacing-xl)', marginTop: 'var(--spacing-xl)' }}>
          <main>
            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h2>About {destination.name}</h2>
              <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', marginTop: 'var(--spacing-md)' }}>{destination.description}</p>
            </section>

            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h2>Places to stay in {destination.name}</h2>
              {destination.hotels && destination.hotels.length > 0 ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 'var(--spacing-md)', marginTop: 'var(--spacing-md)' }}>
                  {destination.hotels.map(h => <HotelCard key={h.id} hotel={h} />)}
                </div>
              ) : (
                <div className="card" style={{ textAlign: 'center', padding: 'var(--spacing-xl)' }}>No stays currently available.</div>
              )}
            </section>

            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h2>Top things to do in {destination.name}</h2>
              {destination.attractions && destination.attractions.length > 0 ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 'var(--spacing-md)', marginTop: 'var(--spacing-md)' }}>
                  {destination.attractions.map(a => <AttractionCard key={a.id} attraction={a} />)}
                </div>
              ) : (
                <div className="card" style={{ textAlign: 'center', padding: 'var(--spacing-xl)' }}>No attractions currently available.</div>
              )}
            </section>

            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h2>Traveler Reviews</h2>
              <div style={{ marginTop: 'var(--spacing-md)' }}>
                {/* Destination reviews are not supported by the backend */}
                <p style={{ color: 'var(--text-secondary)' }}>Reviews are only available for hotels and attractions.</p>
              </div>
            </section>
          </main>

          <aside>
            <TripPlannerSidebar destination={destination} />
          </aside>
        </div>
      </div>
    </div>
  );
};

export default DestinationDetail;
