import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Layout from './components/Layout';
import DoctorDashboard from './pages/doctor/Dashboard';
import EncounterDetail from './pages/doctor/EncounterDetail';
import Admission from './pages/doctor/Admission';
import PatientDashboard from './pages/patient/Dashboard';
import LLMHealthPage from './pages/admin/LLMHealth';
import DevTools from './pages/admin/DevTools';

// Protected Route Component
const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode, allowedRoles?: string[] }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Redirect to their own dashboard if they try to access unauthorized pages
    return <Navigate to={user.role === 'doctor' ? '/doctor/dashboard' : '/patient/dashboard'} />;
  }

  return <>{children}</>;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Doctor Routes */}
          <Route path="/doctor" element={
            <ProtectedRoute allowedRoles={['doctor']}>
              <Layout />
            </ProtectedRoute>
          }>
            <Route path="dashboard" element={<DoctorDashboard />} />
            <Route path="encounters/:id" element={<EncounterDetail />} />
            <Route path="admit" element={<Admission />} />
          </Route>

          {/* Patient Routes */}
          <Route path="/patient" element={
            <ProtectedRoute allowedRoles={['patient']}>
              <Layout />
            </ProtectedRoute>
          }>
            <Route path="dashboard" element={<PatientDashboard />} />
          </Route>

          {/* Admin/Dev Routes (Accessible by doctors for demo purposes) */}
          <Route path="/admin" element={
            <ProtectedRoute allowedRoles={['doctor', 'admin']}>
              <Layout />
            </ProtectedRoute>
          }>
            <Route path="llm-status" element={<LLMHealthPage />} />
            <Route path="dev-tools" element={<DevTools />} />
          </Route>

          {/* Default Redirect */}
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;