import { useState, useEffect } from 'react';
import { getWishlist, addToWishlist, removeFromWishlist } from '../services/wishlistService';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const WishlistButton = ({ entityType, entityId }) => {
  const [wishlistItem, setWishlistItem] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      const fetchWishlist = async () => {
        const data = await getWishlist();
        const item = data.find(i => i[entityType] === entityId);
        setWishlistItem(item || null);
      };
      fetchWishlist();
    }
  }, [entityType, entityId, user]);

  const toggleWishlist = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    setLoading(true);
    try {
      if (wishlistItem) {
        await removeFromWishlist(wishlistItem.id);
        setWishlistItem(null);
      } else {
        const newItem = await addToWishlist({ [entityType]: entityId });
        setWishlistItem(newItem);
      }
    } catch (error) {
      console.error('Wishlist toggle failed', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button 
      onClick={toggleWishlist} 
      disabled={loading} 
      aria-label={wishlistItem ? "Remove from wishlist" : "Add to wishlist"}
      className="btn btn-secondary"
      style={{
        padding: '0',
        width: '48px',
        height: '48px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '24px',
        color: wishlistItem ? 'var(--danger)' : 'var(--text-primary)',
        transition: 'all 0.2s'
      }}
    >
      {wishlistItem ? "♥" : "♡"}
    </button>
  );
};

export default WishlistButton;
