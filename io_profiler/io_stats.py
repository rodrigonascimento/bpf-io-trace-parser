import json
from pathlib import Path

class GlobalIOStats():
    def __init__(self, name: str) -> None:
        self.global_syscall_counts = dict()
        self.name = name

    def receive(self, message: str):
        if message[:4] != 'time': 
            return
        
        syscall_name = message.split()[2].split('_')[2]
        if syscall_name not in self.global_syscall_counts:
            self.global_syscall_counts[syscall_name] = 1
        else:
            self.global_syscall_counts[syscall_name] += 1

    def write_output_file(self):
        with open('global_syscall_counts.json', 'w') as global_syscounts_output:
            json.dump(self.global_syscall_counts, global_syscounts_output)

class PerFileIOStats():
    def __init__(self, name: str) -> None:
        self.per_file_syscall_counts = dict()
        self.name = name

    def receive(self, message: str):
        if message[:4] != 'time':
            return
        