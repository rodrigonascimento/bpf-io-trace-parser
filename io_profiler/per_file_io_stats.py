import json
from pathlib import Path
from io_profiler.telemetry import TelemetryFile

class PerFileEvents():
    def __init__(self, name: str, tlt_dir: str):
        self.name = name
        self.tlt_dir = tlt_dir
        self.fd_filename = dict()
    
    def process(self, message: str): 
        if message[:4] != 'time': 
            return
        
        filename       = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        timestamp      = message.split()[[field.startswith('time') for field in message.split()].index(True)].split('=')[1].split('.')[0]
        ms             = message.split()[[field.startswith('time') for field in message.split()].index(True)].split('=')[1].split('.')[1]
        probe          = message.split()[[field.startswith('probe') for field in message.split()].index(True)].split('=')[1].split('_')[2]
        process        = message.split()[[field.startswith('process') for field in message.split()].index(True)].split('=')[1]
        pid            = message.split()[[field.startswith('pid') for field in message.split()].index(True)].split('=')[1]
        tid            = message.split()[[field.startswith('tid') for field in message.split()].index(True)].split('=')[1]
        fd             = message.split()[[field.startswith('fd') for field in message.split()].index(True)].split('=')[1]        
        lat_ns = message.split()[[field.startswith('lat') for field in message.split()].index(True)].split('=')[1] if 'lat=' in message else ''
        req_size_bytes = message.split()[[field.startswith('req_size_bytes') for field in message.split()].index(True)].split('=')[1] if 'req_size_bytes=' in message else ''
        offset         = message.split()[[field.startswith('offset') for field in message.split()].index(True)].split('=')[1] if 'offset' in message else ''
        if 'read' in probe:
            bytes_rw   = message.split()[[field.startswith('bytes_read') for field in message.split()].index(True)].split('=')[1]
        elif 'write' in probe:
            bytes_rw   = message.split()[[field.startswith('bytes_written') for field in message.split()].index(True)].split('=')[1]
        else:
            bytes_rw   = ''
        
        line = timestamp + ',' + ms + ',' + probe + ',' + process + ',' + pid + ',' + tid + ',' + filename + ',' + fd + ',' + lat_ns + ',' + req_size_bytes + ',' + offset + ',' + bytes_rw
        
        tlt_filename = 'tlt' + filename.replace('/', '_') + '_' + fd +'.csv'
        if (pid,tid,fd,filename) not in self.fd_filename:
            tlt_csv_file = TelemetryFile(csv_filename=self.tlt_dir + '/' + tlt_filename)
            self.fd_filename[(pid,tid,fd,filename)] = tlt_csv_file
                
        self.fd_filename[(pid,tid,fd,filename)].add_line(line=line)

class PerFileSysCallCount():
    def __init__(self, name: str, dir_name: str) -> None:
        self.per_file_syscall_counts = dict()
        self.name = name
        self.dir_name = dir_name

    def process(self, message: str):
        if message[:4] != 'time':
            return

        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith(self.dir_name):
            syscall_name = message.split()[[field.startswith('probe') for field in message.split()].index(True)].split('=')[1].split('_')[2]

            if filename not in self.per_file_syscall_counts:
                self.per_file_syscall_counts[filename] = dict()
                self.per_file_syscall_counts[filename][syscall_name] = 1
            else:
                if syscall_name not in self.per_file_syscall_counts[filename]:
                    self.per_file_syscall_counts[filename][syscall_name] = 1
                else:
                    self.per_file_syscall_counts[filename][syscall_name] += 1
        else:
            return

    def calculate_total_calls_per_file(self):
        for f in self.per_file_syscall_counts.keys():
            total = 0
            for s in self.per_file_syscall_counts[f].keys():
                total += self.per_file_syscall_counts[f][s]
            
            self.per_file_syscall_counts[f]['total'] = total

    def write_output_file(self, output_file: str):
        with open(file=output_file, mode='w') as per_file_syscounts_output:
            json.dump(self.per_file_syscall_counts, per_file_syscounts_output, indent=2)
