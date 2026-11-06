import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { 
  Factory, Gauge, Zap, AlertTriangle, CheckCircle, 
  Plus, Activity, Wrench, ShieldAlert, TrendingDown, RefreshCw
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend
} from 'recharts';

export const ProcessingUnitDashboard = () => {
  const [summary, setSummary] = useState(null);
  const [records, setRecords] = useState([]);
  const [machines, setMachines] = useState([]);
  const [energyLogs, setEnergyLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Batch Form State
  const [batchNo, setBatchNo] = useState('');
  const [productName, setProductName] = useState('Canned Mixed Veg Curries');
  const [rawInputKg, setRawInputKg] = useState(5000);
  const [finishedOutputKg, setFinishedOutputKg] = useState(4600);
  const [plannedKg, setPlannedKg] = useState(4700);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [sumRes, recRes, macRes, nrgRes] = await Promise.all([
        api.getProcessingSummary(1),
        api.getProductionRecords(1),
        api.getMachines(1),
        api.getEnergyRecords(1)
      ]);
      setSummary(sumRes);
      setRecords(recRes);
      setMachines(macRes);
      setEnergyLogs(nrgRes);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddBatch = async (e) => {
    e.preventDefault();
    const batchId = batchNo || `BATCH-AGRO-26-${Math.floor(Math.random() * 900 + 100)}`;
    try {
      await api.addProductionRecord({
        unit_id: 1,
        batch_number: batchId,
        product_name: productName,
        raw_material_input_kg: Number(rawInputKg),
        finished_product_output_kg: Number(finishedOutputKg),
        planned_production_kg: Number(plannedKg)
      });
      setBatchNo('');
      fetchData();
      alert(`Batch ${batchId} added successfully! Yield calculated.`);
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  // Prepare chart data comparing planned vs actual
  const chartData = records.slice(0, 7).reverse().map(r => ({
    name: r.batch_number.replace('BATCH-AGRO-26-', '#'),
    planned: r.planned_production_kg,
    actual: r.finished_product_output_kg,
    loss: r.material_loss_kg,
    efficiency: r.production_efficiency_pct
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200 mb-1">
            <Factory className="w-3.5 h-3.5 text-amber-600" />
            Module 5: Industrial Food Processing Monitoring
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">AgroFresh Food Processing Plant – Operational Center</h1>
          <p className="text-xs text-slate-500 mt-1">
            Raw material input yields, machine overall equipment effectiveness (OEE), and energy optimization.
          </p>
        </div>
        <button
          onClick={fetchData}
          className="px-3 py-2 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Industrial Telemetry
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Production Efficiency"
          value={`${summary?.production_efficiency_pct || 90.8}%`}
          unit="Yield rate"
          icon={Gauge}
          color="emerald"
          change="Target: > 88%"
          subtitle="Finished output / Raw input"
        />
        <StatCard
          title="Cumulative Material Loss"
          value={summary?.total_material_loss_kg?.toLocaleString() || "1,020"}
          unit="kg"
          icon={TrendingDown}
          color="amber"
          change="9.2% Loss rate"
          subtitle="Peeling, trimmings & steam"
        />
        <StatCard
          title="Machine Downtime"
          value={summary?.total_machine_downtime_minutes || "40"}
          unit="minutes"
          icon={Wrench}
          color="blue"
          change="Availability 94.6%"
          subtitle="3 Active lines online"
        />
        <StatCard
          title="Specific Energy"
          value="0.309"
          unit="kWh / kg"
          icon={Zap}
          color="purple"
          change="Normal benchmark"
          subtitle="Electricity & thermal consumption"
        />
      </div>

      {/* Anomaly Alerts from Module 6 Engine */}
      {summary?.anomalies_detected && summary.anomalies_detected.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-rose-600" />
            AI Operational Inefficiency & Anomaly Warnings
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {summary.anomalies_detected.map((anom, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-rose-50/70 border border-rose-200 text-xs">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-rose-900">{anom.title}</span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-800">
                    {anom.severity}
                  </span>
                </div>
                <div className="text-[11px] font-semibold text-rose-700 mb-1">{anom.metric}</div>
                <p className="text-slate-700 mb-2 leading-relaxed">{anom.message}</p>
                <div className="text-[11px] font-semibold text-emerald-800 bg-white/70 p-2 rounded-lg border border-rose-100">
                  🔧 Action: {anom.recommendation}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Production Chart: Planned vs Actual Output */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Planned vs Actual Finished Production Yield</h3>
              <p className="text-xs text-slate-500">Comparing target output against achieved batch production (kg)</p>
            </div>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
              Batch Tracking
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="planned" name="Planned Output (kg)" fill="#94a3b8" radius={[4, 4, 0, 0]} />
                <Bar dataKey="actual" name="Actual Output (kg)" fill="#059669" radius={[4, 4, 0, 0]} />
                <Bar dataKey="loss" name="Material Loss (kg)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Log New Industrial Batch Form */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-1">Log Production Batch</h3>
          <p className="text-xs text-slate-500 mb-4">Record raw material input and finished goods.</p>
          <form onSubmit={handleAddBatch} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Product Description</label>
              <input
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Raw Input (kg)</label>
              <input
                type="number"
                value={rawInputKg}
                onChange={(e) => setRawInputKg(e.target.value)}
                className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Finished Goods Output (kg)</label>
              <input
                type="number"
                value={finishedOutputKg}
                onChange={(e) => setFinishedOutputKg(e.target.value)}
                className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Planned Target (kg)</label>
              <input
                type="number"
                value={plannedKg}
                onChange={(e) => setPlannedKg(e.target.value)}
                className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full py-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs rounded-lg transition-colors shadow-xs flex items-center justify-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" />
              Submit Batch Yield Record
            </button>
          </form>
        </div>
      </div>

      {/* Machine Downtime & Telemetry Table */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-slate-900">Processing Line Machinery Telemetry</h3>
          <span className="text-xs text-slate-500">{machines.length} Equipment Monitored</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 uppercase font-semibold text-[10px] border-b border-slate-200">
              <tr>
                <th className="py-2.5 px-3">Equipment</th>
                <th className="py-2.5 px-3">Code</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Run Hours</th>
                <th className="py-2.5 px-3">Downtime</th>
                <th className="py-2.5 px-3">Temperature</th>
                <th className="py-2.5 px-3">Vibration</th>
                <th className="py-2.5 px-3">Downtime Reason</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {machines.map((m) => (
                <tr key={m.id} className="hover:bg-slate-50/50">
                  <td className="py-2.5 px-3 font-semibold text-slate-800">{m.machine_name}</td>
                  <td className="py-2.5 px-3 text-slate-500 font-mono text-[11px]">{m.machine_code}</td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                      {m.status}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-700">{m.operating_hours} hrs</td>
                  <td className="py-2.5 px-3 font-medium text-slate-900">{m.downtime_minutes} min</td>
                  <td className="py-2.5 px-3 text-slate-700">{m.temperature_celsius}°C</td>
                  <td className="py-2.5 px-3 text-slate-700">{m.vibration_mm_s} mm/s</td>
                  <td className="py-2.5 px-3 text-slate-500 italic">{m.downtime_reason || 'Routine operation'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
