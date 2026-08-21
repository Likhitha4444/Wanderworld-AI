import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirmation: '',
    first_name: '',
    last_name: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState({});
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError({});
    try {
      await register(formData);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.errors || { general: 'Registration failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px', padding: 'var(--spacing-xl)' }}>
        <h2 style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)', color: 'var(--accent)' }}>Register</h2>
        {error.general && <p style={{ color: 'var(--danger)', textAlign: 'center', marginBottom: 'var(--spacing-md)' }}>{error.general}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">First Name</label>
            <input className="form-input" name="first_name" type="text" value={formData.first_name} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label className="form-label">Last Name</label>
            <input className="form-input" name="last_name" type="text" value={formData.last_name} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" name="email" type="email" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-group" style={{ position: 'relative' }}>
            <label className="form-label">Password</label>
            <input className="form-input" name="password" type={showPassword ? 'text' : 'password'} value={formData.password} onChange={handleChange} required />
            <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input className="form-input" name="password_confirmation" type="password" value={formData.password_confirmation} onChange={handleChange} required />
          </div>
          <button className="btn btn-primary" style={{ width: '100%' }} type="submit" disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 'var(--spacing-md)', color: 'var(--text-muted)' }}>
          Already have an account? <Link to="/login" style={{ color: 'var(--accent)', textDecoration: 'none' }}>Login</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
