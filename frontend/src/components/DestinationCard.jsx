import { Link } from 'react-router-dom';
import TravelImage from './TravelImage';
import { ArrowRightIcon } from './Icons';

const DestinationCard = ({ destination }) => {
  if (!destination) return null;

  return (
    <Link to={`/destinations/${destination.slug}`} className="dest-card">
      <div className="dest-card-image-wrapper">
        <TravelImage 
          src={destination.cover_image_url} 
          alt={destination.name} 
          className="dest-card-image"
        />
        <div className="dest-card-badge">
          <span className="badge badge-glass">
            {destination.category || destination.country || 'DESTINATION'}
          </span>
        </div>
      </div>
      <div className="dest-card-content">
        <div className="dest-card-info">
          <h3 className="dest-card-name">{destination.name}</h3>
          <p className="dest-card-country">{destination.country}</p>
        </div>
        <div className="dest-card-btn" aria-label={`Explore ${destination.name}`}>
          <ArrowRightIcon />
        </div>
      </div>
    </Link>
  );
};

export default DestinationCard;
