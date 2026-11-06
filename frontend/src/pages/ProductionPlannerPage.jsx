import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { 
  Sparkles, PackageCheck, AlertTriangle, CheckCircle, 
  ShoppingCart, RefreshCw, Info, ArrowRight, Lightbulb
} from 'lucide-react';

export const ProductionPlannerPage = () => {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPlan = async () => {
    setLoading(true);
    try {
      const data = await api.getSmartProductionPlan(1);
      setPlans(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlan();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-200 mb-1">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            Module 8: Holistic AI Smart Production Planning
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">AI Integrated Production & Procurement Recommendations</h1>
          <p className="text-xs text-slate-500 mt-1">
            Multi-variable optimization combining ML demand predictions, near-expiry raw materials, and historical plate waste rates.
          </p>
        </div>
        <button
          onClick={fetchPlan}
          className="px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors flex items-center gap-1.5 shadow-xs"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Recalculate Smart Plan
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Optimized Meal Portions"
          value="1,840"
          unit="total daily portions"
          icon={PackageCheck}
          color="emerald"
          change="Demand calibrated"
          subtitle="4 Core recipes planned"
        />
        <StatCard
          title="Near-Expiry Utilized"
          value="48.5"
          unit="kg raw materials"
          icon={AlertTriangle}
          color="amber"
          change="Zero spoilage loss"
          subtitle="Expires within 72 hrs"
        />
        <StatCard
          title="Procurement Recommended"
          value="64.0"
          unit="kg ingredients"
          icon={ShoppingCart}
          color="blue"
          change="Just-In-Time"
          subtitle="Avoids excess stock holding"
        />
        <StatCard
          title="Waste Buffer Reductions"
          value="-18.2%"
          unit="kitchen overprep"
          icon={Sparkles}
          color="purple"
          change="AI calibrated"
          subtitle="Dynamic 4% vs 20% gut feel"
        />
      </div>

      {/* Recommendations Cards */}
      <div className="space-y-4">
        {plans.map((item, idx) => (
          <div key={idx} className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs hover:border-emerald-300 transition-all">
            <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-slate-900">{item.item_name}</h3>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                    {item.category}
                  </span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                    {Math.round(item.confidence_score * 100)}% Confidence
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs pt-1">
                  <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                    <span className="text-slate-500 text-[11px]">Recommended Cook</span>
                    <div className="font-bold text-slate-900 text-sm mt-0.5">{item.recommended_portions} portions</div>
                    <span className="text-[10px] text-slate-400">({item.recommended_production_kg} kg raw)</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                    <span className="text-slate-500 text-[11px]">Current Pantry Stock</span>
                    <div className="font-bold text-slate-900 text-sm mt-0.5">{item.current_inventory_kg} kg</div>
                    <span className="text-[10px] text-slate-400">Available on hand</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-amber-50/60 border border-amber-100">
                    <span className="text-amber-800 text-[11px] font-medium">Expiring &lt;72 Hours</span>
                    <div className="font-bold text-amber-900 text-sm mt-0.5">{item.expiring_soon_kg} kg</div>
                    <span className="text-[10px] text-amber-700 font-semibold">Priority Consumption</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-blue-50/60 border border-blue-100">
                    <span className="text-blue-800 text-[11px] font-medium">Procurement Action</span>
                    <div className="font-bold text-blue-900 text-sm mt-0.5">
                      {item.procurement_recommendation_kg > 0 ? `Procure ${item.procurement_recommendation_kg} kg` : 'Stock Sufficient'}
                    </div>
                    <span className="text-[10px] text-blue-700">Just-In-Time delivery</span>
                  </div>
                </div>

                {/* Explainable AI Reasoning */}
                <div className="mt-3 p-3 rounded-lg bg-emerald-50/60 border border-emerald-100 text-xs">
                  <div className="font-bold text-emerald-900 flex items-center gap-1.5 mb-1.5">
                    <Lightbulb className="w-3.5 h-3.5 text-emerald-600" />
                    Explainable AI Logic (Why this recommendation?):
                  </div>
                  <ul className="space-y-1 text-slate-700 text-[11px] list-disc list-inside">
                    {item.reasoning.map((reason, rIdx) => (
                      <li key={rIdx}>{reason}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="shrink-0 flex items-center lg:flex-col justify-end gap-2 pt-2 lg:pt-0">
                <button
                  onClick={() => alert(`Recipe batch '${item.item_name}' approved for kitchen preparation schedule.`)}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-colors shadow-xs"
                >
                  Approve Batch Schedule
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
