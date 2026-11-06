import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, UserCheck, Bell, ChevronDown, Sparkles, Building2, Utensils, Factory, HeartHandshake } from 'lucide-react';

const roleLabels = {
  ADMIN: { title: 'MoFPI Administrator', color: 'bg-emerald-100 text-emerald-800 border-emerald-300', icon: ShieldCheck },
  KITCHEN_MANAGER: { title: 'Kitchen Manager', color: 'bg-blue-100 text-blue-800 border-blue-300', icon: Utensils },
  PROCESSING_MANAGER: { title: 'Processing Unit Lead', color: 'bg-amber-100 text-amber-800 border-amber-300', icon: Factory },
  NGO: { title: 'NGO / Food Bank Lead', color: 'bg-purple-100 text-purple-800 border-purple-300', icon: HeartHandshake }
};

export const Navbar = ({ activeTab, setActiveTab }) => {
  const { user, switchDemoRole } = useAuth();
  const currentRoleInfo = roleLabels[user?.role] || roleLabels.ADMIN;
  const RoleIcon = currentRoleInfo.icon;

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 sticky top-0 z-30 shadow-sm">
      {/* Left: Branding & Ministry Tag */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
            FW
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 text-base tracking-tight">FoodWise AI</span>
              <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                MoFPI PS 26234
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">Smart Food Waste Management & Sustainable Redistribution</p>
          </div>
        </div>
      </div>

      {/* Right: Quick Role Switcher & User Profile */}
      <div className="flex items-center gap-4">
        {/* Quick Role Switcher Pill */}
        <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-lg p-1 text-xs">
          <span className="text-slate-600 font-medium px-2 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span className="hidden md:inline">Role View:</span>
          </span>
          <button
            onClick={() => { switchDemoRole('ADMIN'); setActiveTab('admin'); }}
            className={`px-2.5 py-1 rounded font-medium transition-all ${user?.role === 'ADMIN' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Admin
          </button>
          <button
            onClick={() => { switchDemoRole('KITCHEN_MANAGER'); setActiveTab('kitchen'); }}
            className={`px-2.5 py-1 rounded font-medium transition-all ${user?.role === 'KITCHEN_MANAGER' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Kitchen
          </button>
          <button
            onClick={() => { switchDemoRole('PROCESSING_MANAGER'); setActiveTab('processing'); }}
            className={`px-2.5 py-1 rounded font-medium transition-all ${user?.role === 'PROCESSING_MANAGER' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Industry
          </button>
          <button
            onClick={() => { switchDemoRole('NGO'); setActiveTab('ngo'); }}
            className={`px-2.5 py-1 rounded font-medium transition-all ${user?.role === 'NGO' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            NGO
          </button>
        </div>

        {/* User Badge */}
        <div className="flex items-center gap-3 pl-3 border-l border-slate-200">
          <div className="text-right hidden lg:block">
            <div className="text-sm font-semibold text-slate-800">{user?.full_name || 'Active User'}</div>
            <div className="text-xs text-slate-500">{user?.email}</div>
          </div>
          <div className={`px-2.5 py-1 rounded-full text-xs font-semibold border flex items-center gap-1.5 ${currentRoleInfo.color}`}>
            <RoleIcon className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{currentRoleInfo.title}</span>
          </div>
        </div>
      </div>
    </header>
  );
};
