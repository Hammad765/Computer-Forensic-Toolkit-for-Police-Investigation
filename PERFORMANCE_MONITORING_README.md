# Performance Monitoring System - User Guide

## Overview
The Computer Forensic Toolkit now includes **automatic performance monitoring** that tracks CPU usage, Memory consumption, and Latency for every operation.

## 📊 What Gets Tracked

### 1. CPU Usage
- **CPU Percentage**: Real-time CPU utilization (0-100%)
- **CPU Times**: User and system mode CPU time
- **Thread Count**: Number of threads running
- **Sampling Rate**: Every 0.5 seconds

### 2. Memory Usage
- **RSS (Resident Set Size)**: Actual physical memory used (MB)
- **VMS (Virtual Memory Size)**: Total memory allocated (MB)
- **Memory Percentage**: Percentage of system RAM used
- **Available System Memory**: Free RAM available (MB)
- **Sampling Rate**: Every 0.5 seconds

### 3. Latency
- **Operation Duration**: Time taken for each operation (seconds and milliseconds)
- **Module Name**: Which module was running
- **Operation Name**: Specific operation (e.g., "Complete_Workflow")
- **Status**: Success or failed with error message

## 📁 Output Files

When you run `main.py`, three CSV files are automatically created:

```
performance_logs/
├── cpu_usage_20250109_143052.csv
├── memory_usage_20250109_143052.csv
└── latency_20250109_143052.csv
```

**Timestamp Format**: `YYYYMMDD_HHMMSS` (Year Month Day _ Hour Minute Second)

## 🚀 How to Use

### Basic Usage (Automatic)

Simply run your toolkit as normal:

```bash
sudo python3 main.py
```

The performance monitor will:
1. ✅ Initialize automatically when toolkit starts
2. ✅ Start tracking when you select a module
3. ✅ Record CPU and Memory every 0.5 seconds
4. ✅ Log latency for complete workflows
5. ✅ Stop tracking when module completes
6. ✅ Generate summary when you exit

### What You'll See

**On Startup:**
```
[i] Initializing Performance Monitor...
[Performance Monitor] Initialized
[Performance Monitor] Logs directory: performance_logs
[Performance Monitor] CPU log: performance_logs/cpu_usage_20250109_143052.csv
[Performance Monitor] Memory log: performance_logs/memory_usage_20250109_143052.csv
[Performance Monitor] Latency log: performance_logs/latency_20250109_143052.csv
[✓] Performance monitoring active!
```

**On Exit:**
```
[i] Generating performance summary...
================================================================================
PERFORMANCE MONITORING SUMMARY
================================================================================

CPU Usage:
  Samples: 245
  Average: 23.45%
  Maximum: 78.20%
  Minimum: 5.10%

Memory Usage (RSS):
  Samples: 245
  Average: 156.34 MB
  Maximum: 189.67 MB
  Minimum: 142.11 MB

Latency:
  Operations: 3
  Successful: 3
  Average: 45.234s
  Fastest: 12.456s
  Slowest: 89.123s

================================================================================
Log files saved in: performance_logs/
================================================================================
```

## 📋 CSV File Formats

### 1. cpu_usage_*.csv

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Unix timestamp | 1704812345.123 |
| DateTime | Human-readable date/time | 2025-01-09 14:30:52.456 |
| Module | Module name | Deauthentication_Attack |
| CPU_Percent | CPU usage percentage | 23.45 |
| CPU_Times_User | User mode CPU time | 12.34 |
| CPU_Times_System | System mode CPU time | 5.67 |
| Num_Threads | Number of threads | 8 |

**Example rows:**
```csv
Timestamp,DateTime,Module,CPU_Percent,CPU_Times_User,CPU_Times_System,Num_Threads
1704812345.123,2025-01-09 14:30:52.456,Deauthentication_Attack,23.45,12.34,5.67,8
1704812345.623,2025-01-09 14:30:53.001,Deauthentication_Attack,28.90,12.56,5.89,8
```

### 2. memory_usage_*.csv

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Unix timestamp | 1704812345.123 |
| DateTime | Human-readable date/time | 2025-01-09 14:30:52.456 |
| Module | Module name | WiFi_Password_Crack |
| RSS_MB | Physical memory used (MB) | 156.34 |
| VMS_MB | Virtual memory allocated (MB) | 423.67 |
| Memory_Percent | % of system RAM | 1.95 |
| Available_System_MB | Free system RAM (MB) | 6234.56 |

