import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getDestinations } from '../services/destinationService';
import { useAuth } from '../context/AuthContext';
import SearchBar from '../components/SearchBar';
import DestinationCard from '../components/DestinationCard';
import apiClient from '../api/client';
import { 
  PlaneIcon, 
  CompassIcon, 
  DnaIcon, 
  SparklesIcon, 
  ShieldIcon, 
  ArrowRightIcon 
} from '../components/Icons';

const bgImage = 'https://img.magnific.com/free-photo/photographer-stands-with-camera-shore-with-great-evening-sky-him_1304-5307.jpg?semt=ais_hybrid&w=740&q=80';

const HomePage = () => {
  const [destinations, setDestinations] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchHomeData = async () => {
      setLoading(true);
      try {
        const [destRes, recRes] = await Promise.all([
          getDestinations({ is_featured: true }),
          user ? apiClient.get('/recommendations/').catch(() => ({ data: [] })) : Promise.resolve({ data: [] })
        ]);
        setDestinations(destRes.results || destRes || []);
        setRecommendations(recRes.data?.data || []);
      } catch (err) {
        console.error('Error fetching home data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHomeData();
  }, [user]);

  return (
    <div style={{ backgroundColor: 'var(--bg-primary)', color: 'var(--text-primary)', minHeight: '100vh' }}>
      
      {/* 1. Cinematic Hero Section */}
      <section 
        className="hero-section" 
        style={{ 
          backgroundImage: `linear-gradient(to bottom, rgba(5, 8, 13, 0.45) 0%, rgba(5, 8, 13, 0.75) 65%, rgba(5, 8, 13, 1) 100%), url("${bgImage}")`,
          backgroundSize: 'cover',
          backgroundPosition: 'center center',
          backgroundRepeat: 'no-repeat'
        }}
      >
        <div className="hero-overlay" />
        
        <div className="hero-container">
          {/* Small pill */}
          <div className="hero-badge">
            <PlaneIcon />
            <span>Your adventure awaits</span>
          </div>

          {/* Main heading */}
          <h1 className="hero-title">
            Discover your next<br />
            <span className="text-cyan">journey.</span>
          </h1>

          {/* Supporting text */}
          <p className="hero-subtitle">
            Explore breathtaking destinations, discover unique attractions, and create personalized trips with WanderWorld.
          </p>

          {/* Glass Search Box */}
          <SearchBar showTrending={true} />
        </div>
      </section>

      {/* 2. Feature Highlights Section */}
      <section className="features-section">
        <div className="container">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <CompassIcon />
              </div>
              <h3 className="feature-title">Smart Discovery</h3>
              <p className="feature-desc">Find the best places to stay, eat and explore.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <DnaIcon />
              </div>
              <h3 className="feature-title">Travel DNA</h3>
              <p className="feature-desc">Get recommendations based on your unique preferences.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <SparklesIcon />
              </div>
              <h3 className="feature-title">AI Trip Planner</h3>
              <p className="feature-desc">Plan the perfect trip with our AI-powered itinerary.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <ShieldIcon />
              </div>
              <h3 className="feature-title">Trusted & Secure</h3>
              <p className="feature-desc">Your data is safe with us while you travel the world.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Popular Destinations Section */}
      <section className="container" style={{ padding: '3rem 1.5rem 4rem' }}>
        <div className="section-header">
          <h2 className="section-title">Popular Destinations</h2>
          <Link to="/destinations" className="section-link">
            View all destinations <ArrowRightIcon />
          </Link>
        </div>

        {loading ? (
          <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>Loading destinations...</p>
          </div>
        ) : destinations.length > 0 ? (
          <div className="grid-container">
            {destinations.slice(0, 4).map(dest => (
              <DestinationCard key={dest.id} destination={dest} />
            ))}
          </div>
        ) : (
          <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
            <h3 style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>No featured destinations found yet.</h3>
            <Link to="/destinations" className="btn btn-secondary">Explore Destinations</Link>
          </div>
        )}
      </section>

      {/* 4. Recommendations / Travel DNA Section (Preserved Functionality) */}
      <section className="container" style={{ padding: '1rem 1.5rem 4rem' }}>
        <div className="section-header">
          <h2 className="section-title">{user ? 'Made for you' : 'Discover travel that fits you'}</h2>
        </div>

        {user ? (
          recommendations.length > 0 ? (
            <div className="grid-container" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
              {recommendations.slice(0, 3).map(rec => (
                <div key={rec.id} className="glass-card glass-card-hover">
                  <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '0.5rem', color: '#FFFFFF' }}>{rec.name}</h3>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.925rem' }}>{rec.reason}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
              <h3 style={{ marginBottom: '0.5rem', fontSize: '1.25rem' }}>Made for you</h3>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>Complete your Travel DNA to see personalized recommendations.</p>
              <Link to="/travel-dna" className="btn btn-primary">Create Travel DNA</Link>
            </div>
          )
        ) : (
          <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '1.05rem' }}>Understand your travel preferences with WanderWorld.</p>
            <Link to="/register" className="btn btn-primary">Create your Travel DNA</Link>
          </div>
        )}
      </section>

      {/* 5. Premium CTA Section */}
      <section className="container cta-section">
        <div className="cta-card">
          <h2 className="cta-title">Ready to plan your next adventure?</h2>
          <p className="cta-subtitle">
            Create a trip, get personalized recommendations and explore the world your way.
          </p>
          <div className="cta-actions">
            <Link to="/trips/new" className="btn btn-primary btn-lg">
              Plan a Trip
            </Link>
            <Link to="/trips/new" className="btn btn-outlined btn-lg">
              <SparklesIcon style={{ width: '18px', height: '18px' }} />
              Create with AI
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
};

export default HomePage;
