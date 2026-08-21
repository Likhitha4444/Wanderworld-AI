import React from 'react';
import { Link } from 'react-router-dom';
import WishlistButton from './WishlistButton';

const DestinationHero = ({ destination }) => {
  return (
    <div className="destination-hero" style={{ 
      position: 'relative', 
      height: '480px', 
      width: '100%', 
      borderRadius: 'var(--radius-lg)', 
      overflow: 'hidden' 
    }}>
      {destination.cover_image_url ? (
        <img 
          src={destination.cover_image_url} 
          alt={destination.name} 
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      ) : (
        <div style={{ width: '100%', height: '100%', backgroundColor: 'var(--bg-card)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          No Image Available
        </div>
      )}
      <div style={{ 
        position: 'absolute', 
        bottom: 0, 
        left: 0, 
        right: 0, 
        padding: 'var(--spacing-xl)', 
        background: 'linear-gradient(to top, rgba(0,0,0,0.9), transparent)',
        color: 'white'
      }}>
        <h1 style={{ fontSize: 'var(--font-size-h1)', margin: '0 0 var(--spacing-sm)' }}>{destination.name}</h1>
        <p style={{ fontSize: 'var(--font-size-xl)', margin: '0 0 var(--spacing-lg)', opacity: 0.9 }}>{destination.country}</p>
        <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'center' }}>
          <WishlistButton entityType="destination" entityId={destination.id} />
          <Link to={`/trips/new?destination=${destination.id}`} className="btn btn-primary">
            Plan a Trip
          </Link>
        </div>
      </div>
    </div>
  );
};

export default DestinationHero;