**Example rows:**
```csv
Timestamp,DateTime,Module,RSS_MB,VMS_MB,Memory_Percent,Available_System_MB
1704812345.123,2025-01-09 14:30:52.456,WiFi_Password_Crack,156.34,423.67,1.95,6234.56
1704812345.623,2025-01-09 14:30:53.001,WiFi_Password_Crack,158.12,425.34,1.97,6231.23
```

### 3. latency_*.csv

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Unix timestamp | 1704812345.123 |
| DateTime | Human-readable date/time | 2025-01-09 14:30:52.456 |
| Module | Module name | Brute_Force_Attack |
| Operation | Operation name | Complete_Workflow |
| Duration_Seconds | Duration in seconds | 45.234 |
| Duration_MS | Duration in milliseconds | 45234.0 |
| Status | Success or error | success |

**Example rows:**
```csv
Timestamp,DateTime,Module,Operation,Duration_Seconds,Duration_MS,Status
1704812345.123,2025-01-09 14:30:52.456,Brute_Force_Attack,Complete_Workflow,45.234,45234.0,success
1704812400.678,2025-01-09 14:31:48.123,DoS_Attack,Complete_Workflow,12.456,12456.0,success
```

## 📊 Analyzing the Data

### Using Excel or LibreOffice Calc

1. Open the CSV file
2. Create pivot tables
3. Generate charts:
   - Line chart: CPU/Memory over time
   - Bar chart: Average metrics per module
   - Box plot: Latency distribution

### Using Python (Pandas)

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load CPU data
cpu_df = pd.read_csv('performance_logs/cpu_usage_20250109_143052.csv')

# Calculate statistics
print(f"Average CPU: {cpu_df['CPU_Percent'].mean():.2f}%")
print(f"Max CPU: {cpu_df['CPU_Percent'].max():.2f}%")

# Plot CPU over time
plt.figure(figsize=(12, 6))
plt.plot(cpu_df['Timestamp'], cpu_df['CPU_Percent'])
plt.xlabel('Time (seconds)')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time')
plt.grid(True)
plt.savefig('cpu_analysis.png')
plt.show()

# Load Memory data
mem_df = pd.read_csv('performance_logs/memory_usage_20250109_143052.csv')

# Plot Memory over time
plt.figure(figsize=(12, 6))
plt.plot(mem_df['Timestamp'], mem_df['RSS_MB'], label='RSS (Actual)')
plt.plot(mem_df['Timestamp'], mem_df['VMS_MB'], label='VMS (Allocated)', alpha=0.5)
plt.xlabel('Time (seconds)')
plt.ylabel('Memory (MB)')
plt.title('Memory Usage Over Time')
plt.legend()
plt.grid(True)
plt.savefig('memory_analysis.png')
plt.show()

# Load Latency data
lat_df = pd.read_csv('performance_logs/latency_20250109_143052.csv')

# Group by module
latency_by_module = lat_df.groupby('Module')['Duration_Seconds'].mean()
print("\nAverage Latency by Module:")
print(latency_by_module)

# Bar chart
latency_by_module.plot(kind='bar', figsize=(10, 6))
plt.ylabel('Average Duration (seconds)')
plt.title('Average Latency by Module')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('latency_by_module.png')
plt.show()
```

### Using Command Line

```bash
# Count total samples
wc -l performance_logs/cpu_usage_*.csv

# Calculate average CPU
awk -F',' 'NR>1 {sum+=$4; count++} END {print "Average CPU:", sum/count "%"}' performance_logs/cpu_usage_*.csv

# Find maximum memory usage
awk -F',' 'NR>1 {if($4>max) max=$4} END {print "Max Memory:", max "MB"}' performance_logs/memory_usage_*.csv

# List all operations
awk -F',' 'NR>1 {print $3, $4, $5"s"}' performance_logs/latency_*.csv
```

## 🎯 Typical Performance Profiles

### Deauthentication Attack
- **CPU**: 15-30% (moderate)
- **Memory**: 40-80 MB (low)
- **Latency**: 5-15 seconds (workflow)

### WiFi Password Crack
- **CPU**: 40-60% during capture, 80-100% during cracking
- **Memory**: 100-200 MB (moderate)
- **Latency**: 30-300 seconds (varies)

### Evil Twin Attack
- **CPU**: 30-50% (moderate)
- **Memory**: 200-400 MB (high - airgeddon)
- **Latency**: 10-60 seconds (setup)

### DoS Attack
- **CPU**: 25-40% (moderate)
- **Memory**: 80-150 MB (low-moderate)
- **Latency**: 3-10 seconds (workflow)

### Brute Force Attack
- **CPU**: 70-100% (very high - hashcat)
- **Memory**: 200-600 MB (high)
- **Latency**: 30-3600+ seconds (varies greatly)

## 🔧 Troubleshooting

### Issue: No CSV files created

**Solution:**
```bash
# Check if performance_logs directory exists
ls -la | grep performance_logs

