const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('foodwise_token');
  const headers = {
    ...options.headers,
  };

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorDetail;
    } catch {
      errorDetail = response.statusText;
    }
    throw new Error(errorDetail);
  }

  // Handle binary streams like CSV/PDF
  const contentType = response.headers.get('content-type');
  if (contentType && (contentType.includes('application/pdf') || contentType.includes('text/csv'))) {
    return response.blob();
  }

  return response.json();
}

export const api = {
  // Auth
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  getMe: () => request('/auth/me'),
  getDemoUsers: () => request('/auth/demo-users'),

  // Admin
  getAdminSummary: () => request('/admin/dashboard-summary'),
  getInstitutions: () => request('/admin/institutions'),
  getNgos: () => request('/admin/ngos'),
  getUsers: () => request('/admin/users'),

  // Kitchen
  getKitchenSummary: (id = 1) => request(`/kitchen/summary/${id}`),
  predictDemand: (data) => request('/kitchen/predict-demand', { method: 'POST', body: JSON.stringify(data) }),
  getInventory: (kitchenId = 1) => request(`/kitchen/inventory/${kitchenId}`),
  addInventoryItem: (data) => request('/kitchen/inventory', { method: 'POST', body: JSON.stringify(data) }),
  getProduction: (kitchenId = 1) => request(`/kitchen/production/${kitchenId}`),
  recordProduction: (data) => request('/kitchen/production', { method: 'POST', body: JSON.stringify(data) }),
  getConsumption: (kitchenId = 1) => request(`/kitchen/consumption/${kitchenId}`),
  recordConsumption: (data) => request('/kitchen/consumption', { method: 'POST', body: JSON.stringify(data) }),
  getSurplus: (kitchenId = 1) => request(`/kitchen/surplus/${kitchenId}`),
  listSurplusForDonation: (surplusId) => request(`/kitchen/surplus/list-donation/${surplusId}`, { method: 'POST' }),

  // Quality & IoT
  assessFoodImage: (formData) => request('/quality/assess-image', { method: 'POST', body: formData }),
  getQualityHistory: (kitchenId) => request(`/quality/history${kitchenId ? `?kitchen_id=${kitchenId}` : ''}`),
  getIotReadings: (kitchenId = 1) => request(`/iot/live-readings/${kitchenId}`),
  simulateTelemetry: (kitchenId = 1, triggerAnomaly = false) => request(`/iot/simulate-telemetry/${kitchenId}?trigger_anomaly=${triggerAnomaly}`, { method: 'POST' }),

  // Redistribution
  getDonations: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/redistribution/donations${q ? `?${q}` : ''}`);
  },
  getMatchingNgos: (donationId) => request(`/redistribution/matching-ngos/${donationId}`),
  acceptDonation: (donationId, ngoId) => request(`/redistribution/accept/${donationId}?ngo_id=${ngoId}`, { method: 'POST' }),
  schedulePickup: (data) => request('/redistribution/schedule-pickup', { method: 'POST', body: JSON.stringify(data) }),
  updateDeliveryStatus: (donationId, data) => request(`/redistribution/update-status/${donationId}`, { method: 'POST', body: JSON.stringify(data) }),

  // Routing
  getMapMarkers: () => request('/routing/map-markers'),
  getOptimizedRoute: (kitchenId = 1) => request(`/routing/optimize?kitchen_id=${kitchenId}`),

  // Processing Unit
  getProcessingSummary: (unitId = 1) => request(`/processing/summary/${unitId}`),
  getProductionRecords: (unitId = 1) => request(`/processing/production-records/${unitId}`),
  addProductionRecord: (data) => request('/processing/production-records', { method: 'POST', body: JSON.stringify(data) }),
  getMachines: (unitId = 1) => request(`/processing/machines/${unitId}`),
  addMachineLog: (data) => request('/processing/machines', { method: 'POST', body: JSON.stringify(data) }),
  getEnergyRecords: (unitId = 1) => request(`/processing/energy/${unitId}`),
  addEnergyRecord: (data) => request('/processing/energy', { method: 'POST', body: JSON.stringify(data) }),

  // Sustainability & Analytics
  getSustainabilitySummary: () => request('/analytics/sustainability-summary'),
  getSmartProductionPlan: (kitchenId = 1) => request(`/analytics/smart-production-plan/${kitchenId}`),
  getWasteAnomalies: (kitchenId = 1) => request(`/analytics/waste-anomalies?kitchen_id=${kitchenId}`),
  exportCsvUrl: `${BASE_URL}/analytics/export/csv`,
  exportPdfUrl: `${BASE_URL}/analytics/export/pdf`,
};
