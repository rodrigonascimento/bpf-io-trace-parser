import json
from pathlib import Path

class GlobalCSVFy():
    def __init__(self, name: str, dir_name: str, csv_filename: str) -> None:
        self.name = name
        self.dir_name = dir_name
        self.csv_filename = csv_filename
        
    def process(self, message: str) -> None:
        if message[:4] != 'time': 
            return

        filename = message.split()[[field.startswith('filename') for field in message.split()].index(True)].split('=')[1]
        if filename:
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
        else:
            return


class GlobalEventCount():
    def __init__(self, name: str) -> None:
        self.name = name
        self.number_events_captured: int = 0
        self.number_events_lost: int = 0 

    def process(self, message: str) -> None:
        if message[:4] != 'Lost':
            self.number_events_captured += 1 
            return

        lost_events = int(message.split()[1])
        self.number_events_lost += lost_events
    
    def write_output_file(self, output_file: str):
        with open(file=output_file, mode='w') as outf:
            outf.write('events_captured,events_lost\n')
            outf.write(str(self.number_events_captured) + ',' + str(self.number_events_lost))
