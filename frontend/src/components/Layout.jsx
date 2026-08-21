import { useState, useEffect } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GlobeIcon, MenuIcon, CloseIcon, HeartIcon } from './Icons';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="app-container">
      <header className="navbar">
        <Link to="/" className="navbar-brand">
          <div className="navbar-brand-logo">
            <GlobeIcon />
          </div>
          <span>Wander<span className="navbar-brand-accent">World</span></span>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="navbar-nav desktop-nav">
          <Link to="/" className={`navbar-link ${isActive('/') ? 'active' : ''}`}>Home</Link>
          <Link to="/destinations" className={`navbar-link ${isActive('/destinations') ? 'active' : ''}`}>Destinations</Link>
          {user ? (
            <>
              <Link to="/trips" className={`navbar-link ${isActive('/trips') ? 'active' : ''}`}>Trips</Link>
              <Link to="/travel-dna" className={`navbar-link ${isActive('/travel-dna') ? 'active' : ''}`}>Travel DNA</Link>
              <Link to="/recommendations" className={`navbar-link ${isActive('/recommendations') ? 'active' : ''}`}>Recommendations</Link>
              <Link to="/wishlist" className={`navbar-link ${isActive('/wishlist') ? 'active' : ''}`} style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                <HeartIcon style={{ width: '16px', height: '16px' }} />
                Wishlist
              </Link>
              <Link to="/profile" className={`navbar-link ${isActive('/profile') ? 'active' : ''}`}>Profile</Link>
              <button onClick={handleLogout} className="btn btn-secondary btn-sm" style={{ marginLeft: '0.5rem' }}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/search" className={`navbar-link ${isActive('/search') ? 'active' : ''}`}>Search</Link>
              <Link to="/login" className="btn btn-outlined btn-sm" style={{ marginLeft: '0.5rem' }}>Login</Link>
              <Link to="/register" className="btn btn-primary btn-sm">Register</Link>
            </>
          )}
        </nav>

        {/* Mobile Navigation Toggle Button */}
        <button 
          className="mobile-toggle"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle navigation menu"
        >
          {mobileMenuOpen ? <CloseIcon /> : <MenuIcon />}
        </button>

        {/* Mobile Navigation Menu Drawer */}
        {mobileMenuOpen && (
          <nav className="mobile-nav">
            <Link to="/" className={`navbar-link ${isActive('/') ? 'active' : ''}`}>Home</Link>
            <Link to="/destinations" className={`navbar-link ${isActive('/destinations') ? 'active' : ''}`}>Destinations</Link>
            {user ? (
              <>
                <Link to="/trips" className={`navbar-link ${isActive('/trips') ? 'active' : ''}`}>Trips</Link>
                <Link to="/travel-dna" className={`navbar-link ${isActive('/travel-dna') ? 'active' : ''}`}>Travel DNA</Link>
                <Link to="/recommendations" className={`navbar-link ${isActive('/recommendations') ? 'active' : ''}`}>Recommendations</Link>
                <Link to="/wishlist" className={`navbar-link ${isActive('/wishlist') ? 'active' : ''}`} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <HeartIcon style={{ width: '18px', height: '18px' }} />
                  Wishlist
                </Link>
                <Link to="/profile" className={`navbar-link ${isActive('/profile') ? 'active' : ''}`}>Profile</Link>
                <div className="mobile-actions">
                  <button onClick={handleLogout} className="btn btn-secondary" style={{ width: '100%' }}>Logout</button>
                </div>
              </>
            ) : (
              <>
                <Link to="/search" className={`navbar-link ${isActive('/search') ? 'active' : ''}`}>Search</Link>
                <div className="mobile-actions">
                  <Link to="/login" className="btn btn-outlined" style={{ width: '100%', textAlign: 'center' }}>Login</Link>
                  <Link to="/register" className="btn btn-primary" style={{ width: '100%', textAlign: 'center' }}>Register</Link>
                </div>
              </>
            )}
          </nav>
        )}
      </header>

      <main className="page-container">
        <Outlet />
      </main>

      <footer className="footer">
        <div className="container footer-content">
          <div className="footer-brand">
            <div className="navbar-brand-logo" style={{ width: '28px', height: '28px' }}>
              <GlobeIcon style={{ width: '16px', height: '16px' }} />
            </div>
            <span>Wander<span className="navbar-brand-accent">World</span></span>
          </div>
          <p>WanderWorld © 2026. Discover your next adventure.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
