import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { 
  HeartHandshake, Clock, MapPin, Truck, CheckCircle2, 
  AlertTriangle, Filter, Check, X, Calendar, ShieldCheck, RefreshCw
} from 'lucide-react';

export const NgoDashboard = ({ setActiveTab }) => {
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterCategory, setFilterCategory] = useState('');
  const [selectedDonation, setSelectedDonation] = useState(null);

  // Pickup Scheduling Modal State
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [scheduleDonationId, setScheduleDonationId] = useState(null);
  const [vehicleType, setVehicleType] = useState('Refrigerated Van Alpha');
  const [driverName, setDriverName] = useState('Volunteer Team Alpha');
  const [driverPhone, setDriverPhone] = useState('+91 98112 34567');
  const [pickupMinutes, setPickupMinutes] = useState(20);

  const fetchDonations = async () => {
    setLoading(true);
    try {
      const data = await api.getDonations(filterCategory ? { category: filterCategory } : {});
      setDonations(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDonations();
  }, [filterCategory]);

  const handleAcceptDonation = async (donationId) => {
    try {
      await api.acceptDonation(donationId, 1);
      fetchDonations();
      alert("Donation accepted! Next step: Schedule pickup transport.");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const handleScheduleSubmit = async (e) => {
    e.preventDefault();
    try {
      const pickupTime = new Date(Date.now() + pickupMinutes * 60000).toISOString();
      const deliverTime = new Date(Date.now() + (pickupMinutes + 35) * 60000).toISOString();
      await api.schedulePickup({
        donation_id: scheduleDonationId,
        vehicle_type: vehicleType,
        driver_name: driverName,
        driver_phone: driverPhone,
        scheduled_pickup_time: pickupTime,
        estimated_delivery_time: deliverTime
      });
      setShowScheduleModal(false);
      fetchDonations();
      alert("Pickup transport scheduled successfully!");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const handleStatusProgress = async (donationId, currentStatus) => {
    let nextStatus = 'COLLECTED';
    if (currentStatus === 'PICKUP_SCHEDULED') nextStatus = 'COLLECTED';
    else if (currentStatus === 'COLLECTED') nextStatus = 'DELIVERED';
    else if (currentStatus === 'DELIVERED') nextStatus = 'COMPLETED';

    try {
      await api.updateDeliveryStatus(donationId, {
        status: nextStatus,
        receiver_signature_name: "Aahaar Food Bank Distribution Team"
      });
      fetchDonations();
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const availableCount = donations.filter(d => d.status === 'AVAILABLE').length;
  const inProgressCount = donations.filter(d => ['ACCEPTED', 'PICKUP_SCHEDULED', 'COLLECTED'].includes(d.status)).length;
  const completedCount = donations.filter(d => ['DELIVERED', 'COMPLETED'].includes(d.status)).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded bg-purple-100 text-purple-800 border border-purple-200 mb-1">
            <HeartHandshake className="w-3.5 h-3.5 text-purple-600" />
            Module 3 & 4: NGO Redistribution & Delivery
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Aahaar Food Bank Foundation – Dispatch & Intake</h1>
          <p className="text-xs text-slate-500 mt-1">
            Registered DARPAN-DL-2021-00918 • Daily Capacity: 450 meals • Refrigerated Transport: Equipped
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('routing')}
            className="px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors flex items-center gap-1.5 shadow-xs"
          >
            <Truck className="w-3.5 h-3.5" />
            Open Route Optimizer Map
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <StatCard
          title="Available Nearby Donations"
          value={availableCount}
          unit="lots ready"
          icon={HeartHandshake}
          color="emerald"
          change="Freshly listed"
          subtitle="Awaiting NGO claim"
        />
        <StatCard
          title="Active Pickups / In-Transit"
          value={inProgressCount}
          unit="dispatches"
          icon={Truck}
          color="blue"
          change="Cold-chain active"
          subtitle="Live status tracking"
        />
        <StatCard
          title="Meals Distributed"
          value="4,820"
          unit="portions this month"
          icon={CheckCircle2}
          color="purple"
          change="Zero spoilage reported"
          subtitle="Delivered to beneficiaries"
        />
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <span className="font-semibold text-slate-700">Filter Category:</span>
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="px-2.5 py-1.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
          >
            <option value="">All Categories</option>
            <option value="Cooked Meals">Cooked Meals</option>
            <option value="Bakery">Bakery & Breads</option>
            <option value="Fresh Produce">Fresh Produce</option>
            <option value="Packaged Food">Packaged Goods</option>
          </select>
        </div>
        <div className="text-slate-500 text-[11px]">
          Showing {donations.length} total redistribution lots
        </div>
      </div>

      {/* Donations Feed */}
      <div className="grid grid-cols-1 gap-4">
        {donations.map((d) => {
          const isUrgent = new Date(d.safe_use_deadline) - new Date() < 2 * 3600 * 1000;
          return (
            <div
              key={d.id}
              className={`bg-white rounded-xl p-5 border transition-all ${
                d.status === 'AVAILABLE'
                  ? 'border-emerald-200 hover:border-emerald-400 shadow-xs'
                  : 'border-slate-200 bg-slate-50/40'
              }`}
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-mono text-xs font-bold text-slate-500">#{d.donation_code}</span>
                    <h3 className="text-base font-bold text-slate-900">{d.title}</h3>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                      {d.food_category}
                    </span>
                    <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${
                      d.status === 'AVAILABLE' ? 'bg-emerald-50 text-emerald-800 border-emerald-300' :
                      d.status === 'ACCEPTED' ? 'bg-blue-50 text-blue-800 border-blue-300' :
                      d.status === 'PICKUP_SCHEDULED' ? 'bg-amber-50 text-amber-800 border-amber-300' :
                      d.status === 'COLLECTED' ? 'bg-purple-50 text-purple-800 border-purple-300' :
                      'bg-slate-100 text-slate-700 border-slate-300'
                    }`}>
                      {d.status}
                    </span>
                  </div>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600">
                    <div>Portions: <b className="text-slate-900">{d.portions} portions</b> ({d.quantity_kg} kg)</div>
                    <div className="flex items-center gap-1 text-slate-500">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      {d.pickup_address}
                    </div>
                    <div className={`flex items-center gap-1 ${isUrgent ? 'text-rose-600 font-bold' : 'text-slate-600'}`}>
                      <Clock className="w-3.5 h-3.5" />
                      Safe-use deadline: {new Date(d.safe_use_deadline).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>

                  <div className="text-[11px] text-slate-500 bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-100">
                    <b>Storage Spec:</b> {d.storage_condition} • Packaging: {d.packaging_type}
                  </div>
                </div>

                {/* Action Buttons depending on donation workflow status */}
                <div className="flex items-center gap-2 shrink-0">
                  {d.status === 'AVAILABLE' && (
                    <button
                      onClick={() => handleAcceptDonation(d.id)}
                      className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-colors shadow-xs flex items-center gap-1.5"
                    >
                      <Check className="w-3.5 h-3.5" />
                      Accept Donation
                    </button>
                  )}

                  {d.status === 'ACCEPTED' && (
                    <button
                      onClick={() => { setScheduleDonationId(d.id); setShowScheduleModal(true); }}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg transition-colors shadow-xs flex items-center gap-1.5"
                    >
                      <Truck className="w-3.5 h-3.5" />
                      Schedule Transport
                    </button>
                  )}

                  {['PICKUP_SCHEDULED', 'COLLECTED'].includes(d.status) && (
                    <button
                      onClick={() => handleStatusProgress(d.id, d.status)}
                      className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs rounded-lg transition-colors shadow-xs flex items-center gap-1.5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      Mark as {d.status === 'PICKUP_SCHEDULED' ? 'Collected' : 'Delivered'}
                    </button>
                  )}

                  {['DELIVERED', 'COMPLETED'].includes(d.status) && (
                    <div className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 text-xs font-semibold border border-emerald-200 flex items-center gap-1.5">
                      <ShieldCheck className="w-4 h-4 text-emerald-600" />
                      Delivered & Audited
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Pickup Schedule Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200">
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">Schedule Food Collection Transport</h3>
              <button onClick={() => setShowScheduleModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleScheduleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Vehicle Type</label>
                <select
                  value={vehicleType}
                  onChange={(e) => setVehicleType(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200"
                >
                  <option value="Refrigerated Van Alpha">Refrigerated Van Alpha (Cold-chain 4°C)</option>
                  <option value="Electric Cargo Van 02">Electric Cargo Van 02</option>
                  <option value="Volunteer Car Courier">Volunteer Courier Team</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Assigned Driver / Coordinator</label>
                <input
                  type="text"
                  value={driverName}
                  onChange={(e) => setDriverName(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Contact Phone</label>
                <input
                  type="text"
                  value={driverPhone}
                  onChange={(e) => setDriverPhone(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Estimated Departure In</label>
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    value={pickupMinutes}
                    onChange={(e) => setPickupMinutes(Number(e.target.value))}
                    className="w-24 px-3 py-2 rounded-lg border border-slate-200"
                    min="5"
                    max="180"
                  />
                  <span className="text-slate-600">minutes</span>
                </div>
              </div>

              <div className="pt-2 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowScheduleModal(false)}
                  className="px-3.5 py-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold shadow-xs"
                >
                  Confirm Transport Dispatch
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
