import { useState } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../api/client';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');
    try {
      await apiClient.post('/auth/forgot-password/', { email });
      setMessage('If an account with that email exists, you will receive a password reset link.');
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px', padding: 'var(--spacing-xl)' }}>
        <h2 style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)', color: 'var(--accent)' }}>Forgot Password</h2>
        {error && <p style={{ color: 'var(--danger)', textAlign: 'center', marginBottom: 'var(--spacing-md)' }}>{error}</p>}
        {message && <p style={{ color: 'var(--success)', textAlign: 'center', marginBottom: 'var(--spacing-md)' }}>{message}</p>}
        {!message && (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input className="form-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} type="submit" disabled={loading}>{loading ? 'Sending...' : 'Send Reset Link'}</button>
          </form>
        )}
        <p style={{ textAlign: 'center', marginTop: 'var(--spacing-md)', color: 'var(--text-muted)' }}>
          Remember your password? <Link to="/login" style={{ color: 'var(--accent)', textDecoration: 'none' }}>Login</Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
