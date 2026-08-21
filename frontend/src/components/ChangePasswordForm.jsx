import { useState } from 'react';
import apiClient from '../api/client';

const ChangePasswordForm = () => {
  const [passwords, setPasswords] = useState({
    current_password: '',
    new_password: '',
    new_password_confirmation: ''
  });
  const [message, setMessage] = useState({ type: '', text: '' });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setPasswords({ ...passwords, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    if (passwords.new_password !== passwords.new_password_confirmation) {
      setMessage({ type: 'error', text: 'New passwords do not match.' });
      setLoading(false);
      return;
    }

    try {
      await apiClient.post('/auth/change-password/', passwords);
      setMessage({ type: 'success', text: 'Password changed successfully.' });
      setPasswords({ current_password: '', new_password: '', new_password_confirmation: '' });
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.message || 'Failed to change password.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Change Password</h3>
      {message.text && (
        <p style={{ 
          color: message.type === 'error' ? 'var(--danger)' : 'var(--success)',
          marginBottom: 'var(--spacing-md)',
          padding: 'var(--spacing-sm)',
          borderRadius: 'var(--radius-sm)',
          backgroundColor: message.type === 'error' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(34, 197, 94, 0.1)',
          border: message.type === 'error' ? '1px solid var(--danger)' : '1px solid var(--success)'
        }}>
          {message.text}
        </p>
      )}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Current Password <span style={{color: 'var(--danger)'}}>*</span></label>
          <input className="form-input" name="current_password" type="password" value={passwords.current_password} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label className="form-label">New Password <span style={{color: 'var(--danger)'}}>*</span></label>
          <input className="form-input" name="new_password" type="password" value={passwords.new_password} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label className="form-label">Confirm New Password <span style={{color: 'var(--danger)'}}>*</span></label>
          <input className="form-input" name="new_password_confirmation" type="password" value={passwords.new_password_confirmation} onChange={handleChange} required />
        </div>
        <button className="btn btn-primary" type="submit" disabled={loading} style={{width: '100%'}}>
          {loading ? 'Changing...' : 'Change Password'}
        </button>
      </form>
    </div>
  );
};

export default ChangePasswordForm;
