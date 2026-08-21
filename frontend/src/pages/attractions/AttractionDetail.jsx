import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getAttractionDetail } from '../../services/attractionService';
import WishlistButton from '../../components/WishlistButton';
import ReviewList from '../../components/ReviewList';
import ReviewForm from '../../components/ReviewForm';

const AttractionDetail = () => {
  const { slug } = useParams();
  const [attraction, setAttraction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    getAttractionDetail(slug).then(data => {
        setAttraction(data);
        setLoading(false);
    });
  }, [slug]);

  if (loading) return <div className="page-container">Loading...</div>;
  if (!attraction) return <div className="page-container">Attraction not found</div>;

  return (
    <div className="destination-detail-page">
      <div className="page-container">
        <nav style={{ padding: 'var(--spacing-md) 0' }}>
          <Link to="/" className="navbar-link">Home</Link> / <Link to="/destinations" className="navbar-link">Destinations</Link> / <span>{attraction.name}</span>
        </nav>

        <div className="destination-hero" style={{ height: '400px', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
            <img src={attraction.image_url} alt={attraction.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>

        <main style={{ padding: 'var(--spacing-xl) 0' }}>
            <h1>{attraction.name}</h1>
            <p style={{ color: 'var(--accent)' }}>{attraction.category}</p>
            <p>{attraction.description}</p>
            <p>Entry Fee: {attraction.entry_fee} {attraction.currency}</p>
            
            <WishlistButton entityType="attraction" entityId={attraction.id} />

            <section style={{ marginTop: 'var(--spacing-xl)' }}>
              <h2>Traveler Reviews</h2>
              <ReviewList entityType="attraction" slug={slug} key={refreshTrigger} />
              <ReviewForm entityType="attraction" entityId={attraction.id} onReviewCreated={() => setRefreshTrigger(prev => prev + 1)} />
            </section>
        </main>
      </div>
    </div>
  );
};

export default AttractionDetail;
