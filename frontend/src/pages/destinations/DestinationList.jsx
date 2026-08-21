import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getDestinations } from '../../services/destinationService';
import Pagination from '../../components/Pagination';

const DestinationList = () => {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({});
  const [filters, setFilters] = useState({});

  const fetchDestinations = async (url) => {
    setLoading(true);
    try {
      const response = url ? await apiClient.get(url) : await getDestinations(filters);
      setDestinations(response.results || response);
      setPagination({ next: response.next, previous: response.previous, count: response.count });
    } catch (error) {
      console.error('Error fetching destinations:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDestinations();
  }, [filters]);

  const renderSkeletons = () => (
    <div className="grid-container">
      {[1, 2, 3, 4, 5, 6].map(i => (
        <div key={i} className="card" style={{ height: '350px', backgroundColor: 'var(--bg-card)' }} />
      ))}
    </div>
  );

  return (
    <div style={{ backgroundColor: 'var(--bg-primary)', minHeight: '100vh', color: 'var(--text-primary)' }}>
      <header className="container" style={{ padding: 'var(--spacing-xl) 0 var(--spacing-lg)', textAlign: 'center' }}>
        <h1 style={{ fontSize: 'var(--font-size-h1)', margin: '0 0 var(--spacing-sm)' }}>Explore Destinations</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--spacing-lg)', fontSize: 'var(--font-size-lg)' }}>Discover places worth remembering.</p>
        
        <div style={{ display: 'flex', gap: 'var(--spacing-md)', justifyContent: 'center', flexWrap: 'wrap' }}>
          <input 
            className="form-input"
            type="text" 
            placeholder="Search..." 
            style={{ maxWidth: '300px' }}
            onChange={e => setFilters({...filters, search: e.target.value})} 
          />
          <input 
            className="form-input"
            type="text" 
            placeholder="Country..." 
            style={{ maxWidth: '200px' }}
            onChange={e => setFilters({...filters, country: e.target.value})} 
          />
        </div>
      </header>
      
      <main className="container" style={{ paddingBottom: 'var(--spacing-xl)' }}>
        {loading ? renderSkeletons() : (
          destinations.length > 0 ? (
            <div className="grid-container">
              {destinations.map((dest) => (
                <div key={dest.id} className="card" style={{ display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden', transition: 'all 0.3s ease' }} 
                     onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-8px)'}
                     onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
                  {dest.cover_image_url ? (
                    <div style={{ overflow: 'hidden' }}>
                        <img 
                          src={dest.cover_image_url} 
                          alt={dest.name} 
                          style={{ width: '100%', height: '220px', objectFit: 'cover', transition: 'transform 0.5s ease' }} 
                          onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                          onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
                        />
                    </div>
                  ) : (
                    <div style={{ width: '100%', height: '220px', backgroundColor: 'var(--bg-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <span style={{ color: 'var(--text-muted)' }}>{dest.name}</span>
                    </div>
                  )}
                  <div style={{ padding: 'var(--spacing-md)' }}>
                    <h3 style={{ margin: '0 0 var(--spacing-xs)', fontSize: 'var(--font-size-lg)' }}>{dest.name}</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--spacing-sm)', fontSize: 'var(--font-size-sm)' }}>{dest.country}</p>
                    <p style={{ color: 'var(--text-muted)', marginBottom: 'var(--spacing-md)', fontSize: 'var(--font-size-sm)', height: '40px', overflow: 'hidden' }}>{dest.short_description}</p>
                    <Link to={`/destinations/${dest.slug}`} className="btn btn-primary" style={{ width: '100%' }}>Explore</Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="card" style={{ textAlign: 'center', padding: 'var(--spacing-xl)' }}>
              <h3 style={{ color: 'var(--text-secondary)' }}>No destinations found</h3>
              <p style={{ color: 'var(--text-muted)' }}>Try another destination or clear your filters.</p>
              <button className="btn btn-secondary" onClick={() => setFilters({})} style={{ marginTop: 'var(--spacing-md)' }}>Clear Filters</button>
            </div>
          )
        )}
        
        {!loading && destinations.length > 0 && (
          <div style={{ marginTop: 'var(--spacing-xl)', display: 'flex', justifyContent: 'center' }}>
            <Pagination pagination={pagination} onPageChange={fetchDestinations} />
          </div>
        )}
      </main>
    </div>
  );
};

export default DestinationList;
