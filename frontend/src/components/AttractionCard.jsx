import TravelImage from './TravelImage';
import { Link } from 'react-router-dom';

const AttractionCard = ({ attraction }) => {
  return (
    <div className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
      <TravelImage 
        src={attraction.image_url} 
        alt={attraction.name} 
        style={{ width: '100%', height: '220px' }} 
      />
      <div style={{ padding: 'var(--spacing-md)' }}>
        <h4 style={{ margin: '0 0 var(--spacing-xs)' }}>{attraction.name}</h4>
        <p style={{ margin: '0 0 var(--spacing-xs)', fontSize: 'var(--font-size-sm)', color: 'var(--accent)' }}>{attraction.category}</p>
        <p style={{ margin: '0 0 var(--spacing-md)', fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>{attraction.short_description}</p>
        <Link to={`/attractions/${attraction.slug}`} className="btn btn-secondary" style={{ width: '100%', textAlign: 'center', display: 'block', textDecoration: 'none' }}>Explore</Link>
      </div>
    </div>
  );
};

export default AttractionCard;
