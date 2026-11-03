from kernel_sim.models import PCB, ProcessState
from kernel_sim.memory import MemoryManager


class ProcessManager:
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.processes: dict[int, PCB] = {}

    def create_process(self, pid: int, memory_mb: int, burst: int) -> PCB:
        if pid <= 0:
            raise ValueError("El PID debe ser mayor que 0.")
        if pid in self.processes:
            raise ValueError(f"Ya existe un proceso con PID {pid}.")
        if burst <= 0:
            raise ValueError("La ráfaga de CPU debe ser mayor que 0.")

        self.memory.allocate(pid, memory_mb)
        pcb = PCB(
            pid=pid,
            memory_mb=memory_mb,
            burst_total=burst,
            burst_remaining=burst,
            state=ProcessState.READY,
        )
        pcb.tcb.state = ProcessState.READY
        self.processes[pid] = pcb
        return pcb

    def get(self, pid: int) -> PCB:
        if pid not in self.processes:
            raise KeyError(f"No existe el PID {pid}.")
        return self.processes[pid]

    def active_processes(self):
        return [
            p for p in self.processes.values()
            if p.state not in (ProcessState.TERMINATED, ProcessState.ABORTED)
        ]

    def abort_process(self, pid: int) -> PCB:
        pcb = self.get(pid)
        pcb.set_state(ProcessState.ABORTED)
        pcb.burst_remaining = 0
        self.memory.release(pid)
        return pcb

    def terminate_process(self, pid: int) -> PCB:
        pcb = self.get(pid)
        pcb.set_state(ProcessState.TERMINATED)
        pcb.burst_remaining = 0
        self.memory.release(pid)
        return pcb

    def table(self) -> str:
        if not self.processes:
            return "No hay procesos registrados."

        header = (
            f"{'PID':<6}{'ESTADO':<14}{'MEM(MB)':<10}"
            f"{'BT TOTAL':<10}{'BT REST':<10}{'TID':<8}"
        )
        lines = [header, "-" * len(header)]
        for p in sorted(self.processes.values(), key=lambda x: x.pid):
            lines.append(
                f"{p.pid:<6}{p.state.value:<14}{p.memory_mb:<10}"
                f"{p.burst_total:<10}{p.burst_remaining:<10}{p.tcb.tid:<8}"
            )
        return "\n".join(lines)
