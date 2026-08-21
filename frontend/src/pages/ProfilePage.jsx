import { useAuth } from '../context/AuthContext';
import { useEffect, useState } from 'react';
import apiClient from '../api/client';
import ChangePasswordForm from '../components/ChangePasswordForm';

const ProfilePage = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await apiClient.get('/auth/profile/');
        setProfile(response.data.data);
      } catch (error) {
        console.error('Failed to fetch profile', error);
      }
    };
    fetchProfile();
  }, []);

  if (!user) return <div className="page-container">Loading...</div>;

  return (
    <div className="container" style={{ padding: 'var(--spacing-xl) 0' }}>
      <h2 style={{ marginBottom: 'var(--spacing-lg)' }}>Profile</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--spacing-lg)' }}>
        <div className="card">
          <div className="form-group">
            <label className="form-label">Email</label>
            <p style={{ color: 'var(--text-secondary)' }}>{user.email}</p>
          </div>
          <div className="form-group">
            <label className="form-label">Name</label>
            <p style={{ color: 'var(--text-secondary)' }}>{user.first_name} {user.last_name}</p>
          </div>
          {profile && (
            <>
              <div className="form-group">
                <label className="form-label">Bio</label>
                <p style={{ color: profile.bio ? 'var(--text-secondary)' : 'var(--text-muted)' }}>
                  {profile.bio || 'Not provided'}
                </p>
              </div>
              <div className="form-group">
                <label className="form-label">Location</label>
                <p style={{ color: profile.location ? 'var(--text-secondary)' : 'var(--text-muted)' }}>
                  {profile.location || 'Not provided'}
                </p>
              </div>
            </>
          )}
        </div>
        <ChangePasswordForm />
      </div>
    </div>
  );
};

export default ProfilePage;
