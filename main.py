from pathlib import Path
from io_profiler.file_reader import TraceFileReader
from io_profiler.global_io_stats import GlobalCSVFy

def main():
    bpf_trfile_reader = TraceFileReader(Path('test_file.out'))
    global_csvfy = GlobalCSVFy(name='g-csvfy', dir_name='/data/db', csv_filename='./output_results/test_file.csv')
    bpf_trfile_reader.subscribe(global_csvfy)
    bpf_trfile_reader.read_file()    


if __name__ == '__main__':
    main()
