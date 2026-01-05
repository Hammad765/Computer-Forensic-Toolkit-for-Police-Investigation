#!/usr/bin/env python3
"""
Performance Monitor Module
Tracks CPU, Memory, and Latency metrics for forensic evidence

© Copyright Hammad Arshad & Lewis Golightly 2025
"""

import psutil
import time
import csv
import json
import os
from datetime import datetime
from threading import Thread, Event

# Import color codes
try:
    from color import *
except:
    # Fallback if color module not available
    RED = GREEN = GOLD = CYAN = ORANGE = RESET = ""


class PerformanceMonitor:
    """Monitor and log performance metrics (CPU, Memory, Latency)"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()
        
        # Storage for current monitoring session
        self.current_module = None
        self.cpu_samples = []
        self.memory_samples = []
        self.start_time = None
        self.end_time = None
        
        # Storage for completed sessions
        self.sessions = []
        
        # Latency tracking
        self.latency_logs = []
        
        print(f"{GREEN}[✓] Performance Monitor initialized{RESET}")
    
    def start_monitoring(self, module_name):
        """Start monitoring CPU and Memory for a module"""
        if self.monitoring:
            print(f"{GOLD}[i] Already monitoring. Stopping previous session...{RESET}")
            self.stop_monitoring()
        
        self.current_module = module_name
        self.cpu_samples = []
        self.memory_samples = []
        self.start_time = time.time()
        self.monitoring = True
        self.stop_event.clear()
        
        # Start monitoring thread
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print(f"{CYAN}[●] Monitoring started for: {module_name}{RESET}")
    
    def _monitor_loop(self):
        """Internal loop that collects CPU and Memory samples"""
        while not self.stop_event.is_set():
            try:
                # Get CPU usage (interval=1 means measure over 1 second)
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # Get memory usage (RSS - Resident Set Size)
                memory_info = self.process.memory_info()
                memory_bytes = memory_info.rss
                
                # Store samples
                self.cpu_samples.append(cpu_percent)
                self.memory_samples.append(memory_bytes)
                
            except Exception as e:
                print(f"{RED}[✗] Error in monitoring loop: {e}{RESET}")
                break
    
    def stop_monitoring(self):
        """Stop monitoring and save session data"""
        if not self.monitoring:
            print(f"{GOLD}[i] No active monitoring session{RESET}")
            return
        
        # Signal thread to stop
        self.stop_event.set()
        self.end_time = time.time()
        self.monitoring = False
        
        # Wait for thread to finish
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        # Calculate statistics
        if self.cpu_samples and self.memory_samples:
            session_data = {
                "module": self.current_module,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.end_time - self.start_time,
                "cpu_samples": self.cpu_samples.copy(),
                "memory_samples": self.memory_samples.copy(),
                "cpu_avg": sum(self.cpu_samples) / len(self.cpu_samples),
                "cpu_min": min(self.cpu_samples),
                "cpu_max": max(self.cpu_samples),
                "memory_avg": sum(self.memory_samples) / len(self.memory_samples),
                "memory_min": min(self.memory_samples),
                "memory_max": max(self.memory_samples),
                "timestamp": datetime.now().isoformat()
            }
            
            self.sessions.append(session_data)
            
            print(f"{GREEN}[✓] Monitoring stopped for: {self.current_module}{RESET}")
            print(f"  └─ Samples collected: CPU={len(self.cpu_samples)}, Memory={len(self.memory_samples)}")
        else:
            print(f"{RED}[✗] No samples collected{RESET}")
    
    def get_last_cpu_avg(self):
        """Get average CPU usage from last monitoring session"""
        if self.sessions:
            return self.sessions[-1]["cpu_avg"]
        return 0.0
    
    def get_last_cpu_min(self):
        """Get minimum CPU usage from last monitoring session"""
        if self.sessions:
            return self.sessions[-1]["cpu_min"]
        return 0.0
    
    def get_last_cpu_max(self):
        """Get maximum CPU usage from last monitoring session"""
        if self.sessions:
            return self.sessions[-1]["cpu_max"]
        return 0.0
    
    def get_last_memory_avg(self):
        """Get average memory usage from last monitoring session (in bytes)"""
        if self.sessions:
            return self.sessions[-1]["memory_avg"]
        return 0.0
    
    def get_last_memory_min(self):
        """Get minimum memory usage from last monitoring session (in bytes)"""
        if self.sessions:
            return self.sessions[-1]["memory_min"]
        return 0.0
    
    def get_last_memory_max(self):
        """Get maximum memory usage from last monitoring session (in bytes)"""
        if self.sessions:
            return self.sessions[-1]["memory_max"]
        return 0.0
    
    def log_latency(self, module_name, operation, duration):
        """Log latency for a specific operation"""
        latency_entry = {
            "module": module_name,
            "operation": operation,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        self.latency_logs.append(latency_entry)
        
        print(f"{CYAN}[⏱] Latency logged: {module_name} - {operation} = {duration:.2f}s{RESET}")
    
    def export_to_csv(self, filename=None):
        """Export all sessions to CSV file"""
        if not self.sessions:
            print(f"{GOLD}[i] No sessions to export{RESET}")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_metrics_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = [
                    'module', 'timestamp', 'duration', 
                    'cpu_avg', 'cpu_min', 'cpu_max',
                    'memory_avg_mb', 'memory_min_mb', 'memory_max_mb',
                    'samples_count'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for session in self.sessions:
                    writer.writerow({
                        'module': session['module'],
                        'timestamp': session['timestamp'],
                        'duration': f"{session['duration']:.2f}",
                        'cpu_avg': f"{session['cpu_avg']:.2f}",
                        'cpu_min': f"{session['cpu_min']:.2f}",
                        'cpu_max': f"{session['cpu_max']:.2f}",
                        'memory_avg_mb': f"{session['memory_avg'] / (1024*1024):.2f}",
                        'memory_min_mb': f"{session['memory_min'] / (1024*1024):.2f}",
                        'memory_max_mb': f"{session['memory_max'] / (1024*1024):.2f}",
                        'samples_count': len(session['cpu_samples'])
                    })
            
            print(f"{GREEN}[✓] Performance metrics exported to: {filename}{RESET}")
            
        except Exception as e:
            print(f"{RED}[✗] Failed to export CSV: {e}{RESET}")
    
    def export_latency_to_csv(self, filename=None):
        """Export latency logs to CSV file"""
        if not self.latency_logs:
            print(f"{GOLD}[i] No latency logs to export{RESET}")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"latency_logs_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['module', 'operation', 'duration_seconds', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for log in self.latency_logs:
                    writer.writerow(log)
            
            print(f"{GREEN}[✓] Latency logs exported to: {filename}{RESET}")
            
        except Exception as e:
            print(f"{RED}[✗] Failed to export latency CSV: {e}{RESET}")
    
    def generate_summary(self):
        """Generate and display summary of all monitoring sessions"""
        if not self.sessions:
            print(f"\n{GOLD}[i] No performance data collected yet{RESET}\n")
            return
        
        print(f"\n{GOLD}{'='*60}{RESET}")
        print(f"{CYAN}PERFORMANCE MONITORING SUMMARY{RESET}")
        print(f"{GOLD}{'='*60}{RESET}\n")
        
        # Group sessions by module
        module_sessions = {}
        for session in self.sessions:
            module = session['module']
            if module not in module_sessions:
                module_sessions[module] = []
            module_sessions[module].append(session)
        
        # Display summary for each module
        for module, sessions in module_sessions.items():
            print(f"{CYAN}━━━ {module} ━━━{RESET}")
            print(f"  Sessions: {len(sessions)}")
            
            # Calculate averages across all sessions
            avg_cpu = sum(s['cpu_avg'] for s in sessions) / len(sessions)
            avg_memory_mb = sum(s['memory_avg'] for s in sessions) / len(sessions) / (1024*1024)
            avg_duration = sum(s['duration'] for s in sessions) / len(sessions)
            
            print(f"  Average CPU:    {avg_cpu:.2f}%")
            print(f"  Average Memory: {avg_memory_mb:.2f} MB")
            print(f"  Average Time:   {avg_duration:.2f} seconds")
            print()
        
        # Display latency summary
        if self.latency_logs:
            print(f"{CYAN}━━━ Latency Logs ━━━{RESET}")
            print(f"  Total Operations: {len(self.latency_logs)}")
            
            # Group by module
            module_latencies = {}
            for log in self.latency_logs:
                module = log['module']
                if module not in module_latencies:
                    module_latencies[module] = []
                module_latencies[module].append(log['duration_seconds'])
            
            for module, durations in module_latencies.items():
                avg_latency = sum(durations) / len(durations)
                print(f"  {module}: {avg_latency:.2f}s average")
            print()
        
        # Export data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.export_to_csv(f"performance_metrics_{timestamp}.csv")
        
        if self.latency_logs:
            self.export_latency_to_csv(f"latency_logs_{timestamp}.csv")
        
        print(f"{GOLD}{'='*60}{RESET}\n")
    
    def get_current_stats(self):
        """Get current statistics during active monitoring"""
        if not self.monitoring or not self.cpu_samples:
            return None
        
        return {
            "module": self.current_module,
            "cpu_current": self.cpu_samples[-1] if self.cpu_samples else 0,
            "cpu_avg": sum(self.cpu_samples) / len(self.cpu_samples),
            "memory_current_mb": (self.memory_samples[-1] / (1024*1024)) if self.memory_samples else 0,
            "memory_avg_mb": (sum(self.memory_samples) / len(self.memory_samples)) / (1024*1024),
            "samples_collected": len(self.cpu_samples),
            "elapsed_time": time.time() - self.start_time if self.start_time else 0
        }


# Global monitor instance
_monitor_instance = None


def init_monitor():
    """Initialize and return global performance monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = PerformanceMonitor()
    return _monitor_instance


def get_monitor():
    """Get existing monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        print(f"{RED}[✗] Monitor not initialized. Call init_monitor() first{RESET}")
        return None
    return _monitor_instance


# For standalone testing
if __name__ == "__main__":
    print("Testing Performance Monitor...")
    
    monitor = init_monitor()
    
    # Test monitoring
    print("\nStarting test monitoring for 5 seconds...")
    monitor.start_monitoring("Test_Module")
    
    time.sleep(5)
    
    monitor.stop_monitoring()
    
    # Display results
    print(f"\nResults:")
    print(f"  CPU Avg: {monitor.get_last_cpu_avg():.2f}%")
    print(f"  CPU Min: {monitor.get_last_cpu_min():.2f}%")
    print(f"  CPU Max: {monitor.get_last_cpu_max():.2f}%")
    print(f"  Memory Avg: {monitor.get_last_memory_avg() / (1024*1024):.2f} MB")
    
    # Test latency logging
    monitor.log_latency("Test_Module", "Test_Operation", 5.0)
    
    # Generate summary
    monitor.generate_summary()
    
    print("\nTest complete!")
