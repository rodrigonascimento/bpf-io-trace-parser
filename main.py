from pathlib import Path
from io_profiler.file_reader import TraceFileReader
from io_profiler.io_stats import GlobalSysCallCount, PerFileSysCallCount
from io_profiler.telemetry import TelemetryContentRouter

def main():
    bpf_trfile_reader = TraceFileReader(Path('test_file.out'))

    global_io_stats = GlobalSysCallCount(name='g-syscall-count', dir_name='/data/db')
    per_file_io_stats = PerFileSysCallCount(name='pf-syscall-count', dir_name='/data/db')
    telemetry_content_router = TelemetryContentRouter(name='tlt-router', dir_name='/data/db')

    bpf_trfile_reader.subscribe(global_io_stats)
    bpf_trfile_reader.subscribe(per_file_io_stats)
    bpf_trfile_reader.subscribe(telemetry_content_router)

    bpf_trfile_reader.read_file()

    global_io_stats.write_output_file()

    per_file_io_stats.calculate_total_calls_per_file()
    per_file_io_stats.write_output_file()

if __name__ == '__main__':
    main()
