#!/bin/bash
# Verification script for Phase 1 outputs

echo "PHASE 1 OUTPUT VERIFICATION"
echo "============================"
echo "Timestamp: $(date -Iseconds)"
echo ""

# Check output directories
echo "Checking output directories..."
if [ -d "phases/phase1/outputs" ]; then
    echo "✓ Output directory exists"
    
    # Count files by type
    echo ""
    echo "File counts by type:"
    find phases/phase1/outputs -name "*.json" | wc -l | xargs echo "  JSON files:"
    find phases/phase1/outputs -name "*.png" | wc -l | xargs echo "  PNG files:"
    find phases/phase1/outputs -name "*.csv" | wc -l | xargs echo "  CSV files:"
    find phases/phase1/outputs -name "*.qasm" | wc -l | xargs echo "  QASM files:"
    
    # Show latest files
    echo ""
    echo "Latest generated files:"
    find phases/phase1/outputs -type f -name "*.json" -o -name "*.png" | sort -r | head -5 | while read file; do
        echo "  $(basename "$file")"
    done
else
    echo "✗ Output directory not found"
fi

echo ""
echo "To generate Phase 1 outputs:"
echo "  ./phases/phase1/install_phase1.sh"
echo ""
echo "Outputs are ready for MS Word report import."
echo "Use absolute paths for embedding in documents."
