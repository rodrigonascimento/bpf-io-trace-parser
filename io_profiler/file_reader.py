from pathlib import Path

class TraceFileReader():
    def __init__(self, trace_filename: Path) -> None:
        self.trace_file = trace_filename
        self.subscribers = list()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def _publish(self, message: str):
        for subscriber in self.subscribers:
            subscriber.process(message)

    def read_file(self):
        with open(file=self.trace_file.name, mode='r') as bpf_output:
            for line in bpf_output.readlines():
                self._publish(line)
