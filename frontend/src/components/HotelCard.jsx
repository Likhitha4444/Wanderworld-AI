import TravelImage from './TravelImage';
import { Link } from 'react-router-dom';

const HotelCard = ({ hotel }) => {
  const formatPrice = (price, currency) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: currency,
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
      <TravelImage 
        src={hotel.image_url} 
        alt={hotel.name} 
        style={{ width: '100%', height: '220px' }} 
      />
      <div style={{ padding: 'var(--spacing-md)' }}>
        <h4 style={{ margin: '0 0 var(--spacing-xs)' }}>{hotel.name}</h4>
        <p style={{ margin: '0 0 var(--spacing-xs)', fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>
            ★ {hotel.star_rating} • {hotel.city}, {hotel.country}
        </p>
        <p style={{ margin: '0 0 var(--spacing-sm)' }}>
          <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>Typical from</span>
          <br/>
          <span style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'bold', color: 'var(--accent)' }}>
            {formatPrice(hotel.price_per_night, hotel.currency)} / night
          </span>
        </p>
        <Link to={`/hotels/${hotel.slug}`} className="btn btn-secondary" style={{ width: '100%', textAlign: 'center', display: 'block', textDecoration: 'none' }}>View Stay</Link>
      </div>
    </div>
  );
};

export default HotelCard;
