from pathlib import Path

class TelemetryContentRouter():
    def __init__(self, name: str, dir_name: str) -> None:
        self.name = name
        self.fd_filename = dict()
        self.tlt_file_id = 0
        self.dir_name = dir_name

    def process(self, message: str):
        if message[:4] != 'time':
            return
        
        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename.startswith(self.dir_name):
            syscall_name = message.split()[[field.startswith('probe') for field in message.split()].index(True)].split('=')[1].split('_')[2]
            pid = int(message.split()[[field.startswith('pid') for field in message.split()].index(True)].split('=')[1])
            tid = int(message.split()[[field.startswith('tid') for field in message.split()].index(True)].split('=')[1])
            fd = int(message.split()[[field.startswith('fd') for field in message.split()].index(True)].split('=')[1])

            if syscall_name == 'open' or syscall_name == 'openat' or syscall_name == 'openat2' or syscall_name == 'creat':
                tlt_filename = filename.replace('/', '_') + '.tlt'    
                if fd not in self.fd_filename:
                    tlt_fd_file = TelemetryFile(tlt_file_name='./telemetry_files/' + tlt_filename)
                    tlt_fd_file.create()
                    self.fd_filename[(pid,tid,fd)] = tlt_fd_file

            if syscall_name == 'close':
                self.fd_filename[(pid,tid,fd)].add_line(line=message)
                self.fd_filename.pop((pid,tid,fd))
                return

            self.fd_filename[(pid,tid,fd)].add_line(line=message)
        else:
            return


class TelemetryFile():
    def __init__(self, tlt_file_name: str) -> None:
        self.tlt_file_name = Path(tlt_file_name)

    def __str__(self) -> str:
        return self.tlt_file_name.name

    def create(self):
        self.tlt_file_name.touch()

    def add_line(self, line: str):            
        with open(file=self.tlt_file_name.absolute(), mode='+a') as fd_tlt_file:
            fd_tlt_file.write(line)
    