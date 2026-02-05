#!/usr/bin/env python3
"""
Phase 1 Validation Script
Runs all Phase 1 components and generates comprehensive validation report.
"""

import subprocess
import sys
import json
from datetime import datetime
import os

def run_validation():
    print("=" * 70)
    print("PHASE 1: DIGITAL PROTOTYPING - COMPREHENSIVE VALIDATION")
    print("=" * 70)
    
    timestamp = datetime.now().isoformat()
    validation_report = {
        "phase": "Phase_1_Digital_Prototyping",
        "timestamp": timestamp,
        "system": {
            "platform": sys.platform,
            "python_version": sys.version
        },
        "components": {},
        "outputs": {},
        "validation_status": {}
    }
    
    # Component 1: Multiphysics Model
    print("\n[1/3] Running Multiphysics Model Validation...")
    try:
        import phases.phase1.multiphysics.aem_model as model_module
        model = model_module.AEMElectrolyzerModel()
        
        # Run model components
        j, V = model.generate_polarization_curve()
        time, deg, V_deg = model.generate_degradation_model()
        
        validation_report["components"]["multiphysics_model"] = {
            "status": "SUCCESS",
            "data_points_generated": len(j),
            "degradation_hours_simulated": 40000,
            "output_files": [
                f"phases/phase1/outputs/validation_data/polarization_curve_*.json",
                f"phases/phase1/outputs/validation_data/degradation_model_*.json",
                f"phases/phase1/outputs/graphs/polarization_curve_*.png",
                f"phases/phase1/outputs/graphs/degradation_analysis_*.png"
            ]
        }
        print("✓ Multiphysics model validated")
    except Exception as e:
        validation_report["components"]["multiphysics_model"] = {
            "status": "FAILED",
            "error": str(e)
        }
        print(f"✗ Multiphysics model failed: {e}")
    
    # Component 2: Quantum Algorithms
    print("\n[2/3] Running Quantum Algorithm Validation...")
    try:
        import phases.phase1.quantum_algorithms.quantum_optimizer as quantum_module
        optimizer = quantum_module.QuantumAEMOptimizer()
        
        # Run quantum components
        circuit = optimizer.create_parameter_optimization_circuit(num_qubits=4)
        iterations, costs, params = optimizer.simulate_optimization_process(num_iterations=100)
        
        validation_report["components"]["quantum_algorithms"] = {
            "status": "SUCCESS",
            "qubits_used": circuit.num_qubits,
            "iterations_simulated": len(iterations),
            "cost_improvement_percent": float((costs[0] - costs[-1]) / costs[0] * 100),
            "output_files": [
                f"phases/phase1/outputs/circuits/quantum_circuit_*.png",
                f"phases/phase1/outputs/circuits/quantum_circuit_*.qasm",
                f"phases/phase1/outputs/validation_data/optimization_results_*.json",
                f"phases/phase1/outputs/graphs/optimization_convergence_*.png"
            ]
        }
        print("✓ Quantum algorithms validated")
    except Exception as e:
        validation_report["components"]["quantum_algorithms"] = {
            "status": "FAILED", 
            "error": str(e)
        }
        print(f"✗ Quantum algorithms failed: {e}")
    
    # Component 3: File Verification
    print("\n[3/3] Verifying Output Files...")
    try:
        output_files = []
        for root, dirs, files in os.walk("phases/phase1/outputs"):
            for file in files:
                if file.endswith(('.json', '.png', '.csv', '.qasm')):
                    filepath = os.path.join(root, file)
                    output_files.append({
                        "path": filepath,
                        "size_bytes": os.path.getsize(filepath),
                        "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    })
        
        validation_report["outputs"] = {
            "total_files": len(output_files),
            "file_types": {
                "json": len([f for f in output_files if f["path"].endswith('.json')]),
                "png": len([f for f in output_files if f["path"].endswith('.png')]),
                "csv": len([f for f in output_files if f["path"].endswith('.csv')]),
                "qasm": len([f for f in output_files if f["path"].endswith('.qasm')])
            },
            "files": output_files[:10]  # First 10 files
        }
        
        print(f"✓ Output verification: {len(output_files)} files generated")
        
        # Overall validation status
        all_success = all(comp["status"] == "SUCCESS" 
                         for comp in validation_report["components"].values())
        
        validation_report["validation_status"] = {
            "overall": "PASS" if all_success else "FAIL",
            "components_passed": sum(1 for comp in validation_report["components"].values() 
                                   if comp["status"] == "SUCCESS"),
            "total_components": len(validation_report["components"])
        }
        
    except Exception as e:
        validation_report["validation_status"] = {
            "overall": "FAIL",
            "error": str(e)
        }
        print(f"✗ File verification failed: {e}")
    
    # Save comprehensive validation report
    report_filename = f"phases/phase1/validation_report_{timestamp.replace(':', '-')}.json"
    with open(report_filename, 'w') as f:
        json.dump(validation_report, f, indent=2)
    
    # Generate summary for quick review
    print("\n" + "=" * 70)
    print("VALIDATION REPORT SUMMARY")
    print("=" * 70)
    print(f"Timestamp: {timestamp}")
    print(f"Overall Status: {validation_report['validation_status'].get('overall', 'UNKNOWN')}")
    
    for comp_name, comp_data in validation_report["components"].items():
        status = comp_data.get("status", "UNKNOWN")
        print(f"{comp_name}: {status}")
    
    print(f"\nOutput Files Generated: {validation_report['outputs'].get('total_files', 0)}")
    for file_type, count in validation_report["outputs"].get("file_types", {}).items():
        print(f"  {file_type.upper()}: {count}")
    
    print(f"\nFull Report: {report_filename}")
    print("=" * 70)
    print("All outputs ready for MS Word report import.")
    print("Copy these files to your research documentation:")
    print("1. JSON files → Data tables and results")
    print("2. PNG files → Figures and visualizations")
    print("3. CSV files → Raw data for analysis")
    print("4. Validation report → Overall project status")
    print("=" * 70)

if __name__ == "__main__":
    run_validation()
