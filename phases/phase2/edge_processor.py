#!/usr/bin/env python3
"""
Edge Computing Processor - Phase 2
Simulates real-time edge processing for hardware validation.
"""
import json
import csv
from datetime import datetime
import numpy as np

class EdgeProcessor:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.output_dir = "phases/phase2/outputs/"
        
    def process_hardware_data(self, input_data):
        print("Processing hardware data with edge algorithms...")
        
        processed = {
            "timestamp": input_data["timestamp"],
            "temperature_filtered": self._moving_average(input_data["temperature_c"], window=10),
            "pressure_anomalies": self._detect_anomalies(input_data["pressure_bar"], threshold=2.0),
            "current_compressed": self._compress_data(input_data["current_a"], factor=10),
            "efficiency_calculated": self._calculate_efficiency(
                input_data["voltage_v"], input_data["current_a"], input_data["hydrogen_production_l_h"]
            ),
            "predictive_alerts": self._generate_alerts(input_data)
        }
        
        self._save_edge_results(processed, input_data)
        return processed
    
    def _moving_average(self, data, window=10):
        return np.convolve(data, np.ones(window)/window, mode='same').tolist()
    
    def _detect_anomalies(self, data, threshold=2.0):
        mean = np.mean(data)
        std = np.std(data)
        return [1 if abs(x - mean) > threshold * std else 0 for x in data]
    
    def _compress_data(self, data, factor=10):
        return data[::factor].tolist()
    
    def _calculate_efficiency(self, voltage, current, hydrogen):
        power = np.array(voltage) * np.array(current)
        efficiency = np.array(hydrogen) / (power + 1e-6) * 100
        return efficiency.tolist()
    
    def _generate_alerts(self, data):
        alerts = []
        for i in range(len(data["timestamp"])):
            alert = 0
            if data["temperature_c"][i] > 70:
                alert = 1
            elif data["pressure_bar"][i] > 35:
                alert = 2
            elif data["membrane_resistance_ohm"][i] > 0.15:
                alert = 3
            alerts.append(alert)
        return alerts
    
    def _save_edge_results(self, processed, original):
        report = {
            "processing_timestamp": self.timestamp,
            "algorithms_applied": [
                "moving_average_filter",
                "anomaly_detection",
                "data_compression",
                "efficiency_calculation",
                "predictive_alert_generation"
            ],
            "performance_metrics": {
                "data_reduction_ratio": len(processed["current_compressed"]) / len(original["current_a"]),
                "anomalies_detected": sum(processed["pressure_anomalies"]),
                "alerts_generated": len([a for a in processed["predictive_alerts"] if a > 0]),
                "avg_efficiency": float(np.mean(processed["efficiency_calculated"]))
            }
        }
        
        json_filename = f"{self.output_dir}edge_logs/edge_processing_{self.timestamp.replace(':', '-')}.json"
        with open(json_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        csv_filename = f"{self.output_dir}edge_logs/alerts_{self.timestamp.replace(':', '-')}.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "alert_type", "alert_description"])
            for i, alert in enumerate(processed["predictive_alerts"]):
                if alert > 0:
                    desc = ["", "Over-temperature", "Over-pressure", "Membrane degradation"][alert]
                    writer.writerow([original["timestamp"][i], alert, desc])
        
        print(f"Edge processing report: {json_filename}")
        print(f"Alert summary: {csv_filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("EDGE COMPUTING PROCESSOR - PHASE 2")
    print("=" * 60)
    
    from hardware_simulator import HardwareSimulator
    hardware = HardwareSimulator()
    hardware_data = hardware.simulate_pilot_system(duration_hours=24)
    
    processor = EdgeProcessor()
    processed_data = processor.process_hardware_data(hardware_data)
    
    print("\n" + "=" * 60)
    print(f"Original data points: {len(hardware_data['timestamp'])}")
    print(f"Compressed data points: {len(processed_data['current_compressed'])}")
    print(f"Data reduction: {(1 - len(processed_data['current_compressed'])/len(hardware_data['timestamp']))*100:.1f}%")
    print(f"Alerts generated: {sum(1 for a in processed_data['predictive_alerts'] if a > 0)}")
    print("=" * 60)
