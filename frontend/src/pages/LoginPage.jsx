import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login({ email, password });
      navigate('/profile');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px', padding: 'var(--spacing-xl)' }}>
        <h2 style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)', color: 'var(--accent)' }}>Login</h2>
        {error && <p style={{ color: 'var(--color-danger)', textAlign: 'center', marginBottom: 'var(--spacing-md)' }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="form-group" style={{ position: 'relative' }}>
            <label className="form-label">Password</label>
            <input className="form-input" type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} required />
            <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          <div style={{ textAlign: 'right', marginBottom: 'var(--spacing-md)' }}>
            <Link to="/forgot-password" style={{ color: 'var(--accent)', textDecoration: 'none', fontSize: 'var(--font-size-sm)' }}>Forgot password?</Link>
          </div>
          <button className="btn btn-primary" style={{ width: '100%' }} type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 'var(--spacing-md)', color: 'var(--text-muted)' }}>
          Don't have an account? <Link to="/register" style={{ color: 'var(--accent)', textDecoration: 'none' }}>Register</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
