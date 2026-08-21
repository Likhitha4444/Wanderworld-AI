import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import apiClient from '../api/client';

const ResetPasswordPage = () => {
  const { uidb64, token } = useParams();
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordConfirmation, setNewPasswordConfirmation] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (newPassword !== newPasswordConfirmation) {
      setError('Passwords do not match.');
      return;
    }
    setLoading(true);
    setError('');
    setMessage('');
    try {
      await apiClient.post(`/auth/reset-password/${uidb64}/${token}/`, { 
        new_password: newPassword, 
        new_password_confirmation: newPasswordConfirmation 
      });
      setMessage('Password reset successfully. You can now login.');
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err.response?.data?.message || 'Password reset failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px', padding: 'var(--spacing-xl)' }}>
        <h2 style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)', color: 'var(--accent)' }}>Reset Password</h2>
        {error && <p style={{ color: 'var(--danger)', textAlign: 'center', marginBottom: 'var(--spacing-md)' }}>{error}</p>}
        {message && <p style={{ color: 'var(--success)', textAlign: 'center', marginBottom: 'var(--spacing-md)' }}>{message}</p>}
        {!message && (
          <form onSubmit={handleSubmit}>
            <div className="form-group" style={{ position: 'relative' }}>
              <label className="form-label">New Password</label>
              <input className="form-input" type={showPassword ? 'text' : 'password'} value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
              <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                {showPassword ? 'Hide' : 'Show'}
              </button>
            </div>
            <div className="form-group">
              <label className="form-label">Confirm New Password</label>
              <input className="form-input" type="password" value={newPasswordConfirmation} onChange={(e) => setNewPasswordConfirmation(e.target.value)} required />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} type="submit" disabled={loading}>{loading ? 'Resetting...' : 'Reset Password'}</button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ResetPasswordPage;
