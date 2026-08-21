import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { performSearch } from '../../services/searchService';
import DestinationCard from '../../components/DestinationCard';
import HotelCard from '../../components/HotelCard';
import AttractionCard from '../../components/AttractionCard';

const SearchPage = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      try {
        const data = await performSearch(query);
        setResults(data.results);
      } catch (error) {
        console.error('Search error:', error);
      } finally {
        setLoading(false);
      }
    };
    if (query) fetchResults();
  }, [query]);

  if (loading) return <div className="container" style={{ padding: 'var(--spacing-xl) 0' }}>Searching...</div>;

  return (
    <div className="container" style={{ padding: 'var(--spacing-xl) 0' }}>
      <h2 style={{ marginBottom: 'var(--spacing-lg)' }}>Search results for: <span style={{ color: 'var(--accent)' }}>{query}</span></h2>
      
      {results && (
        <>
          {results.destinations.length > 0 && (
            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Destinations</h3>
              <div className="grid-container">
                {results.destinations.map(d => <DestinationCard key={d.id} destination={d} />)}
              </div>
            </section>
          )}
          {results.hotels.length > 0 && (
            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Hotels</h3>
              <div className="grid-container">
                {results.hotels.map(h => <HotelCard key={h.id} hotel={h} />)}
              </div>
            </section>
          )}
          {results.attractions.length > 0 && (
            <section style={{ marginBottom: 'var(--spacing-xl)' }}>
              <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Attractions</h3>
              <div className="grid-container">
                {results.attractions.map(a => <AttractionCard key={a.id} attraction={a} />)}
              </div>
            </section>
          )}
          {results.destinations.length === 0 && results.hotels.length === 0 && results.attractions.length === 0 && (
            <div className="card" style={{ textAlign: 'center', padding: 'var(--spacing-xl)' }}>
              <h3>No results found for "{query}"</h3>
              <p style={{ color: 'var(--text-muted)' }}>Try a different search term.</p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SearchPage;
