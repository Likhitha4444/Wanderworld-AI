import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import ProfilePage from './pages/ProfilePage';
import ErrorBoundary from './components/ErrorBoundary';
import DestinationList from './pages/destinations/DestinationList';
import DestinationDetail from './pages/destinations/DestinationDetail';
import HotelDetail from './pages/hotels/HotelDetail';
import AttractionDetail from './pages/attractions/AttractionDetail';
import SearchPage from './pages/search/SearchPage';
import TravelDnaPage from './pages/travelDna/TravelDnaPage';
import RecommendationsPage from './pages/recommendations/RecommendationsPage';
import WishlistPage from './pages/wishlist/WishlistPage';
import TripListPage from './pages/trips/TripListPage';
import TripPlannerPage from './pages/trips/TripPlannerPage';
import TripDetailPage from './pages/trips/TripDetailPage';

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<HomePage />} />
              <Route path="login" element={<LoginPage />} />
              <Route path="register" element={<RegisterPage />} />
              <Route path="forgot-password" element={<ForgotPasswordPage />} />
              <Route path="reset-password/:uidb64/:token" element={<ResetPasswordPage />} />
              <Route path="destinations" element={<DestinationList />} />
              <Route path="destinations/:slug" element={<DestinationDetail />} />
              <Route path="hotels/:slug" element={<HotelDetail />} />
              <Route path="attractions/:slug" element={<AttractionDetail />} />
              <Route path="search" element={<SearchPage />} />
              <Route path="travel-dna" element={<ProtectedRoute><TravelDnaPage /></ProtectedRoute>} />
              <Route path="recommendations" element={<ProtectedRoute><RecommendationsPage /></ProtectedRoute>} />
              <Route path="wishlist" element={<ProtectedRoute><WishlistPage /></ProtectedRoute>} />
              <Route path="trips" element={<ProtectedRoute><TripListPage /></ProtectedRoute>} />
              <Route path="trips/new" element={<ProtectedRoute><TripPlannerPage /></ProtectedRoute>} />
              <Route path="trips/:id" element={<ProtectedRoute><TripDetailPage /></ProtectedRoute>} />
              <Route 
                path="profile" 
                element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                } 
              />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
