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
