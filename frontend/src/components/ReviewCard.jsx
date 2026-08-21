import RatingDisplay from './RatingDisplay';

const ReviewCard = ({ review }) => {
  const initials = review.user_name ? review.user_name.charAt(0).toUpperCase() : 'A';
  
  return (
    <div className="glass-card glass-card-hover" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#040810', fontWeight: 'bold' }}>
          {initials}
        </div>
        <div style={{ flex: 1 }}>
          <h4 style={{ margin: 0 }}>{review.user_name || 'Anonymous'}</h4>
          <RatingDisplay rating={review.rating} />
        </div>
        {review.created_at && (
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {new Date(review.created_at).toLocaleDateString()}
          </span>
        )}
      </div>
      <p style={{ color: 'var(--text-secondary)', margin: 0 }}>{review.comment}</p>
    </div>
  );
};

export default ReviewCard;
