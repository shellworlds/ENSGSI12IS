#!/usr/bin/env python3
"""
Hardware-in-the-Loop Simulator - Phase 2
Generates simulated hardware outputs for validation.
"""
import numpy as np
import json
import csv
import os
from datetime import datetime

class HardwareSimulator:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.output_dir = "outputs/"
        os.makedirs(self.output_dir + "hardware_data", exist_ok=True)
        
    def simulate_pilot_system(self, duration_hours=24):
        print(f"Simulating pilot system for {duration_hours} hours...")
        time_points = np.linspace(0, duration_hours, 100)
        
        data = {
            "timestamp": [self._add_hours(self.timestamp, t) for t in time_points],
            "temperature_c": 60 + 5 * np.sin(time_points/6),
            "pressure_bar": 30 + 2 * np.cos(time_points/12),
            "current_a": 100 + 20 * np.sin(time_points/8),
            "voltage_v": 1.8 + 0.2 * np.cos(time_points/10),
            "hydrogen_production_l_h": 10 + 3 * np.sin(time_points/6),
            "membrane_resistance_ohm": 0.1 + 0.02 * (time_points/100),
            "coolant_flow_l_min": 2.0 + 0.5 * np.sin(time_points/12)
        }
        
        self._save_hardware_data(data, time_points)
        return data
    
    def _add_hours(self, timestamp, hours):
        from datetime import datetime, timedelta
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return (dt + timedelta(hours=hours)).isoformat()
    
    def _save_hardware_data(self, data, time_points):
        csv_filename = f"{self.output_dir}hardware_data/pilot_system_{self.timestamp.replace(':', '-')}.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerows(zip(*data.values()))
        
        print(f"Hardware data saved: {csv_filename}")
        
        summary = {
            "simulation_timestamp": self.timestamp,
            "duration_hours": float(time_points[-1]),
            "data_points": len(time_points),
            "sensors_simulated": list(data.keys()),
            "statistics": {
                "avg_temperature": float(np.mean(data['temperature_c'])),
                "avg_pressure": float(np.mean(data['pressure_bar'])),
                "avg_hydrogen_production": float(np.mean(data['hydrogen_production_l_h'])),
                "max_voltage": float(np.max(data['voltage_v'])),
                "min_voltage": float(np.min(data['voltage_v']))
            }
        }
        
        json_filename = csv_filename.replace('.csv', '_summary.json')
        with open(json_filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Summary saved: {json_filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("HARDWARE-IN-THE-LOOP SIMULATION - PHASE 2")
    print("=" * 60)
    
    simulator = HardwareSimulator()
    data = simulator.simulate_pilot_system(duration_hours=24)
    
    print("\n" + "=" * 60)
    print(f"Data points generated: {len(data['timestamp'])}")
    print(f"Time duration: 24 hours")
    print(f"Sensors simulated: {len(data.keys())}")
    print("=" * 60)
