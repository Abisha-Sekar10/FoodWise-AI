import React from 'react';
import { 
  ArrowRight, ShieldCheck, UtensilsCrossed, Factory, HeartHandshake, 
  Sparkles, CheckCircle2, TrendingUp, Leaf, Database, Cpu, Navigation
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Overview = ({ setActiveTab }) => {
  const { switchDemoRole } = useAuth();

  const workflowSteps = [
    { step: 1, title: 'Consumption & Attendance Logging', desc: 'Kitchen managers log daily dining attendance and plate scrapings.', role: 'Kitchen', tab: 'kitchen' },
    { step: 2, title: 'AI Demand Forecasting', desc: 'Random Forest model forecasts consumption with attendance & seasonal features.', role: 'Kitchen', tab: 'kitchen' },
    { step: 3, title: 'Smart Production Planning', desc: 'System calculates optimal production batch sizes with tight 4% safety buffer.', role: 'Kitchen', tab: 'planner' },
    { step: 4, title: 'Production & Service Recording', desc: 'Kitchen records actual portions prepared vs served to identify delta.', role: 'Kitchen', tab: 'kitchen' },
    { step: 5, title: 'Surplus Identification', desc: 'Automatic algorithm flags leftover edible portions from production logs.', role: 'Kitchen', tab: 'kitchen' },
    { step: 6, title: '1-Click Redistribution Listing', desc: 'Listing generated with safe-use deadline, storage type, and GPS pickup pin.', role: 'Kitchen', tab: 'kitchen' },
    { step: 7, title: 'NGO Matching & Acceptance', desc: 'Nearby verified food banks review urgency, portion count, and accept donation.', role: 'NGO', tab: 'ngo' },
    { step: 8, title: 'AI Route Optimization', desc: 'Multi-stop route generated considering transit time and food safe-use deadlines.', role: 'Logistics', tab: 'routing' },
    { step: 9, title: 'Cold-Chain Delivery Tracking', desc: 'Lifecycle tracked: Available → Accepted → Scheduled → Collected → Delivered.', role: 'NGO', tab: 'ngo' },
    { step: 10, title: 'Sustainability & ESG Audit', desc: 'Admin & public audit CO2 avoided (2.5x), water conserved, and PDF reports.', role: 'Admin', tab: 'sustainability' },
  ];

  const roleCards = [
    {
      title: 'Administrator',
      role: 'ADMIN',
      desc: 'National MoFPI oversight, registered institutions & NGOs, macro waste reduction stats, and policy reports.',
      icon: ShieldCheck,
      color: 'border-emerald-200 bg-emerald-50/50 hover:border-emerald-400',
      tab: 'admin'
    },
    {
      title: 'Institutional Kitchen Manager',
      role: 'KITCHEN_MANAGER',
      desc: 'College cafeterias, hotels, hospitals: daily attendance, ML demand forecasts, image quality triage, surplus listing.',
      icon: UtensilsCrossed,
      color: 'border-blue-200 bg-blue-50/50 hover:border-blue-400',
      tab: 'kitchen'
    },
    {
      title: 'Food Processing Unit Lead',
      role: 'PROCESSING_MANAGER',
      desc: 'Industrial processing: raw material input vs output yield, machine downtime, energy intensity (kWh/kg) and anomaly alerts.',
      icon: Factory,
      color: 'border-amber-200 bg-amber-50/50 hover:border-amber-400',
      tab: 'processing'
    },
    {
      title: 'NGO & Food Bank Coordinator',
      role: 'NGO',
      desc: 'Discovery of nearby surplus food, acceptance matching, cold-chain van scheduling, and delivery confirmation.',
      icon: HeartHandshake,
      color: 'border-purple-200 bg-purple-50/50 hover:border-purple-400',
      tab: 'ngo'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Banner */}
      <div className="bg-gradient-to-r from-emerald-900 via-emerald-800 to-teal-900 text-white rounded-2xl p-8 shadow-sm relative overflow-hidden">
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-700/60 border border-emerald-500/40 text-emerald-200 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            Problem Statement 26234 • MoFPI Official Software Solution
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
            FoodWise AI – Smart Food Waste Reduction & Sustainable Redistribution Ecosystem
          </h1>
          <p className="mt-3 text-emerald-100 text-sm sm:text-base leading-relaxed">
            An end-to-end, AI-powered enterprise platform connecting institutional kitchens, industrial food processing units, 
            and verified NGOs to eradicate food waste through demand forecasting, computer vision quality screening, 
            IoT cold storage monitoring, route-optimized redistribution, and verifiable ESG sustainability metrics.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <button
              onClick={() => setActiveTab('kitchen')}
              className="px-4 py-2.5 bg-white text-emerald-900 rounded-lg font-semibold text-sm hover:bg-emerald-50 transition-all shadow-sm flex items-center gap-2"
            >
              Launch Kitchen Demand AI
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('sustainability')}
              className="px-4 py-2.5 bg-emerald-700/80 hover:bg-emerald-700 text-white rounded-lg font-semibold text-sm transition-all border border-emerald-500/50 flex items-center gap-2"
            >
              <Leaf className="w-4 h-4" />
              View ESG & Sustainability Audit
            </button>
          </div>
        </div>
      </div>

      {/* Role Navigation Cards */}
      <div>
        <div className="mb-4">
          <h2 className="text-lg font-bold text-slate-900">Explore by User Role</h2>
          <p className="text-sm text-slate-500">Each role features dedicated dashboards, custom telemetry, and role-based permissions.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {roleCards.map((rc) => {
            const Icon = rc.icon;
            return (
              <div
                key={rc.role}
                onClick={() => { switchDemoRole(rc.role); setActiveTab(rc.tab); }}
                className={`p-5 rounded-xl border cursor-pointer transition-all hover:shadow-md flex flex-col justify-between ${rc.color}`}
              >
                <div>
                  <div className="w-10 h-10 rounded-lg bg-white shadow-xs flex items-center justify-center mb-3">
                    <Icon className="w-5 h-5 text-slate-800" />
                  </div>
                  <h3 className="font-bold text-slate-900 text-base">{rc.title}</h3>
                  <p className="text-xs text-slate-600 mt-2 leading-relaxed">{rc.desc}</p>
                </div>
                <div className="mt-4 pt-3 border-t border-slate-200/60 flex items-center justify-between text-xs font-semibold text-slate-800">
                  <span>Open Role Dashboard</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 10-Step End-to-End Workflow */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <div className="mb-6">
          <div className="inline-block px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold text-xs mb-1">
            End-to-End Operational Lifecycle
          </div>
          <h2 className="text-xl font-bold text-slate-900">Complete 10-Step Redistribution Workflow</h2>
          <p className="text-sm text-slate-500">From initial dining demand forecasting to verified meal delivery at food banks.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {workflowSteps.map((ws) => (
            <div
              key={ws.step}
              onClick={() => setActiveTab(ws.tab)}
              className="p-4 rounded-xl border border-slate-100 bg-slate-50/60 hover:bg-emerald-50/50 hover:border-emerald-200 cursor-pointer transition-all flex items-start gap-3.5"
            >
              <div className="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
                {ws.step}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-slate-800">{ws.title}</h4>
                  <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-white text-slate-600 border border-slate-200">
                    {ws.role}
                  </span>
                </div>
                <p className="text-xs text-slate-600 mt-1">{ws.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Technology & AI Architecture Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-2 mb-3 text-emerald-700 font-bold text-sm">
            <Cpu className="w-4 h-4" />
            Machine Learning Engine
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Random Forest Regressor (Scikit-Learn) predicts dining consumption with attendance, seasonal variance, and weather data. 
            IsolationForest algorithms detect anomalies in kitchen plate waste and machine downtime.
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-2 mb-3 text-blue-700 font-bold text-sm">
            <Navigation className="w-4 h-4" />
            Logistics & Route Optimization
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Greedy 2-Opt and Nearest Neighbor heuristics calculate multi-stop redistribution circuits, 
            prioritizing short safe-use deadlines to ensure zero expired meal drops.
          </p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-2 mb-3 text-purple-700 font-bold text-sm">
            <Database className="w-4 h-4" />
            Normalized Relational Database
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            PostgreSQL & SQLAlchemy schema with 22 normalized tables, role-based JWT access controls, 
            and complete audit trails for every donation transaction.
          </p>
        </div>
      </div>
    </div>
  );
};
