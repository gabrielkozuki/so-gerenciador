from enum import Enum

class Policies(Enum):
    FIFO = 0 #never preemtive
    # Shortest Job First (SJF)
    # Priority Scheduling
    # Round Robin (always preemptive)