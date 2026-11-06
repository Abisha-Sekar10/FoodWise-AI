"""
FoodWise AI - Demand Prediction Training Script
Problem Statement 26234 (Ministry of Food Processing Industries)
Trains a Random Forest Regressor on institutional kitchen attendance,
seasonal factors, day-of-week, temperature, and consumption records.
"""

import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.ml.demand_forecasting import demand_forecaster

def main():
    print("=" * 60)
    print("FoodWise AI - Random Forest Demand Model Training")
    print("=" * 60)
    print("Generating 730 days of synthetic dining consumption records...")
    metrics = demand_forecaster.train()
    print("\nTraining Completed Successfully!")
    print(f"R² Score:            {metrics['r2_score']}")
    print(f"MAE (Portions):       {metrics['mae_portions']}")
    print(f"RMSE (Portions):      {metrics['rmse_portions']}")
    print(f"Samples Trained:      {metrics['trained_samples']}")
    print(f"Features:             {', '.join(metrics['features'])}")
    print("=" * 60)

if __name__ == "__main__":
    main()
