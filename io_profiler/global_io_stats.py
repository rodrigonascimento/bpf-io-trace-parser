import json
from pathlib import Path

class GlobalSysCallCount():
    def __init__(self, name: str, dir_name: str) -> None:
        self.global_syscall_counts = dict()
        self.name = name
        self.dir_name = dir_name

    def process(self, message: str):
        if message[:4] != 'time': 
            return
        
        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith(self.dir_name):
            syscall_name = message.split()[[field.startswith('probe') for field in message.split()].index(True)].split('=')[1].split('_')[2]
            if syscall_name not in self.global_syscall_counts:
                self.global_syscall_counts[syscall_name] = 1
            else:
                self.global_syscall_counts[syscall_name] += 1
        else:
            return

    def write_output_file(self):
        with open(file='global_syscall_counts.json', mode='w') as global_syscounts_output:
            json.dump(self.global_syscall_counts, global_syscounts_output, indent=2)

class GlobalPidTidInfo():
    def __init__(self, name: str, dir_name: str) -> None:
        self.global_pid_tid_count = dict()
        self.name = name
        self.dir_name = dir_name

    def process(self, message: str):
        if message[:4] != 'time': 
            return
        
        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith(self.dir_name):
            pid = int(message.split()[[field.startswith('pid') for field in message.split()].index(True)].split('=')[1])
            tid = int(message.split()[[field.startswith('tid') for field in message.split()].index(True)].split('=')[1])
            if pid in self.global_pid_tid_count.keys():
                if not tid in self.global_pid_tid_count[pid]:
                    self.global_pid_tid_count[pid].append(tid)
            else:
                self.global_pid_tid_count[pid] = list()
                self.global_pid_tid_count[pid].append(tid) 
    
    def write_output_file(self):
        with open(file='global_pid_tid_info.json', mode='w') as g_pidtid_info:
            json.dump(self.global_pid_tid_count, g_pidtid_info, indent=2)

class GlobalCSVFy():
    def __init__(self, name: str, dir_name: str, csv_filename: str) -> None:
        self.name = name
        self.dir_name = dir_name
        self.csv_filename = csv_filename
        
    def process(self, message: str) -> None:
        if message[:4] != 'time': 
            return

        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith(self.dir_name):
            if not Path(self.csv_filename).exists():
                with open(file=self.csv_filename, mode='w') as csvfy:
                    csvfy.write('timestamp,millisecond,syscall_probe,process,pid,tid,filename,fd,lat_ns,req_size_bytes,offset,bytes\n')
            else:
                with open(file=self.csv_filename, mode='a') as csvfy:
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
                    csvfy.write(line + '\n')
