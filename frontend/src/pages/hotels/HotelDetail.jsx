import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getHotelDetail } from '../../services/hotelService';
import WishlistButton from '../../components/WishlistButton';
import ReviewList from '../../components/ReviewList';
import ReviewForm from '../../components/ReviewForm';

const HotelDetail = () => {
  const { slug } = useParams();
  const [hotel, setHotel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    getHotelDetail(slug).then(data => {
        setHotel(data);
        setLoading(false);
    });
  }, [slug]);

  if (loading) return <div className="page-container">Loading...</div>;
  if (!hotel) return <div className="page-container">Hotel not found</div>;

  return (
    <div className="destination-detail-page">
      <div className="page-container">
        <nav style={{ padding: 'var(--spacing-md) 0' }}>
          <Link to="/" className="navbar-link">Home</Link> / <Link to="/destinations" className="navbar-link">Destinations</Link> / <span>{hotel.name}</span>
        </nav>

        <div className="destination-hero" style={{ height: '400px', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
            <img src={hotel.image_url} alt={hotel.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>

        <main style={{ padding: 'var(--spacing-xl) 0' }}>
            <h1>{hotel.name}</h1>
            <p>★ {hotel.star_rating} • {hotel.city}, {hotel.country}</p>
            <p>{hotel.description}</p>
            <p style={{ fontWeight: 'bold', color: 'var(--accent)' }}>{hotel.price_per_night} {hotel.currency} / night</p>
            
            <WishlistButton entityType="hotel" entityId={hotel.id} />

            <section style={{ marginTop: 'var(--spacing-xl)' }}>
              <h2>Traveler Reviews</h2>
              <ReviewList entityType="hotel" slug={slug} key={refreshTrigger} />
              <ReviewForm entityType="hotel" entityId={hotel.id} onReviewCreated={() => setRefreshTrigger(prev => prev + 1)} />
            </section>
        </main>
      </div>
    </div>
  );
};

export default HotelDetail;
