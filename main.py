import argparse

from pathlib import Path
from io_profiler.file_reader import TraceFileReader
from io_profiler.global_io_stats import GlobalCSVFy, GlobalEventCount

def cli_args():
    parser = argparse.ArgumentParser(
        prog='io-trace-parser',
        description='Parse information out of the ebpf-syscall-io-tracer.bt program.'
    )

    parser.add_argument('--trace-file', type=str, help='Trace file to be parsed.')
    parser.add_argument('--csv-output', type=str, help='CSV filename.')
    parser.add_argument('--tlt-output', type=str, help='Per-file telemetry output directory.')

    return parser.parse_args()

def main():
    cli = cli_args()

    bpf_trfile_reader = TraceFileReader(cli.trace_file)
    global_csvfy = GlobalCSVFy(name='g-csvfy', csv_filename=cli.csv_output)
    global_evt_count = GlobalEventCount(name='g-evt-count')
    
    bpf_trfile_reader.subscribe(global_csvfy)
    bpf_trfile_reader.subscribe(global_evt_count)
    bpf_trfile_reader.read_file()    

    global_evt_count.write_output_file(output_file='./output_results/event_count.csv')


if __name__ == '__main__':
    main()
