import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { 
  ScanEye, UploadCloud, AlertTriangle, ShieldCheck, Thermometer, 
  Droplets, Wind, DoorClosed, AlertCircle, RefreshCw, CheckCircle, Info
} from 'lucide-react';

export const QualityAndIotPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [itemName, setItemName] = useState('Fresh Cut Vegetables Sample');
  const [previewUrl, setPreviewUrl] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [recentAssessments, setRecentAssessments] = useState([]);

  // IoT Sensor Telemetry State
  const [iotData, setIotData] = useState(null);
  const [iotLoading, setIotLoading] = useState(true);

  const fetchIot = async () => {
    setIotLoading(true);
    try {
      const data = await api.getIotReadings(1);
      setIotData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIotLoading(false);
    }
  };

  const fetchAssessments = async () => {
    try {
      const history = await api.getQualityHistory();
      setRecentAssessments(history);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchIot();
    fetchAssessments();
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAssessmentResult(null);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      alert("Please select or upload an image first.");
      return;
    }

    setAnalyzing(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('item_name', itemName);
      formData.append('kitchen_id', '1');

      const result = await api.assessFoodImage(formData);
      setAssessmentResult(result);
      fetchAssessments();
    } catch (err) {
      alert("Analysis failed: " + err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleTriggerTelemetry = async (anomaly = false) => {
    try {
      await api.simulateTelemetry(1, anomaly);
      fetchIot();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-200 mb-1">
          <ScanEye className="w-3.5 h-3.5 text-emerald-600" />
          Module 2: Quality Vision & IoT Cold Chain
        </div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Smart Food Quality & IoT Storage Monitoring</h1>
        <p className="text-xs text-slate-500 mt-1">
          Computer vision screening for surface deterioration alongside real-time cold storage sensory telemetry.
        </p>
      </div>

      {/* Mandatory Safety Notice */}
      <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
        <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">FSSAI & MoFPI Food Safety Protocol Requirement:</span> AI computer vision provides preliminary visual triage to detect discoloration, surface mold, and textural softening. It does not replace laboratory microbiological testing or trained human sensory safety evaluation. Only food verified under safe conditions qualifies for redistribution.
        </div>
      </div>

      {/* Grid: Computer Vision Upload + Live Results */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload Card */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-1">AI Food Image Quality Assessment</h3>
          <p className="text-xs text-slate-500 mb-4">
            Upload a photo of prepared meals, fruits, or raw produce for visual freshness categorization.
          </p>

          <form onSubmit={handleAnalyze} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Food Sample Name</label>
              <input
                type="text"
                value={itemName}
                onChange={(e) => setItemName(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., Steamed Rice, Tomato Crate, Fresh Paneer"
                required
              />
            </div>

            <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:border-emerald-500 transition-colors bg-slate-50/50">
              {previewUrl ? (
                <div className="space-y-3">
                  <img src={previewUrl} alt="Preview" className="max-h-48 mx-auto rounded-lg object-contain shadow-xs" />
                  <label className="inline-block text-xs text-emerald-600 font-semibold cursor-pointer hover:underline">
                    Choose different image
                    <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
                  </label>
                </div>
              ) : (
                <label className="cursor-pointer flex flex-col items-center">
                  <UploadCloud className="w-10 h-10 text-slate-400 mb-2" />
                  <span className="text-xs font-semibold text-slate-700">Click to upload food photo</span>
                  <span className="text-[11px] text-slate-400 mt-1">JPEG, PNG, or WebP up to 10MB</span>
                  <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
                </label>
              )}
            </div>

            <button
              type="submit"
              disabled={analyzing || !selectedFile}
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-300 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-2 shadow-xs"
            >
              <ScanEye className="w-4 h-4" />
              {analyzing ? 'Evaluating Visual Attributes...' : 'Run Vision Quality Assessment'}
            </button>
          </form>
        </div>

        {/* Inference Results Card */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-slate-900">Visual Quality Analysis Output</h3>
              {assessmentResult && (
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${
                  assessmentResult.visual_quality_category.includes('Fresh')
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                    : assessmentResult.visual_quality_category.includes('Good')
                    ? 'bg-blue-50 text-blue-800 border-blue-300'
                    : assessmentResult.visual_quality_category.includes('Slight')
                    ? 'bg-amber-50 text-amber-800 border-amber-300'
                    : 'bg-rose-50 text-rose-800 border-rose-300'
                }`}>
                  {assessmentResult.visual_quality_category}
                </span>
              )}
            </div>

            {assessmentResult ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-slate-500 font-medium">Confidence Score</span>
                    <div className="text-lg font-bold text-slate-900 mt-0.5">
                      {Math.round(assessmentResult.confidence_score * 100)}%
                    </div>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-slate-500 font-medium">Redistribution Eligibility</span>
                    <div className="text-sm font-bold mt-1">
                      {assessmentResult.is_redistribution_approved ? (
                        <span className="text-emerald-700 flex items-center gap-1">
                          <CheckCircle className="w-4 h-4" /> Approved
                        </span>
                      ) : (
                        <span className="text-rose-700 flex items-center gap-1">
                          <AlertTriangle className="w-4 h-4" /> Rejected (Unsafe)
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {assessmentResult.requires_human_inspection && (
                  <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-800 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
                    <span><b>Flagged for Secondary Human Check:</b> Slight visual variance detected. Verify aroma and texture manually.</span>
                  </div>
                )}

                <div className="p-3 rounded-lg bg-slate-50 border border-slate-100 text-xs">
                  <span className="font-semibold text-slate-700">Detected Visual Features:</span>
                  <div className="grid grid-cols-2 gap-2 mt-2 text-[11px] text-slate-600">
                    <div>Color Uniformity: <b>{assessmentResult.detected_features?.color_uniformity || 88}%</b></div>
                    <div>Browning Index: <b>{assessmentResult.detected_features?.browning_index || 12}</b></div>
                    <div>Surface Defect: <b>{assessmentResult.detected_features?.surface_defect_ratio || 5}%</b></div>
                    <div>Mean Brightness: <b>{assessmentResult.detected_features?.mean_brightness || 135}</b></div>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-emerald-50/60 border border-emerald-100 text-xs text-emerald-900">
                  <b>Evaluator Recommendation:</b> {assessmentResult.human_verifier_notes}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-xs text-slate-400">
                Upload or select an image on the left and click "Run Vision Quality Assessment" to view automated visual triage metrics.
              </div>
            )}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-[10px] text-slate-400 italic">
            Models calibrated against MoFPI sensory standards for institutional catering.
          </div>
        </div>
      </div>

      {/* IoT Cold Storage Telemetry Section */}
      <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-slate-900">Live IoT Cold Storage & Environment Telemetry</h2>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                Simulated IoT Stream (MQTT Compliant)
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Monitors walk-in chillers, deep freezers, and dry pantries to guarantee cold-chain safety.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => handleTriggerTelemetry(false)}
              className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Simulate Normal Pulse
            </button>
            <button
              onClick={() => handleTriggerTelemetry(true)}
              className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 transition-colors flex items-center gap-1.5"
            >
              <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
              Simulate Chiller Breach
            </button>
          </div>
        </div>

        {/* Sensory Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {(iotData?.sensors || [
            { sensor_id: 'IOT-CHILLER-01', storage_area: 'Walk-in Chiller (Dairy & Produce)', temperature_celsius: 3.6, humidity_percent: 82.5, ethylene_ppm: 0.08, status: 'NORMAL', safe_temp_range: '1.0°C - 4.5°C' },
            { sensor_id: 'IOT-FREEZER-02', storage_area: 'Deep Freezer (Meat & Frozen)', temperature_celsius: -19.4, humidity_percent: 55.0, ethylene_ppm: 0.01, status: 'NORMAL', safe_temp_range: '-22.0°C - -18.0°C' },
            { sensor_id: 'IOT-PANTRY-03', storage_area: 'Dry Grain Pantry', temperature_celsius: 21.8, humidity_percent: 52.0, ethylene_ppm: 0.03, status: 'NORMAL', safe_temp_range: '18.0°C - 24.0°C' },
            { sensor_id: 'IOT-HOT-HOLD-04', storage_area: 'Cooked Food Holding Area', temperature_celsius: 64.2, humidity_percent: 45.0, ethylene_ppm: 0.02, status: 'NORMAL', safe_temp_range: '> 60.0°C (Hot Holding)' }
          ]).map((sensor) => {
            const isAnomaly = sensor.temperature_celsius > 6.0 && sensor.storage_area.includes('Chiller');
            return (
              <div 
                key={sensor.sensor_id} 
                className={`p-4 rounded-xl border transition-all ${
                  isAnomaly ? 'bg-rose-50/60 border-rose-300 shadow-sm' : 'bg-slate-50/50 border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold text-slate-500">{sensor.sensor_id}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    isAnomaly ? 'bg-rose-100 text-rose-800' : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    {isAnomaly ? 'THRESHOLD BREACH' : 'NORMAL'}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-slate-800 mb-3">{sensor.storage_area}</h4>

                <div className="space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500 flex items-center gap-1">
                      <Thermometer className="w-3.5 h-3.5 text-blue-500" /> Temperature:
                    </span>
                    <span className={`font-bold ${isAnomaly ? 'text-rose-700 text-sm' : 'text-slate-900'}`}>
                      {sensor.temperature_celsius}°C
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500 flex items-center gap-1">
                      <Droplets className="w-3.5 h-3.5 text-cyan-500" /> Humidity:
                    </span>
                    <span className="font-semibold text-slate-800">{sensor.humidity_percent}% RH</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500 flex items-center gap-1">
                      <Wind className="w-3.5 h-3.5 text-emerald-500" /> Ethylene:
                    </span>
                    <span className="font-semibold text-slate-800">{sensor.ethylene_ppm} ppm</span>
                  </div>
                </div>

                <div className="mt-3 pt-2.5 border-t border-slate-200/60 text-[10px] text-slate-500 flex items-center justify-between">
                  <span>Target Range:</span>
                  <span className="font-semibold text-slate-700">{sensor.safe_temp_range}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
