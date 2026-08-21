const RatingDisplay = ({ rating }) => {
  return (
    <span>
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} style={{ color: i < rating ? 'gold' : 'gray' }}>★</span>
      ))}
    </span>
  );
};

export default RatingDisplay;
