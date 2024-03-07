from pathlib import Path
from io_profiler.file_reader import TraceFileReader
from io_profiler.io_stats import GlobalIOStats, PerFileIOStats

def main():
    bpf_trfile_reader = TraceFileReader(Path('test_file.out'))

    global_io_stats = GlobalIOStats(name='global_stats')
    per_file_io_stats = PerFileIOStats(name='per-file-stats')

    bpf_trfile_reader.subscribe(global_io_stats)
    bpf_trfile_reader.subscribe(per_file_io_stats)

    bpf_trfile_reader.read_file()

    global_io_stats.write_output_file()
    per_file_io_stats.write_output_file()

if __name__ == '__main__':
    main()
