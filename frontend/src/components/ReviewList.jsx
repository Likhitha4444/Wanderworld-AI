import { useState, useEffect } from 'react';
import ReviewCard from './ReviewCard';
import { getEntityReviews } from '../services/reviewService';

const ReviewList = ({ entityType, slug }) => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getEntityReviews(entityType, slug)
      .then(data => {
        setReviews(data);
        setError(null);
      })
      .catch(err => {
        console.error('Failed to fetch reviews', err);
        setError('Failed to load reviews.');
        setReviews([]);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [entityType, slug]);

  if (loading) return <p>Loading reviews...</p>;
  if (error) return <p style={{ color: 'var(--danger)' }}>{error}</p>;
  if (!reviews || reviews.length === 0) return (
    <div className="glass-card" style={{ textAlign: 'center', padding: '2rem' }}>
        <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>♡</div>
        <h3>No reviews yet</h3>
        <p style={{ color: 'var(--text-secondary)' }}>Be the first traveler to share your experience.</p>
    </div>
  );

  return (
    <div style={{ display: 'grid', gap: '1rem' }}>
      {reviews.map(review => <ReviewCard key={review.id} review={review} />)}
    </div>
  );
};

export default ReviewList;
