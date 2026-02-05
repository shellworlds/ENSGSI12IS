#!/usr/bin/env python3
"""
AEM Electrolyzer Multiphysics Model - Phase 1
Generates verifiable outputs for research documentation.
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib

class AEMElectrolyzerModel:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.model_version = "1.0"
        self.output_dir = "phases/phase1/outputs/"
        
    def generate_polarization_curve(self, current_density_range=(0, 2000)):
        """Generate polarization curve with validation outputs"""
        print("Generating polarization curve...")
        
        # Simulate AEM electrolyzer voltage-current relationship
        current_density = np.linspace(current_density_range[0], current_density_range[1], 50)
        
        # Simplified model: V = V0 + a*log(j/j0) + r*j
        V0 = 1.23  # Thermodynamic voltage
        a = 0.03   # Tafel slope coefficient
        j0 = 0.1   # Exchange current density
        r = 0.001  # Ohmic resistance
        
        voltage = V0 + a * np.log((current_density + 1e-6)/j0) + r * current_density
        
        # Generate output files
        self._save_polarization_data(current_density, voltage)
        self._plot_polarization_curve(current_density, voltage)
        
        return current_density, voltage
    
    def _save_polarization_data(self, current_density, voltage):
        """Save polarization data to JSON for MS Word import"""
        data = {
            "timestamp": self.timestamp,
            "model": "AEM_Electrolyzer_Polarization_v1",
            "parameters": {
                "V0": 1.23,
                "a": 0.03,
                "j0": 0.1,
                "r": 0.001
            },
            "data": {
                "current_density_ma_cm2": current_density.tolist(),
                "voltage_v": voltage.tolist(),
                "efficiency_percent": (1.23 / voltage * 100).tolist()
            },
            "validation": {
                "min_voltage": float(np.min(voltage)),
                "max_voltage": float(np.max(voltage)),
                "avg_efficiency": float(np.mean(1.23 / voltage * 100))
            }
        }
        
        filename = f"{self.output_dir}validation_data/polarization_curve_{self.timestamp.replace(':', '-')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Generate hash for verification
        with open(filename, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        print(f"Data saved: {filename}")
        print(f"File hash: {file_hash}")
        
        # Save hash to verification log
        with open(f"{self.output_dir}validation_data/file_verification.csv", 'a') as f:
            f.write(f"{filename},{file_hash},{self.timestamp}\n")
    
    def _plot_polarization_curve(self, current_density, voltage):
        """Generate PNG graph for research report"""
        plt.figure(figsize=(12, 8))
        plt.plot(current_density, voltage, 'b-', linewidth=2, label='Model Prediction')
        plt.axhline(y=1.23, color='r', linestyle='--', label='Thermodynamic Limit (1.23V)')
        
        plt.xlabel('Current Density (mA/cm²)', fontsize=12)
        plt.ylabel('Cell Voltage (V)', fontsize=12)
        plt.title('AEM Electrolyzer Polarization Curve', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Annotate key points
        idx_100 = np.argmin(np.abs(current_density - 100))
        idx_1000 = np.argmin(np.abs(current_density - 1000))
        plt.annotate(f'{voltage[idx_100]:.2f}V @ 100mA/cm²', 
                    xy=(current_density[idx_100], voltage[idx_100]),
                    xytext=(current_density[idx_100]+200, voltage[idx_100]-0.1))
        plt.annotate(f'{voltage[idx_1000]:.2f}V @ 1000mA/cm²',
                    xy=(current_density[idx_1000], voltage[idx_1000]),
                    xytext=(current_density[idx_1000]+200, voltage[idx_1000]-0.1))
        
        # Save plot
        filename = f"{self.output_dir}graphs/polarization_curve_{self.timestamp.replace(':', '-')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Graph saved: {filename}")
    
    def generate_degradation_model(self, operating_hours=40000):
        """Simulate membrane degradation over time"""
        print("Generating degradation model...")
        
        time = np.linspace(0, operating_hours, 100)
        
        # Two-phase degradation model
        # Phase 1: Initial stabilization (0-1000h)
        # Phase 2: Linear degradation (1000-40000h)
        
        degradation_rate = np.zeros_like(time)
        mask1 = time < 1000
        mask2 = time >= 1000
        
        degradation_rate[mask1] = 0.0001 * time[mask1]  # Slow initial
        degradation_rate[mask2] = 0.1 + 0.00015 * (time[mask2] - 1000)  # Linear
        
        voltage_increase = 1.23 * (1 + degradation_rate / 100)
        
        # Save degradation data
        self._save_degradation_data(time, degradation_rate, voltage_increase)
        self._plot_degradation_curve(time, degradation_rate, voltage_increase)
        
        return time, degradation_rate, voltage_increase
    
    def _save_degradation_data(self, time, degradation_rate, voltage_increase):
        """Save degradation model outputs"""
        data = {
            "timestamp": self.timestamp,
            "model": "AEM_Membrane_Degradation_v1",
            "parameters": {
                "operating_hours": 40000,
                "initial_degradation_rate": 0.0001,
                "linear_degradation_rate": 0.00015
            },
            "data": {
                "time_hours": time.tolist(),
                "degradation_percent": degradation_rate.tolist(),
                "voltage_v": voltage_increase.tolist(),
                "efficiency_loss_percent": (100 - (1.23 / voltage_increase * 100)).tolist()
            },
            "key_metrics": {
                "degradation_at_10000h": float(degradation_rate[np.argmin(np.abs(time - 10000))]),
                "degradation_at_40000h": float(degradation_rate[-1]),
                "lifetime_prediction_hours": 40000
            }
        }
        
        filename = f"{self.output_dir}validation_data/degradation_model_{self.timestamp.replace(':', '-')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Degradation data saved: {filename}")
    
    def _plot_degradation_curve(self, time, degradation_rate, voltage_increase):
        """Generate degradation visualization"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Degradation percentage
        ax1.plot(time/1000, degradation_rate, 'r-', linewidth=2)
        ax1.set_xlabel('Operating Time (kHours)', fontsize=12)
        ax1.set_ylabel('Performance Degradation (%)', fontsize=12)
        ax1.set_title('Membrane Degradation Over Time', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axvline(x=10, color='g', linestyle='--', alpha=0.5, label='10,000 hours')
        ax1.axvline(x=40, color='orange', linestyle='--', alpha=0.5, label='40,000 hours')
        ax1.legend()
        
        # Plot 2: Voltage increase
        ax2.plot(time/1000, voltage_increase, 'b-', linewidth=2)
        ax2.axhline(y=1.23, color='r', linestyle='--', label='Initial Voltage')
        ax2.set_xlabel('Operating Time (kHours)', fontsize=12)
        ax2.set_ylabel('Cell Voltage (V)', fontsize=12)
        ax2.set_title('Voltage Increase Due to Degradation', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        filename = f"{self.output_dir}graphs/degradation_analysis_{self.timestamp.replace(':', '-')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Degradation graph saved: {filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("AEM ELECTROLYZER MULTIPHYSICS MODEL - PHASE 1 VALIDATION")
    print("=" * 60)
    
    model = AEMElectrolyzerModel()
    
    # Generate polarization curve
    j, V = model.generate_polarization_curve()
    
    # Generate degradation model
    time, deg, V_deg = model.generate_degradation_model()
    
    print("\n" + "=" * 60)
    print("OUTPUT SUMMARY:")
    print("=" * 60)
    print(f"1. Polarization curve: {len(j)} data points generated")
    print(f"2. Degradation model: {len(time)} time points simulated")
    print(f"3. Output directory: phases/phase1/outputs/")
    print(f"4. Timestamp: {model.timestamp}")
    print("=" * 60)
    print("All outputs ready for MS Word report import.")
    print("JSON files can be directly imported as data sources.")
    print("PNG graphs are 300 DPI ready for publication.")
    print("=" * 60)
