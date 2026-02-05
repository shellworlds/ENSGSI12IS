#!/usr/bin/env python3
"""
Pilot Production Simulator - Phase 3
Simulates 10 MW/year production line with quality control.
"""
import numpy as np
import json
import os
from datetime import datetime, timedelta

class ProductionSimulator:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.output_dir = "outputs/"
        os.makedirs(self.output_dir + "production_data", exist_ok=True)
        self.production_rate = 10  # MW/year
        
    def simulate_production_day(self, days=30):
        print(f"Simulating {days} days of pilot production...")
        
        production_data = []
        for day in range(days):
            daily_data = {
                "date": (datetime.now() + timedelta(days=day)).isoformat(),
                "units_produced": np.random.randint(90, 110),
                "defect_rate": np.random.uniform(0.01, 0.05),
                "energy_consumption_mwh": np.random.uniform(8, 12),
                "hydrogen_output_kg": np.random.uniform(180, 220),
                "quality_score": np.random.uniform(0.85, 0.98),
                "downtime_minutes": np.random.randint(0, 60)
            }
            production_data.append(daily_data)
        
        self._save_production_data(production_data)
        return production_data
    
    def _save_production_data(self, data):
        json_filename = f"{self.output_dir}production_data/production_{self.timestamp.replace(':', '-')}.json"
        with open(json_filename, 'w') as f:
            json.dump({
                "timestamp": self.timestamp,
                "production_rate_mw_year": self.production_rate,
                "simulation_days": len(data),
                "total_units": sum(d['units_produced'] for d in data),
                "avg_defect_rate": np.mean([d['defect_rate'] for d in data]),
                "avg_hydrogen_output": np.mean([d['hydrogen_output_kg'] for d in data]),
                "daily_data": data[:5]  # First 5 days for preview
            }, f, indent=2)
        
        print(f"Production data saved: {json_filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("PILOT PRODUCTION SIMULATOR - PHASE 3")
    print("=" * 60)
    
    simulator = ProductionSimulator()
    data = simulator.simulate_production_day(days=30)
    
    print(f"\nSimulated {len(data)} days of production")
    print(f"Total units: {sum(d['units_produced'] for d in data)}")
    print(f"Average defect rate: {np.mean([d['defect_rate'] for d in data]):.2%}")
    print(f"Average hydrogen output: {np.mean([d['hydrogen_output_kg'] for d in data]):.1f} kg/day")
    print("=" * 60)
