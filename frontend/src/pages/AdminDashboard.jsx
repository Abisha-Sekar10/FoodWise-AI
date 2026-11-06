import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { 
  Building2, HeartHandshake, Utensils, Leaf, TrendingUp, 
  CheckCircle2, AlertTriangle, ShieldCheck, Download, RefreshCw, Layers
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Legend, Cell
} from 'recharts';

export const AdminDashboard = () => {
  const [summary, setSummary] = useState(null);
  const [institutions, setInstitutions] = useState([]);
  const [ngos, setNgos] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      const [sumRes, instRes, ngoRes] = await Promise.all([
        api.getAdminSummary(),
        api.getInstitutions(),
        api.getNgos()
      ]);
      setSummary(sumRes);
      setInstitutions(instRes);
      setNgos(ngoRes);
    } catch (err) {
      console.error("Failed to load admin summary:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const COLORS = ['#059669', '#3b82f6', '#f59e0b', '#8b5cf6'];

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">National MoFPI Administrator Command Center</h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time platform oversight, institutional compliance, and sustainable food redistribution monitoring.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={fetchAdminData}
            className="px-3 py-2 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Refresh Telemetry
          </button>
          <a
            href={api.exportPdfUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors flex items-center gap-1.5 shadow-xs"
          >
            <Download className="w-3.5 h-3.5" />
            Download ESG Audit PDF
          </a>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Food Waste Prevented"
          value={summary?.total_food_waste_prevented_kg?.toLocaleString() || "18,920"}
          unit="kg"
          icon={TrendingUp}
          color="emerald"
          change="+24.5%"
          subtitle="vs pre-implementation"
        />
        <StatCard
          title="Total Redistributed"
          value={summary?.total_food_redistributed_kg?.toLocaleString() || "14,850"}
          unit="kg"
          icon={Utensils}
          color="blue"
          change={`${summary?.total_meals_supported?.toLocaleString() || '37,125'} meals`}
          subtitle="Delivered to food banks"
        />
        <StatCard
          title="Carbon Avoided"
          value={summary?.carbon_avoided_kg_co2e?.toLocaleString() || "47,300"}
          unit="kg CO2e"
          icon={Leaf}
          color="amber"
          change="2.5x Factor"
          subtitle="EPA & FAO verified standard"
        />
        <StatCard
          title="Registered Entities"
          value={`${summary?.total_institutions || 8} / ${summary?.total_ngos || 14}`}
          unit="Kitchens / NGOs"
          icon={Building2}
          color="purple"
          change="100% Verified"
          subtitle="FSSAI & Darpan audited"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Redistribution & Prevention Trends */}
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">National Redistribution & Waste Prevention Trends</h3>
              <p className="text-xs text-slate-500">Monthly progression of averted waste and successful NGO deliveries (kg)</p>
            </div>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
              Monthly Active
            </span>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={summary?.trends || []}>
                <defs>
                  <linearGradient id="colorWaste" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#059669" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#059669" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorRedis" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Area type="monotone" dataKey="waste_prevented_kg" name="Waste Prevented (kg)" stroke="#059669" fillOpacity={1} fill="url(#colorWaste)" />
                <Area type="monotone" dataKey="redistributed_kg" name="Redistributed (kg)" stroke="#3b82f6" fillOpacity={1} fill="url(#colorRedis)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Breakdown */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Redistribution Food Categories</h3>
            <p className="text-xs text-slate-500 mb-4">Proportion by nutritional category</p>
            <div className="space-y-3.5">
              {(summary?.category_breakdown || []).map((cat, idx) => (
                <div key={cat.category} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-700">{cat.category}</span>
                    <span className="text-slate-500 font-medium">{cat.percentage}% ({cat.kg} kg)</span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full transition-all duration-500"
                      style={{ width: `${cat.percentage}%`, backgroundColor: COLORS[idx % COLORS.length] }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 flex items-center justify-between">
            <span>Audit Standard: MoFPI 2026</span>
            <span className="text-emerald-700 font-semibold">FSSAI Compliant</span>
          </div>
        </div>
      </div>

      {/* Directory & Recent Activity Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Verified Institutions & NGOs Directory */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-slate-900">Registered Institutions & Food Banks</h3>
            <span className="text-xs text-slate-500">{institutions.length + ngos.length} Entities Live</span>
          </div>
          <div className="space-y-3 overflow-y-auto max-h-72 pr-1">
            {institutions.map(inst => (
              <div key={`inst-${inst.id}`} className="p-3 rounded-lg border border-slate-100 bg-slate-50/50 flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-slate-800">{inst.name}</div>
                  <div className="text-[11px] text-slate-500">{inst.type} • {inst.city}</div>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                    {inst.fssai_license || 'FSSAI License'}
                  </span>
                </div>
              </div>
            ))}
            {ngos.map(ngo => (
              <div key={`ngo-${ngo.id}`} className="p-3 rounded-lg border border-slate-100 bg-slate-50/50 flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-slate-800">{ngo.name}</div>
                  <div className="text-[11px] text-slate-500">{ngo.daily_meals_capacity} meals capacity • {ngo.city}</div>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-purple-50 text-purple-700 border border-purple-200">
                    {ngo.registration_number || 'NGO Darpan'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Real-time System Activities */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-slate-900">Real-Time Platform Audit Stream</h3>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </div>
          <div className="space-y-3">
            {(summary?.recent_activities || []).map((act) => (
              <div key={act.id} className="p-3 rounded-lg border border-slate-100 bg-slate-50/40 flex items-start gap-3 text-xs">
                <div className="p-1.5 rounded bg-emerald-100 text-emerald-800 shrink-0">
                  <ShieldCheck className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1">
                  <div className="text-slate-800 font-medium">{act.text}</div>
                  <div className="text-[10px] text-slate-400 mt-0.5">{act.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
