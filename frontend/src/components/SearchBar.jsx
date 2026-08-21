import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchIcon } from './Icons';

const SearchBar = ({ showTrending = true }) => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  const handleTagClick = (tag) => {
    navigate(`/search?q=${encodeURIComponent(tag)}`);
  };

  const trendingTags = ['Goa', 'Paris', 'Tokyo', 'Bali', 'Dubai'];

  return (
    <div className="search-card-wrapper">
      <div className="search-glass-card">
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-wrapper">
            <SearchIcon className="search-icon" />
            <input
              className="search-input"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search destinations, hotels, attractions..."
            />
          </div>
          <button type="submit" className="btn btn-primary search-btn">
            Search
          </button>
        </form>
      </div>

      {showTrending && (
        <div className="trending-container">
          <span className="trending-label">🔥 Trending:</span>
          {trendingTags.map((tag) => (
            <button
              key={tag}
              type="button"
              className="trending-tag"
              onClick={() => handleTagClick(tag)}
            >
              {tag}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
