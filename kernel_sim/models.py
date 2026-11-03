from dataclasses import dataclass, field
from enum import Enum


class ProcessState(str, Enum):
    NEW = "NUEVO"
    READY = "LISTO"
    RUNNING = "EJECUTANDO"
    BLOCKED = "BLOQUEADO"
    TERMINATED = "TERMINADO"
    ABORTED = "ABORTADO"


@dataclass
class TCB:
    tid: int
    pid: int
    state: ProcessState = ProcessState.NEW


@dataclass
class PCB:
    pid: int
    memory_mb: int
    burst_total: int
    burst_remaining: int
    state: ProcessState = ProcessState.NEW
    tcb: TCB | None = None

    def __post_init__(self):
        if self.tcb is None:
            self.tcb = TCB(tid=self.pid * 100 + 1, pid=self.pid, state=self.state)

    def set_state(self, new_state: ProcessState):
        self.state = new_state
        if self.tcb:
            self.tcb.state = new_state
