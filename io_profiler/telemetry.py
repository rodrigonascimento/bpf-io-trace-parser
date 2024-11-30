from pathlib import Path
class TelemetryFile():
    def __init__(self, csv_filename: str) -> None:
        self.tlt_file_name = Path(csv_filename)
        self.fd_csv_file = -1

        if not self.tlt_file_name.exists():
            self.tlt_file_name.touch()
            self.fd_csv_file = open(self.tlt_file_name, 'w')
            self.fd_csv_file.write('timestamp,millisecond,syscall_probe,process,pid,tid,filename,fd,lat_ns,req_size_bytes,offset,bytes\n')
        else:
            self.fd_csv_file = open(self.tlt_file_name, 'w')

    def close(self):
        self.fd_csv_file.close()

    def __str__(self) -> str:
        return self.tlt_file_name.name

    def add_line(self, line: str):            
        self.fd_csv_file.write(line + '\n')