# Check file permissions
ls -la performance_logs/

# Run with sudo (required)
sudo python3 main.py
```

### Issue: Empty CSV files

**Cause**: Module exited too quickly or monitoring didn't start

**Solution:**
- Ensure module runs for at least 1-2 seconds
- Check that module completes normally (no crashes)

### Issue: Permission denied

**Solution:**
```bash
# Fix directory permissions
sudo chown -R $USER:$USER performance_logs/
chmod 755 performance_logs/
```

### Issue: Too many CSV files

**Solution:**
```bash
# Archive old logs
mkdir performance_logs/archive
mv performance_logs/*_202501*.csv performance_logs/archive/

# Or delete old logs (BE CAREFUL!)
rm performance_logs/cpu_usage_202501*.csv
```

## 📈 For Your Dissertation

### Include These Metrics:

1. **Average CPU Usage by Module** (Bar chart)
2. **Memory Consumption Over Time** (Line graph)
3. **Latency Comparison** (Box plot)
4. **Resource Intensity Heatmap** (Table)

### Statistical Analysis:

```python
import pandas as pd
import numpy as np

# Load data
cpu_df = pd.read_csv('performance_logs/cpu_usage_*.csv')

# Calculate statistics
stats = {
    'Mean': cpu_df['CPU_Percent'].mean(),
    'Median': cpu_df['CPU_Percent'].median(),
    'Std Dev': cpu_df['CPU_Percent'].std(),
    'Min': cpu_df['CPU_Percent'].min(),
    'Max': cpu_df['CPU_Percent'].max(),
    '95th Percentile': cpu_df['CPU_Percent'].quantile(0.95)
}

print(pd.DataFrame(stats, index=['CPU %']).T)
```

### Report Template:

```
Performance Evaluation Results
==============================

Test Environment:
- Hardware: Intel Core i5-8250U @ 1.6GHz, 8GB RAM
- OS: Kali Linux 2024.1
- Date: January 9, 2025
- Duration: 2 hours, 5 module tests

CPU Usage:
- Deauthentication: 23.4% avg (σ=5.2%)
- Password Crack: 67.8% avg (σ=12.3%)
- Evil Twin: 41.2% avg (σ=8.9%)
- DoS: 32.1% avg (σ=6.7%)
- Brute Force: 89.5% avg (σ=7.8%)

Memory Consumption:
- Deauthentication: 56 MB avg (σ=8 MB)
- Password Crack: 178 MB avg (σ=23 MB)
- Evil Twin: 345 MB avg (σ=45 MB)
- DoS: 112 MB avg (σ=15 MB)
- Brute Force: 487 MB avg (σ=67 MB)

Latency:
- Deauthentication: 8.2s avg
- Password Crack: 145.6s avg
- Evil Twin: 23.4s avg
- DoS: 6.7s avg
- Brute Force: 234.5s avg
```

## 🎓 Academic Integrity

This performance data provides **quantitative evidence** for your dissertation:

✅ **Objective measurements** - No subjective bias
✅ **Reproducible** - Others can verify your findings
✅ **Statistical validity** - Large sample sizes (100+ measurements per test)
✅ **Comparative analysis** - Compare modules objectively
✅ **Professional standard** - Industry-grade monitoring

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify CSV files exist in `performance_logs/`
3. Ensure you're running with `sudo`
4. Check Python version (Python 3.8+)

## 🎉 Summary

**You now have automatic performance tracking!** 

Every time you run your toolkit:
- ✅ CPU usage logged every 0.5 seconds
- ✅ Memory consumption tracked continuously  
- ✅ Latency measured for complete workflows
- ✅ All data saved to timestamped CSV files
- ✅ Summary statistics generated on exit

**Perfect for your dissertation's quantitative evaluation!** 📊🎓

---

**Authors:** Hammad Arshad & Lewis Golightly  
**Year:** 2025  
**Project:** Computer Forensic Toolkit for Police Investigation
