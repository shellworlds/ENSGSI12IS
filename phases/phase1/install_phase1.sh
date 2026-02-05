#!/bin/bash
# Phase 1 Installation Script
# Generates verifiable outputs for research documentation

echo "==============================================="
echo "ENSGSI12IS - PHASE 1 INSTALLATION & VALIDATION"
echo "==============================================="

# Check Python version
echo "[1/4] Checking system requirements..."
python3 --version
pip3 --version

# Install required packages
echo "[2/4] Installing Python packages..."
pip3 install numpy matplotlib --quiet
pip3 install qiskit --quiet 2>/dev/null || echo "Note: Quantum simulation optional"

# Create output directories
echo "[3/4] Setting up output directories..."
mkdir -p phases/phase1/outputs/{models,circuits,graphs,validation_data}

# Make scripts executable
chmod +x phases/phase1/multiphysics/aem_model.py
chmod +x phases/phase1/quantum_algorithms/quantum_optimizer.py
chmod +x phases/phase1/validate_phase1.py

# Run validation
echo "[4/4] Running Phase 1 validation..."
cd phases/phase1
python3 validate_phase1.py

echo ""
echo "==============================================="
echo "INSTALLATION COMPLETE"
echo "==============================================="
echo "Output files generated in: phases/phase1/outputs/"
echo "Validation report: phases/phase1/validation_report_*.json"
echo ""
echo "For MS Word report import:"
echo "1. Use PNG files for figures (300 DPI)"
echo "2. Use JSON files for data tables"
echo "3. Use CSV files for raw data"
echo "==============================================="
