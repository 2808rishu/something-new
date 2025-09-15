import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import FAQManagement from './pages/FAQManagement';
import Conversations from './pages/Conversations';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import './App.css';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <ConfigProvider theme={{
      token: {
        colorPrimary: '#667eea',
        borderRadius: 6,
      },
    }}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={
                <ProtectedRoute>
                  <Layout>
                    <Dashboard />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/faqs" element={
                <ProtectedRoute>
                  <Layout>
                    <FAQManagement />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/conversations" element={
                <ProtectedRoute>
                  <Layout>
                    <Conversations />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/analytics" element={
                <ProtectedRoute>
                  <Layout>
                    <Analytics />
                  </Layout>
                </ProtectedRoute>
              } />
              <Route path="/settings" element={
                <ProtectedRoute>
                  <Layout>
                    <Settings />
                  </Layout>
                </ProtectedRoute>
              } />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ConfigProvider>
  );
}

export default App;