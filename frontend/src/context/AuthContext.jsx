import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('foodwise_user');
    return saved ? JSON.parse(saved) : {
      id: 1,
      email: 'admin@foodwise.gov.in',
      full_name: 'Dr. Rajesh Sharma (MoFPI Oversight)',
      role: 'ADMIN',
      institution_id: 1,
      kitchen_id: 1,
      processing_unit_id: 1,
      ngo_id: 1
    };
  });
  const [token, setToken] = useState(() => localStorage.getItem('foodwise_token') || 'demo_token');
  const [loading, setLoading] = useState(false);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await api.login({ email, password });
      setUser(res.user);
      setToken(res.access_token);
      localStorage.setItem('foodwise_user', JSON.stringify(res.user));
      localStorage.setItem('foodwise_token', res.access_token);
      return res.user;
    } finally {
      setLoading(false);
    }
  };

  const switchDemoRole = (role) => {
    const roleProfiles = {
      ADMIN: {
        id: 1,
        email: 'admin@foodwise.gov.in',
        full_name: 'Dr. Rajesh Sharma (MoFPI Oversight)',
        role: 'ADMIN',
        institution_id: 1,
        kitchen_id: 1
      },
      KITCHEN_MANAGER: {
        id: 2,
        email: 'kitchen@delhitechnical.edu',
        full_name: 'Ananya Desai (Mess Executive Lead)',
        role: 'KITCHEN_MANAGER',
        institution_id: 1,
        kitchen_id: 1
      },
      PROCESSING_MANAGER: {
        id: 3,
        email: 'processing@agrofresh.in',
        full_name: 'Vikram Malhotra (Plant Operations Lead)',
        role: 'PROCESSING_MANAGER',
        processing_unit_id: 1
      },
      NGO: {
        id: 4,
        email: 'contact@aahaarngo.org',
        full_name: 'Meera Sen (Aahaar NGO Director)',
        role: 'NGO',
        ngo_id: 1
      }
    };

    const targetUser = roleProfiles[role] || roleProfiles.ADMIN;
    setUser(targetUser);
    localStorage.setItem('foodwise_user', JSON.stringify(targetUser));
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('foodwise_user');
    localStorage.removeItem('foodwise_token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, switchDemoRole, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
