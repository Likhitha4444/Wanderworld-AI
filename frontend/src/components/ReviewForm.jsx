import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { createReview } from '../services/reviewService';

const ReviewForm = ({ entityType, entityId, onReviewCreated }) => {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      alert('Please login to submit a review');
      return;
    }
    setLoading(true);
    try {
      await createReview({ [entityType || 'hotel']: entityId, rating, comment });
      if (onReviewCreated) onReviewCreated();
      setComment('');
    } catch (error) {
      console.error('Failed to submit review', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card" style={{ marginTop: 'var(--spacing-md)' }}>
        <h3>Write a Review</h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>Share your experience with other travelers.</p>
        <form onSubmit={handleSubmit}>
        <div className="form-group">
            <label className="form-label">Rating</label>
            <select 
            value={rating} 
            onChange={(e) => setRating(parseInt(e.target.value))} 
            className="form-input"
            >
            {[5, 4, 3, 2, 1].map(r => <option key={r} value={r}>{r} Stars</option>)}
            </select>
        </div>
        <div className="form-group">
            <label className="form-label">Your experience</label>
            <textarea 
            value={comment} 
            onChange={(e) => setComment(e.target.value)} 
            placeholder="Share your thoughts..." 
            required 
            className="form-input"
            style={{ minHeight: '120px' }}
            />
        </div>
        <button type="submit" disabled={loading} className="btn btn-primary" style={{ width: '100%' }}>
            {loading ? 'Submitting...' : 'Submit Review'}
        </button>
        </form>
    </div>
  );
};

export default ReviewForm;
