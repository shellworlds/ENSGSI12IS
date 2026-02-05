#!/usr/bin/env python3
"""
System Specification Check
Generates JSON output for research documentation
"""
import json
import platform
import psutil
import datetime
import subprocess
import sys

def get_system_info():
    """Collect system specifications"""
    info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "project": "ENSGSI12IS",
        "phase": "Phase 1 - Digital Prototyping",
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        },
        "hardware": {
            "cpu_count": psutil.cpu_count(logical=True),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "disk_free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
        },
        "git": {
            "username": subprocess.getoutput("git config user.name"),
            "email": subprocess.getoutput("git config user.email"),
            "repository": "ENSGSI12IS"
        }
    }
    
    # Check for quantum computing libraries
    quantum_libs = []
    for lib in ['qiskit', 'pennylane', 'cirq']:
        try:
            __import__(lib)
            quantum_libs.append(lib)
        except ImportError:
            pass
    
    info["dependencies"] = {
        "quantum_libraries_available": quantum_libs,
        "required_libraries": ["numpy", "scipy", "matplotlib", "torch", "tensorflow"]
    }
    
    return info

def save_output(info):
    """Save output in multiple formats for research documentation"""
    # JSON output (for data analysis)
    with open('phase1/outputs/reports/system_specs.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    # Text report (for MS Word inclusion)
    with open('phase1/outputs/reports/system_report.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("ENSGSI12IS - SYSTEM VERIFICATION REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Timestamp: {info['timestamp']}\n")
        f.write(f"Project Phase: {info['phase']}\n\n")
        
        f.write("SYSTEM SPECIFICATIONS:\n")
        f.write("-"*40 + "\n")
        f.write(f"OS: {info['system']['os']} {info['system']['os_release']}\n")
        f.write(f"Architecture: {info['system']['architecture']}\n")
        f.write(f"Processor: {info['system']['processor']}\n")
        f.write(f"Python: {info['system']['python_version']}\n\n")
        
        f.write("HARDWARE RESOURCES:\n")
        f.write("-"*40 + "\n")
        f.write(f"CPU Cores (logical): {info['hardware']['cpu_count']}\n")
        f.write(f"CPU Cores (physical): {info['hardware']['cpu_count_physical']}\n")
        f.write(f"RAM Total: {info['hardware']['ram_total_gb']} GB\n")
        f.write(f"RAM Available: {info['hardware']['ram_available_gb']} GB\n")
        f.write(f"Disk Total: {info['hardware']['disk_total_gb']} GB\n")
        f.write(f"Disk Free: {info['hardware']['disk_free_gb']} GB\n\n")
        
        f.write("GIT CONFIGURATION:\n")
        f.write("-"*40 + "\n")
        f.write(f"Username: {info['git']['username']}\n")
        f.write(f"Email: {info['git']['email']}\n")
        f.write(f"Repository: {info['git']['repository']}\n\n")
        
        f.write("DEPENDENCIES STATUS:\n")
        f.write("-"*40 + "\n")
        f.write(f"Quantum Libraries Available: {', '.join(info['dependencies']['quantum_libraries_available'])}\n")
        f.write(f"Required Libraries: {', '.join(info['dependencies']['required_libraries'])}\n")
    
    # Markdown for GitHub
    with open('SYSTEM_VERIFICATION.md', 'w') as f:
        f.write(f"# System Verification - {info['timestamp']}\n\n")
        f.write("## Hardware Specifications\n")
        f.write(f"- **CPU**: {info['hardware']['cpu_count']} cores ({info['hardware']['cpu_count_physical']} physical)\n")
        f.write(f"- **RAM**: {info['hardware']['ram_total_gb']} GB total, {info['hardware']['ram_available_gb']} GB available\n")
        f.write(f"- **Storage**: {info['hardware']['disk_total_gb']} GB total, {info['hardware']['disk_free_gb']} GB free\n\n")
        f.write("## Software Environment\n")
        f.write(f"- **OS**: {info['system']['os']} {info['system']['os_release']}\n")
        f.write(f"- **Python**: {info['system']['python_version']}\n")
    
    print(f"System check completed. Output saved to:")
    print(f"  - phase1/outputs/reports/system_specs.json")
    print(f"  - phase1/outputs/reports/system_report.txt")
    print(f"  - SYSTEM_VERIFICATION.md")

if __name__ == "__main__":
    print("ENSGSI12IS - Phase 1: System Verification")
    print("="*50)
    
    info = get_system_info()
    save_output(info)
    
    # Check minimum requirements
    if info['hardware']['ram_total_gb'] < 16:
        print("\nWARNING: System RAM below recommended 16GB minimum")
    if info['hardware']['cpu_count_physical'] < 4:
        print("WARNING: CPU cores below recommended 4-core minimum")
    
    print("\nVerification complete. Proceed to multiphysics modeling.")
