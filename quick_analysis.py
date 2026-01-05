#!/usr/bin/env python3
"""
Quick Analysis Script for Supervisor Presentation
Generates summary table and charts from performance data
Run this AFTER completing all tests
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

print("=" * 80)
print("QUICK ANALYSIS FOR SUPERVISOR PRESENTATION")
print("=" * 80)

# Check if performance_logs directory exists
if not os.path.exists('performance_logs'):
    print("\n❌ ERROR: performance_logs directory not found!")
    print("Make sure you're running this from the toolkit directory.")
    exit(1)

# Find all CSV files
cpu_files = glob.glob('performance_logs/cpu_usage_*.csv')
mem_files = glob.glob('performance_logs/memory_usage_*.csv')
lat_files = glob.glob('performance_logs/latency_*.csv')

print(f"\n📊 Found {len(cpu_files)} CPU log files")
print(f"📊 Found {len(mem_files)} Memory log files")
print(f"📊 Found {len(lat_files)} Latency log files")

if len(cpu_files) == 0:
    print("\n❌ ERROR: No CSV files found!")
    print("Run some tests first, then come back to this script.")
    exit(1)

# Combine all CSV files
print("\n⏳ Combining CSV files...")

# Read and combine CPU data
cpu_dfs = []
for f in cpu_files:
    try:
        df = pd.read_csv(f)
        cpu_dfs.append(df)
    except:
        pass
cpu_df = pd.concat(cpu_dfs, ignore_index=True)

# Read and combine Memory data
mem_dfs = []
for f in mem_files:
    try:
        df = pd.read_csv(f)
        mem_dfs.append(df)
    except:
        pass
mem_df = pd.concat(mem_dfs, ignore_index=True)

# Read and combine Latency data
lat_dfs = []
for f in lat_files:
    try:
        df = pd.read_csv(f)
        lat_dfs.append(df)
    except:
        pass
lat_df = pd.concat(lat_dfs, ignore_index=True)

print(f"✅ CPU data: {len(cpu_df)} measurements")
print(f"✅ Memory data: {len(mem_df)} measurements")
print(f"✅ Latency data: {len(lat_df)} operations")

# Analyze CPU by module
print("\n" + "=" * 80)
print("CPU USAGE BY MODULE")
print("=" * 80)
cpu_by_module = cpu_df.groupby('Module')['CPU_Percent'].agg(['mean', 'median', 'std', 'min', 'max'])
cpu_by_module = cpu_by_module.round(2)
print(cpu_by_module)

# Analyze Memory by module
print("\n" + "=" * 80)
print("MEMORY USAGE (RSS) BY MODULE")
print("=" * 80)
mem_by_module = mem_df.groupby('Module')['RSS_MB'].agg(['mean', 'median', 'std', 'min', 'max'])
mem_by_module = mem_by_module.round(2)
print(mem_by_module)

# Analyze Latency by module
print("\n" + "=" * 80)
print("LATENCY BY MODULE")
print("=" * 80)
# Filter successful operations only
lat_successful = lat_df[lat_df['Status'] == 'success']
lat_by_module = lat_successful.groupby('Module')['Duration_Seconds'].agg(['mean', 'median', 'std', 'min', 'max'])
lat_by_module = lat_by_module.round(3)
print(lat_by_module)

# Create comprehensive summary
print("\n⏳ Creating summary table...")
summary = pd.DataFrame({
    'Avg_CPU_%': cpu_by_module['mean'],
    'Max_CPU_%': cpu_by_module['max'],
    'Avg_Memory_MB': mem_by_module['mean'],
    'Max_Memory_MB': mem_by_module['max'],
    'Avg_Latency_s': lat_by_module['mean'],
    'Max_Latency_s': lat_by_module['max']
})
summary = summary.round(2)

# Save summary
summary_file = 'SUMMARY_FOR_SUPERVISOR.csv'
summary.to_csv(summary_file)
print(f"✅ Summary saved to: {summary_file}")

print("\n" + "=" * 80)
print("SUMMARY TABLE FOR SUPERVISOR")
print("=" * 80)
print(summary)

# Create visualizations
print("\n⏳ Creating charts...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Computer Forensic Toolkit - Performance Analysis', fontsize=16, fontweight='bold')

# Chart 1: Average CPU Usage
cpu_by_module['mean'].plot(kind='bar', ax=axes[0, 0], color='steelblue', edgecolor='black')
axes[0, 0].set_title('Average CPU Usage by Module', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('CPU Usage (%)', fontsize=10)
axes[0, 0].set_xlabel('Module', fontsize=10)
axes[0, 0].grid(axis='y', alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# Chart 2: Average Memory Usage
mem_by_module['mean'].plot(kind='bar', ax=axes[0, 1], color='seagreen', edgecolor='black')
axes[0, 1].set_title('Average Memory Usage by Module', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Memory (MB)', fontsize=10)
axes[0, 1].set_xlabel('Module', fontsize=10)
axes[0, 1].grid(axis='y', alpha=0.3)
axes[0, 1].tick_params(axis='x', rotation=45)

# Chart 3: Average Latency
lat_by_module['mean'].plot(kind='bar', ax=axes[0, 2], color='coral', edgecolor='black')
axes[0, 2].set_title('Average Latency by Module', fontsize=12, fontweight='bold')
axes[0, 2].set_ylabel('Latency (seconds)', fontsize=10)
axes[0, 2].set_xlabel('Module', fontsize=10)
axes[0, 2].grid(axis='y', alpha=0.3)
axes[0, 2].tick_params(axis='x', rotation=45)

# Chart 4: CPU Distribution (Box plot)
cpu_df.boxplot(column='CPU_Percent', by='Module', ax=axes[1, 0])
axes[1, 0].set_title('CPU Usage Distribution', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('CPU Usage (%)', fontsize=10)
axes[1, 0].set_xlabel('Module', fontsize=10)
axes[1, 0].tick_params(axis='x', rotation=45)
plt.sca(axes[1, 0])
plt.xticks(rotation=45, ha='right')

# Chart 5: Memory Distribution (Box plot)
mem_df.boxplot(column='RSS_MB', by='Module', ax=axes[1, 1])
axes[1, 1].set_title('Memory Usage Distribution', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Memory (MB)', fontsize=10)
axes[1, 1].set_xlabel('Module', fontsize=10)
axes[1, 1].tick_params(axis='x', rotation=45)
plt.sca(axes[1, 1])
plt.xticks(rotation=45, ha='right')

# Chart 6: Latency Distribution (Box plot)
lat_successful.boxplot(column='Duration_Seconds', by='Module', ax=axes[1, 2])
axes[1, 2].set_title('Latency Distribution', fontsize=12, fontweight='bold')
axes[1, 2].set_ylabel('Latency (seconds)', fontsize=10)
axes[1, 2].set_xlabel('Module', fontsize=10)
axes[1, 2].tick_params(axis='x', rotation=45)
plt.sca(axes[1, 2])
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
chart_file = 'CHARTS_FOR_SUPERVISOR.png'
plt.savefig(chart_file, dpi=300, bbox_inches='tight')
print(f"✅ Charts saved to: {chart_file}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n📁 Files created for supervisor:")
print(f"   1. {summary_file}")
print(f"   2. {chart_file}")
print(f"\n👨‍🎓 Show these to your supervisor tomorrow!")
print("=" * 80)

# Additional statistics
print("\n" + "=" * 80)
print("ADDITIONAL STATISTICS")
print("=" * 80)
print(f"Total test runs: {len(lat_df)}")
print(f"Successful runs: {len(lat_successful)}")
print(f"Total CPU measurements: {len(cpu_df)}")
print(f"Total Memory measurements: {len(mem_df)}")
print(f"Total data points: ~{len(cpu_df) + len(mem_df) + len(lat_df)}")
print("=" * 80)

print("\n✅ ALL DONE! Good luck with your supervisor meeting! 🎓🚀")
