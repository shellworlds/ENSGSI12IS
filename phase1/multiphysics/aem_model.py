#!/usr/bin/env python3
"""
AEM Electrolyzer Multiphysics Model
Generates validation graphs and simulation data for research documentation
"""
import numpy as np
import matplotlib.pyplot as plt
import json
import datetime

class AEMElectrolyzerModel:
    def __init__(self):
        self.timestamp = datetime.datetime.now().isoformat()
        self.results = {}
        
    def polarization_curve(self, current_density):
        """Calculate voltage vs current density"""
        # Tafel equation: V = V_rev + a + b*log(j) + r*j
        V_rev = 1.23  # Reversible potential at 25°C
        a_anode = 0.3  # Anode overpotential coefficient
        b_anode = 0.05  # Tafel slope
        r = 0.2  # Ohmic resistance (Ohm.cm²)
        
        # Avoid log(0)
        j = np.maximum(current_density, 1e-10)
        
        V_cell = V_rev + a_anode + b_anode * np.log10(j) + r * j
        
        self.results['polarization_data'] = {
            'current_density': current_density.tolist(),
            'cell_voltage': V_cell.tolist(),
            'efficiency': (1.23 / V_cell * 100).tolist()
        }
        
        return V_cell
    
    def degradation_model(self, time_hours, temperature=60, current_density=1.0):
        """Model membrane degradation over time"""
        # Arrhenius-type degradation model
        E_a = 65000  # Activation energy J/mol
        R = 8.314    # Gas constant
        T = temperature + 273.15  # Convert to Kelvin
        
        k0 = 1e-5  # Base degradation rate
        k = k0 * np.exp(-E_a/(R*T)) * (current_density ** 0.5)
        
        degradation = 1 - np.exp(-k * time_hours)
        
        self.results['degradation_data'] = {
            'time_hours': time_hours.tolist(),
            'degradation_percent': (degradation * 100).tolist(),
            'temperature_C': temperature,
            'current_density': current_density
        }
        
        return degradation
    
    def thermal_model(self, current_density, ambient_temp=25):
        """Calculate temperature rise in stack"""
        # Heat generation: Q = I*V - Power_output
        V_cell = self.polarization_curve(current_density)
        power_in = V_cell * current_density
        power_out = 1.23 * current_density  # Ideal H2 production power
        
        heat_gen = power_in - power_out  # W/cm²
        
        # Simplified thermal model
        R_th = 0.1  # Thermal resistance K.cm²/W
        delta_T = heat_gen * R_th
        
        stack_temp = ambient_temp + delta_T
        
        self.results['thermal_data'] = {
            'current_density': current_density.tolist(),
            'stack_temperature': stack_temp.tolist(),
            'heat_generation': heat_gen.tolist()
        }
        
        return stack_temp
    
    def generate_graphs(self):
        """Generate publication-ready graphs"""
        plt.style.use('seaborn-v0_8-paper')
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Polarization curve
        j = np.linspace(0.1, 3, 50)
        V = self.polarization_curve(j)
        ax1 = axes[0, 0]
        ax1.plot(j, V, 'b-', linewidth=2)
        ax1.set_xlabel('Current Density (A/cm²)')
        ax1.set_ylabel('Cell Voltage (V)')
        ax1.set_title('AEM Polarization Curve')
        ax1.grid(True, alpha=0.3)
        
        # Efficiency
        efficiency = 1.23 / V * 100
        ax2 = axes[0, 1]
        ax2.plot(j, efficiency, 'g-', linewidth=2)
        ax2.set_xlabel('Current Density (A/cm²)')
        ax2.set_ylabel('Efficiency (%)')
        ax2.set_title('System Efficiency vs Current Density')
        ax2.grid(True, alpha=0.3)
        
        # Degradation over time
        time = np.linspace(0, 40000, 100)
        degradation = self.degradation_model(time)
        ax3 = axes[1, 0]
        ax3.plot(time/1000, degradation * 100, 'r-', linewidth=2)
        ax3.set_xlabel('Time (kHours)')
        ax3.set_ylabel('Membrane Degradation (%)')
        ax3.set_title('Membrane Degradation Over Time')
        ax3.grid(True, alpha=0.3)
        
        # Thermal profile
        temp = self.thermal_model(j)
        ax4 = axes[1, 1]
        ax4.plot(j, temp, 'orange', linewidth=2)
        ax4.set_xlabel('Current Density (A/cm²)')
        ax4.set_ylabel('Stack Temperature (°C)')
        ax4.set_title('Stack Thermal Profile')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('phase1/outputs/graphs/multiphysics_model.png', dpi=300, bbox_inches='tight')
        plt.savefig('phase1/outputs/graphs/multiphysics_model.pdf', bbox_inches='tight')
        plt.close()
        
        print("Multiphysics graphs saved to phase1/outputs/graphs/")
    
    def save_results(self):
        """Save all model results"""
        output = {
            'timestamp': self.timestamp,
            'model': 'AEM Electrolyzer Multiphysics Model v1.0',
            'parameters': {
                'reversible_potential': 1.23,
                'operating_temperature_range': [40, 80],
                'current_density_range': [0.1, 3.0]
            },
            'results': self.results
        }
        
        with open('phase1/outputs/reports/multiphysics_results.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Model results saved to phase1/outputs/reports/multiphysics_results.json")

if __name__ == "__main__":
    print("ENSGSI12IS - Phase 1: Multiphysics Model Generation")
    print("="*60)
    
    model = AEMElectrolyzerModel()
    model.generate_graphs()
    model.save_results()
    
    print("\nMultiphysics model complete. Outputs generated:")
    print("1. phase1/outputs/graphs/multiphysics_model.png")
    print("2. phase1/outputs/graphs/multiphysics_model.pdf")
    print("3. phase1/outputs/reports/multiphysics_results.json")
    print("\nThese outputs are suitable for inclusion in research reports.")
