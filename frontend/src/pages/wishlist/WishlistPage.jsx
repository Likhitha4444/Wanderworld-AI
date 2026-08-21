import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getWishlist, removeFromWishlist } from '../../services/wishlistService';
import TravelImage from '../../components/TravelImage';
import { HeartIcon, ArrowRightIcon } from '../../components/Icons';

const WishlistPage = () => {
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [removingId, setRemovingId] = useState(null);

  useEffect(() => {
    fetchWishlist();
  }, []);

  const fetchWishlist = async () => {
    setLoading(true);
    try {
      const data = await getWishlist();
      const items = Array.isArray(data) ? data : data.results || [];
      setWishlist(items);
    } catch (error) {
      console.error('Failed to fetch wishlist', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (id, e) => {
    e.preventDefault();
    e.stopPropagation();
    setRemovingId(id);
    try {
      await removeFromWishlist(id);
      setWishlist(prev => prev.filter(item => item.id !== id));
    } catch (error) {
      console.error('Failed to remove from wishlist', error);
    } finally {
      setRemovingId(null);
    }
  };

  const getItemInfo = (item) => {
    if (item.destination_detail) {
      return {
        type: 'DESTINATION',
        name: item.destination_detail.name,
        location: item.destination_detail.country,
        description: item.destination_detail.short_description || item.destination_detail.description,
        image: item.destination_detail.cover_image_url || null,
        link: `/destinations/${item.destination_detail.slug}`
      };
    }
    if (item.hotel_detail) {
      return {
        type: 'HOTEL',
        name: item.hotel_detail.name,
        location: item.hotel_detail.city ? `${item.hotel_detail.city}, ${item.hotel_detail.country}` : item.hotel_detail.country,
        description: item.hotel_detail.address || item.hotel_detail.short_description,
        image: item.hotel_detail.cover_image_url || item.hotel_detail.image_url || null,
        link: `/hotels/${item.hotel_detail.slug}`
      };
    }
    if (item.attraction_detail) {
      return {
        type: 'ATTRACTION',
        name: item.attraction_detail.name,
        location: item.attraction_detail.city ? `${item.attraction_detail.city}, ${item.attraction_detail.country}` : item.attraction_detail.country,
        description: item.attraction_detail.short_description || item.attraction_detail.description,
        image: item.attraction_detail.cover_image_url || item.attraction_detail.image_url || null,
        link: `/attractions/${item.attraction_detail.slug}`
      };
    }
    return {
      type: 'ITEM',
      name: `Saved Item #${item.id}`,
      location: '',
      description: '',
      image: null,
      link: '/destinations'
    };
  };

  return (
    <div className="container" style={{ padding: '3rem 1.5rem 5rem' }}>
      {/* Header */}
      <div style={{ marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: 'var(--font-size-h2)', fontWeight: 800, color: '#FFFFFF', marginBottom: '0.5rem' }}>
          My Wishlist
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem' }}>
          Your saved travel destinations, hotels and attractions
        </p>
      </div>

      {loading ? (
        <div className="glass-card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <div className="spinner" style={{ margin: '0 auto 1rem' }}></div>
          <p style={{ color: 'var(--text-secondary)' }}>Loading your saved places...</p>
        </div>
      ) : wishlist.length === 0 ? (
        /* Empty State */
        <div className="glass-card" style={{ textAlign: 'center', padding: '4rem 2rem', maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ fontSize: '3.5rem', marginBottom: '1rem', lineHeight: 1 }}>❤️</div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '0.75rem' }}>
            Your wishlist is empty
          </h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', lineHeight: 1.6 }}>
            Start exploring destinations, hotels and attractions and save the places you'd love to visit.
          </p>
          <Link to="/destinations" className="btn btn-primary btn-lg">
            Explore Destinations
          </Link>
        </div>
      ) : (
        /* Grid of Saved Items */
        <div className="grid-container" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.75rem' }}>
          {wishlist.map(item => {
            const info = getItemInfo(item);
            return (
              <div key={item.id} className="glass-card glass-card-hover" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                
                {/* Image & Type Badge Overlay */}
                <div style={{ position: 'relative', width: '100%', height: '220px', backgroundColor: '#0A0E17', overflow: 'hidden' }}>
                  <TravelImage 
                    src={info.image} 
                    alt={info.name} 
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                  <div style={{ position: 'absolute', top: '1rem', left: '1rem', zIndex: 2 }}>
                    <span className="badge badge-glass">
                      {info.type}
                    </span>
                  </div>

                  {/* Remove / Heart Button Overlay */}
                  <button
                    onClick={(e) => handleRemove(item.id, e)}
                    disabled={removingId === item.id}
                    title="Remove from wishlist"
                    style={{
                      position: 'absolute',
                      top: '1rem',
                      right: '1rem',
                      zIndex: 2,
                      width: '38px',
                      height: '38px',
                      borderRadius: '50%',
                      background: 'rgba(10, 15, 26, 0.75)',
                      backdropFilter: 'blur(8px)',
                      border: '1px solid rgba(255, 255, 255, 0.15)',
                      color: 'var(--danger)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <HeartIcon filled={true} style={{ width: '18px', height: '18px', color: '#EF4444' }} />
                  </button>
                </div>

                {/* Content Details */}
                <div style={{ padding: '1.25rem 1.5rem', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between', background: 'linear-gradient(180deg, rgba(14, 20, 34, 0.9) 0%, rgba(10, 15, 26, 0.95) 100%)' }}>
                  <div>
                    <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#FFFFFF', margin: '0 0 0.25rem 0' }}>
                      {info.name}
                    </h3>
                    {info.location && (
                      <p style={{ color: 'var(--accent)', fontSize: '0.875rem', fontWeight: 500, margin: '0 0 0.75rem 0' }}>
                        {info.location}
                      </p>
                    )}
                    {info.description && (
                      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', margin: '0 0 1.25rem 0', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden', lineHeight: 1.5 }}>
                        {info.description}
                      </p>
                    )}
                  </div>

                  <Link to={info.link} className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                    View Details <ArrowRightIcon style={{ width: '16px', height: '16px', marginLeft: '4px' }} />
                  </Link>
                </div>

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default WishlistPage;
