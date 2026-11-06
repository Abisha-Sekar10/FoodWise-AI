import numpy as np
from sklearn.ensemble import IsolationForest

class WasteAnomalyDetector:
    def __init__(self):
        self.iso_forest = IsolationForest(contamination=0.10, random_state=42)

    def detect_kitchen_waste_anomalies(self, consumption_history):
        """
        Detects abnormal waste spikes in kitchen consumption logs.
        consumption_history: list of dicts with plate_waste_kg, service_waste_kg, actual_diners.
        """
        if not consumption_history or len(consumption_history) < 3:
            return []

        # Features: plate_waste_per_diner, service_waste_per_diner, total_waste
        features = []
        for r in consumption_history:
            diners = max(1, r.get("actual_diners", 100))
            pw = r.get("plate_waste_kg", 0.0)
            sw = r.get("service_waste_kg", 0.0)
            total = pw + sw
            features.append([pw / diners, sw / diners, total])

        X = np.array(features)
        
        # Fit or evaluate
        try:
            predictions = self.iso_forest.fit_predict(X)
            scores = self.iso_forest.decision_function(X)
        except Exception:
            # Fallback to standard z-score
            means = np.mean(X, axis=0)
            stds = np.std(X, axis=0) + 1e-5
            z_scores = np.abs((X - means) / stds)
            predictions = np.where(np.max(z_scores, axis=1) > 2.0, -1, 1)
            scores = -np.max(z_scores, axis=1)

        anomalies = []
        for idx, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Outlier detected
                rec = consumption_history[idx]
                diners = max(1, rec.get("actual_diners", 100))
                pw = rec.get("plate_waste_kg", 0.0)
                sw = rec.get("service_waste_kg", 0.0)
                
                cause = "Excessive buffet service waste" if sw > pw else "High diner plate wastage"
                action = (
                    "Service portions exceed consumption norms. Transition to batch replenishment every 30 minutes."
                    if sw > pw else
                    "High plate scrapings detected. Consider reducing individual portion sizes by 15% and providing second helpings on request."
                )

                anomalies.append({
                    "date": rec.get("date"),
                    "meal_type": rec.get("meal_type", "Lunch"),
                    "total_waste_kg": round(pw + sw, 2),
                    "diners": diners,
                    "anomaly_score": round(float(abs(score)), 2),
                    "primary_cause": cause,
                    "actionable_recommendation": action
                })

        return anomalies

    def detect_processing_anomalies(self, records, machine_logs, energy_logs):
        """
        Detects industrial inefficiencies in food processing units:
        - Excessive raw material loss (> 8-12%)
        - Abnormal specific energy (kWh / kg)
        - High downtime vs operating hours
        """
        anomalies = []

        # 1. Material Loss Check
        for r in records:
            eff = r.get("production_efficiency_pct", 90.0)
            loss_kg = r.get("material_loss_kg", 0.0)
            batch = r.get("batch_number", "BATCH-XXX")
            if eff < 82.0:
                anomalies.append({
                    "type": "MATERIAL_LOSS",
                    "severity": "HIGH",
                    "title": f"Material Loss Spike in Batch {batch}",
                    "metric": f"Efficiency {eff}% (Loss: {loss_kg} kg)",
                    "message": f"Yield dropped {round(100 - eff, 1)}% below normal. Check machine calibration, cutting blade sharpness, and extrusion nozzle clearance.",
                    "recommendation": "Perform recalibration before next production cycle."
                })

        # 2. Machine Downtime Check
        for m in machine_logs:
            dt = m.get("downtime_minutes", 0)
            code = m.get("machine_code", "M-01")
            temp = m.get("temperature_celsius", 75.0)
            vibe = m.get("vibration_mm_s", 1.0)
            if dt > 60 or temp > 90.0 or vibe > 3.0:
                anomalies.append({
                    "type": "MACHINE_INEFFICIENCY",
                    "severity": "CRITICAL" if temp > 90 or vibe > 3.0 else "MEDIUM",
                    "title": f"Equipment Warning: {code}",
                    "metric": f"Temp: {temp}°C | Vibration: {vibe} mm/s | Downtime: {dt} min",
                    "message": f"Machine {code} shows irregular thermodynamic/mechanical stress. Elevated risk of unpredicted breakdown.",
                    "recommendation": "Schedule preventive bearing lubrication and thermal cooling inspection."
                })

        # 3. Specific Energy Check
        for e in energy_logs:
            sec = e.get("specific_energy_kwh_per_kg", 0.25)
            shift = e.get("shift", "Shift 1")
            if sec > 0.45 or e.get("is_abnormal_consumption"):
                anomalies.append({
                    "type": "ENERGY_INEFFICIENCY",
                    "severity": "MEDIUM",
                    "title": f"Energy Spike on {shift}",
                    "metric": f"{sec} kWh/kg",
                    "message": f"Energy intensity is 38% above baseline standard (0.28 kWh/kg). Heating boilers or refrigeration chillers may be running idling cycles.",
                    "recommendation": "Implement variable frequency drive (VFD) controls and audit boiler insulation."
                })

        return anomalies

anomaly_detector = WasteAnomalyDetector()
