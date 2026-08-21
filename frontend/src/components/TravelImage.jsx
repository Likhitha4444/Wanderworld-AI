import React, { useState, useEffect } from 'react';

const TravelImage = ({ src, alt, className, style, fallbackSrc = 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&q=80&w=800' }) => {
  const [imageSrc, setImageSrc] = useState(src || fallbackSrc);
  const [hasError, setHasError] = useState(!src);

  useEffect(() => {
    if (!src) {
        setImageSrc(fallbackSrc);
        setHasError(true);
    } else {
        setImageSrc(src);
        setHasError(false);
    }
  }, [src, fallbackSrc]);

  const handleError = () => {
    if (!hasError) {
      setHasError(true);
      setImageSrc(fallbackSrc);
    }
  };

  return (
    <img
      src={imageSrc}
      alt={alt}
      className={className}
      style={{ ...style, objectFit: 'cover' }}
      onError={handleError}
      loading="lazy"
    />
  );
};

export default TravelImage;
