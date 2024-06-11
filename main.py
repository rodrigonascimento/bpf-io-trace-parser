from pathlib import Path
from io_profiler.file_reader import TraceFileReader
from io_profiler.global_io_stats import GlobalSysCallCount, GlobalPidTidInfo, GlobalCSVFy
from io_profiler.per_file_io_stats import PerFileSysCallCount
from io_profiler.telemetry import TelemetryContentRouter

def main():
    bpf_trfile_reader = TraceFileReader(Path('test_file.out'))

    global_syscall_stats = GlobalSysCallCount(name='g-syscall-count', dir_name='/data/db')
    global_pid_tid_info = GlobalPidTidInfo(name='g-pidtid-info', dir_name='/data/db')
    global_csvfy = GlobalCSVFy(name='g-csvfy', dir_name='/data/db', csv_filename='./output_results/test_file.csv')
    
    per_file_syscall_stats = PerFileSysCallCount(name='pf-syscall-count', dir_name='/data/db')
    
    telemetry_content_router = TelemetryContentRouter(name='tlt-router', dir_name='/data/db')

    bpf_trfile_reader.subscribe(global_syscall_stats)
    bpf_trfile_reader.subscribe(global_pid_tid_info)
    bpf_trfile_reader.subscribe(per_file_syscall_stats)
    bpf_trfile_reader.subscribe(telemetry_content_router)
    bpf_trfile_reader.subscribe(global_csvfy)

    bpf_trfile_reader.read_file()
    
    global_syscall_stats.write_output_file(output_file='./output_results/global_syscall_count.json')
    global_pid_tid_info.write_output_file(output_file='./output_results/global_pid_tid_info.json')
    
    per_file_syscall_stats.calculate_total_calls_per_file()
    per_file_syscall_stats.write_output_file(output_file='./output_results/per_file_syscall_counts.json')
    

if __name__ == '__main__':
    main()
