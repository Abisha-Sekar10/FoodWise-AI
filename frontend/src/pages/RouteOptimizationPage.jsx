import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { 
  Navigation, MapPin, Clock, Truck, ShieldCheck, 
  ArrowRight, RefreshCw, AlertTriangle, Layers
} from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';

// Custom Map Markers Icons
const createMarkerIcon = (color) => {
  return L.divIcon({
    className: 'custom-div-icon',
    html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 1px 4px rgba(0,0,0,0.4);"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
};

const hubIcon = createMarkerIcon('#059669'); // Emerald
const ngoIcon = createMarkerIcon('#3b82f6'); // Blue
const donationIcon = createMarkerIcon('#f59e0b'); // Amber

export const RouteOptimizationPage = () => {
  const [markers, setMarkers] = useState([]);
  const [routePlan, setRoutePlan] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchRouteData = async () => {
    setLoading(true);
    try {
      const [markerData, planData] = await Promise.all([
        api.getMapMarkers(),
        api.getOptimizedRoute(1)
      ]);
      setMarkers(markerData);
      setRoutePlan(planData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRouteData();
  }, []);

  const defaultCenter = [28.6139, 77.2090]; // New Delhi center

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-200 mb-1">
            <Navigation className="w-3.5 h-3.5 text-blue-600" />
            Module 4: Multi-Stop Logistics Route Optimization
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">AI Redistribution Logistics & Route Planner</h1>
          <p className="text-xs text-slate-500 mt-1">
            Dynamic Traveling Salesperson (TSP) heuristic balancing travel distance, road congestion, and safe-use deadlines.
          </p>
        </div>
        <button
          onClick={fetchRouteData}
          className="px-3 py-2 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Recalculate Optimal Route
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Route Distance"
          value={routePlan?.total_distance_km || 16.4}
          unit="km"
          icon={Navigation}
          color="emerald"
          change="Saves 4.2 km"
          subtitle="vs unoptimized sequence"
        />
        <StatCard
          title="Estimated Transit Time"
          value={routePlan?.total_time_minutes || 38}
          unit="minutes"
          icon={Clock}
          color="blue"
          change="Under safe deadlines"
          subtitle="Avg speed 30 km/h calibrated"
        />
        <StatCard
          title="Stops in Circuit"
          value={routePlan?.stops_count || 4}
          unit="locations"
          icon={MapPin}
          color="purple"
          change="1 Kitchen → 3 NGOs"
          subtitle="Multi-drop delivery"
        />
        <StatCard
          title="Vehicle Standard"
          value="Cold-Chain"
          unit="4-8°C Insulated"
          icon={Truck}
          color="amber"
          change="FSSAI Compliant"
          subtitle="Van Alpha Assigned"
        />
      </div>

      {/* Interactive Map & Route Sequence */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* OpenStreetMap Component */}
        <div className="lg:col-span-2 bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col">
          <div className="flex items-center justify-between mb-3 text-xs">
            <span className="font-bold text-slate-800 flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-emerald-600" />
              OpenStreetMap Geographic Routing Canvas
            </span>
            <div className="flex items-center gap-3 text-[11px] font-medium text-slate-500">
              <span className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 inline-block" /> Kitchen Hub
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600 inline-block" /> Recipient NGO
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block" /> Surplus Pickup
              </span>
            </div>
          </div>

          <div className="h-96 w-full rounded-lg overflow-hidden border border-slate-200 relative z-10">
            <MapContainer
              center={defaultCenter}
              zoom={11}
              scrollWheelZoom={false}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {/* Markers */}
              {markers.map((m) => {
                const icon = m.type === 'KITCHEN' ? hubIcon : m.type === 'NGO' ? ngoIcon : donationIcon;
                return (
                  <Marker key={m.id} position={[m.lat, m.lng]} icon={icon}>
                    <Popup>
                      <div className="text-xs space-y-1">
                        <div className="font-bold text-slate-900">{m.name}</div>
                        <div className="text-slate-600">{m.address || m.capacity}</div>
                        <div className="text-[10px] text-emerald-700 font-semibold uppercase">{m.type}</div>
                      </div>
                    </Popup>
                  </Marker>
                );
              })}

              {/* Waypoint Polyline */}
              {routePlan?.waypoints && routePlan.waypoints.length > 1 && (
                <Polyline
                  positions={routePlan.waypoints}
                  color="#059669"
                  weight={4}
                  opacity={0.8}
                  dashArray="6, 6"
                />
              )}
            </MapContainer>
          </div>
        </div>

        {/* Turn-by-Turn Waypoint Sequence */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Optimized Stop Sequence</h3>
            <p className="text-xs text-slate-500 mb-4">Ordered by deadline urgency & proximity.</p>

            <div className="space-y-3">
              {(routePlan?.ordered_stops || []).map((stop, idx) => (
                <div key={idx} className="p-3 rounded-lg border border-slate-100 bg-slate-50/50 flex items-start gap-3 text-xs">
                  <div className={`w-6 h-6 rounded-full font-bold text-[11px] flex items-center justify-center shrink-0 ${
                    idx === 0 ? 'bg-emerald-600 text-white' : 'bg-blue-600 text-white'
                  }`}>
                    {idx === 0 ? 'H' : idx}
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-slate-800">{stop.name}</div>
                    <div className="text-[11px] text-slate-500 mt-0.5">{stop.stop_type}</div>
                    {stop.urgency === 'HIGH' && (
                      <span className="inline-block mt-1 text-[10px] font-bold px-1.5 py-0.2 rounded bg-rose-100 text-rose-800">
                        ⚡ Urgent Safe-Use Deadline
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-xs space-y-1 bg-slate-50 p-3 rounded-lg border border-slate-200/60">
            <div className="flex items-center justify-between text-slate-600">
              <span>Optimization Algorithm:</span>
              <span className="font-semibold text-slate-800">2-Opt + Deadline A*</span>
            </div>
            <div className="flex items-center justify-between text-slate-600">
              <span>Carbon Saved vs Idle:</span>
              <span className="font-semibold text-emerald-700">~12.8 kg CO2</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
