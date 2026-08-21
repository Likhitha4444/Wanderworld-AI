import { useState } from 'react';

const Pagination = ({ pagination, onPageChange }) => {
  if (!pagination || (!pagination.next && !pagination.previous)) return null;

  return (
    <div>
      <button disabled={!pagination.previous} onClick={() => onPageChange(pagination.previous)}>
        Previous
      </button>
      <button disabled={!pagination.next} onClick={() => onPageChange(pagination.next)}>
        Next
      </button>
    </div>
  );
};

export default Pagination;
