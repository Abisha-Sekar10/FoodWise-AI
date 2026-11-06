import React from 'react';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard,
  UtensilsCrossed,
  Factory,
  HeartHandshake,
  Navigation,
  Sparkles,
  BarChart3,
  ScanEye,
  Layers,
  Leaf
} from 'lucide-react';

export const Sidebar = ({ activeTab, setActiveTab }) => {
  const { user } = useAuth();

  const navItems = [
    { id: 'overview', label: 'Platform Architecture', icon: Layers, roles: ['ADMIN', 'KITCHEN_MANAGER', 'PROCESSING_MANAGER', 'NGO'] },
    { id: 'admin', label: 'Admin Dashboard', icon: LayoutDashboard, roles: ['ADMIN'] },
    { id: 'kitchen', label: 'Kitchen & Demand AI', icon: UtensilsCrossed, roles: ['ADMIN', 'KITCHEN_MANAGER'] },
    { id: 'quality', label: 'Quality Vision & IoT', icon: ScanEye, roles: ['ADMIN', 'KITCHEN_MANAGER'] },
    { id: 'processing', label: 'Processing & Machines', icon: Factory, roles: ['ADMIN', 'PROCESSING_MANAGER'] },
    { id: 'ngo', label: 'Surplus Redistribution', icon: HeartHandshake, roles: ['ADMIN', 'NGO'] },
    { id: 'routing', label: 'AI Route Logistics', icon: Navigation, roles: ['ADMIN', 'NGO', 'KITCHEN_MANAGER'] },
    { id: 'planner', label: 'Smart Production Plan', icon: Sparkles, roles: ['ADMIN', 'KITCHEN_MANAGER', 'PROCESSING_MANAGER'] },
    { id: 'sustainability', label: 'Sustainability & ESG', icon: Leaf, roles: ['ADMIN', 'KITCHEN_MANAGER', 'PROCESSING_MANAGER', 'NGO'] },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 min-h-[calc(100vh-4rem)] border-r border-slate-800">
      {/* Navigation Group */}
      <div className="flex-1 py-4 px-3 space-y-1">
        <div className="px-3 py-2 text-[11px] font-semibold tracking-wider text-slate-400 uppercase">
          Ecosystem Modules
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          const hasAccess = item.roles.includes(user?.role || 'ADMIN');

          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                  : hasAccess
                  ? 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  : 'text-slate-500 hover:bg-slate-800/40 hover:text-slate-300'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span className="truncate">{item.label}</span>
              {!hasAccess && (
                <span className="ml-auto text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                  Switch
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 text-xs text-slate-400 space-y-1 bg-slate-950/40">
        <div className="font-semibold text-slate-300">FoodWise AI Platform</div>
        <div className="text-[11px]">Backend API: <span className="text-emerald-400">Online :8000</span></div>
        <div className="text-[10px] text-slate-400">RandomForest v1.0 • OpenCV Vision</div>
      </div>
    </aside>
  );
};
