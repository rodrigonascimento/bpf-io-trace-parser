import json
from pathlib import Path

class GlobalIOStats():
    def __init__(self, name: str) -> None:
        self.global_syscall_counts = dict()
        self.name = name

    def process(self, message: str):
        if message[:4] != 'time': 
            return
        
        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith('/data/db'):
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

class PerFileIOStats():
    def __init__(self, name: str) -> None:
        self.per_file_syscall_counts = dict()
        self.name = name

    def process(self, message: str):
        if message[:4] != 'time':
            return

        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith('/data/db'):
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

    def write_output_file(self):
        with open(file='per_file_syscall_counts.json', mode='w') as per_file_syscounts_output:
            json.dump(self.per_file_syscall_counts, per_file_syscounts_output, indent=2)

