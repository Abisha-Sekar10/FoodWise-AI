import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/common/Navbar';
import { Sidebar } from './components/common/Sidebar';
import { Overview } from './pages/Overview';
import { AdminDashboard } from './pages/AdminDashboard';
import { KitchenDashboard } from './pages/KitchenDashboard';
import { QualityAndIotPage } from './pages/QualityAndIotPage';
import { ProcessingUnitDashboard } from './pages/ProcessingUnitDashboard';
import { NgoDashboard } from './pages/NgoDashboard';
import { RouteOptimizationPage } from './pages/RouteOptimizationPage';
import { SustainabilityDashboard } from './pages/SustainabilityDashboard';
import { ProductionPlannerPage } from './pages/ProductionPlannerPage';

function AppContent() {
  const [activeTab, setActiveTab] = useState('overview');
  const { user } = useAuth();

  const renderActivePage = () => {
    switch (activeTab) {
      case 'overview':
        return <Overview setActiveTab={setActiveTab} />;
      case 'admin':
        return <AdminDashboard />;
      case 'kitchen':
        return <KitchenDashboard setActiveTab={setActiveTab} />;
      case 'quality':
        return <QualityAndIotPage />;
      case 'processing':
        return <ProcessingUnitDashboard />;
      case 'ngo':
        return <NgoDashboard setActiveTab={setActiveTab} />;
      case 'routing':
        return <RouteOptimizationPage />;
      case 'planner':
        return <ProductionPlannerPage />;
      case 'sustainability':
        return <SustainabilityDashboard />;
      default:
        return <Overview setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-900">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="flex-1 overflow-y-auto p-6 md:p-8 max-w-7xl mx-auto w-full">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
