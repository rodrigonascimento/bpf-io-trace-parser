from queue import Queue
from pathlib import Path

class TraceFileReader():
    def __init__(self, trace_filename: Path) -> None:
        self.trace_file = trace_filename
        self.file_line_queue = Queue()
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message: str):
        self.file_line_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def read_file_line(self):
        with open(file=self.trace_file.name, mode='r') as bpf_output:
            for line in bpf_output.readlines():
                self.publish(line)

