from collections import deque
from kernel_sim.models import ProcessState


class BinarySemaphore:
    def __init__(self):
        self.value = 1
        self.owner_pid: int | None = None
        self.waiting = deque()
        self.shared_value = 0

    def wait(self, pcb) -> str:
        if self.owner_pid == pcb.pid:
            return f"PID {pcb.pid} ya posee la sección crítica."

        if self.value == 1:
            self.value = 0
            self.owner_pid = pcb.pid
            pcb.set_state(ProcessState.RUNNING)
            return f"PID {pcb.pid} ejecuta wait(): entra a la sección crítica."

        if pcb.pid not in [p.pid for p in self.waiting]:
            pcb.set_state(ProcessState.BLOCKED)
            self.waiting.append(pcb)
        return (
            f"PID {pcb.pid} ejecuta wait(): sección ocupada por PID "
            f"{self.owner_pid}; queda BLOQUEADO."
        )

    def increment_shared(self, pcb, amount: int = 1) -> str:
        if self.owner_pid != pcb.pid:
            return f"ERROR: PID {pcb.pid} no posee la sección crítica."
        self.shared_value += amount
        return (
            f"PID {pcb.pid} modifica Variable Global Compartida -> "
            f"{self.shared_value}"
        )

    def signal(self, pcb) -> str:
        if self.owner_pid != pcb.pid:
            return f"ERROR: PID {pcb.pid} no puede liberar un semáforo que no posee."

        pcb.set_state(ProcessState.READY)
        self.owner_pid = None
        self.value = 1
        msg = f"PID {pcb.pid} ejecuta signal(): libera la sección crítica."

        if self.waiting:
            next_pcb = self.waiting.popleft()
            self.value = 0
            self.owner_pid = next_pcb.pid
            next_pcb.set_state(ProcessState.RUNNING)
            msg += f" PID {next_pcb.pid} sale de la cola y entra a la sección crítica."

        return msg

    def status(self) -> str:
        queue = [p.pid for p in self.waiting]
        return (
            f"Semáforo={self.value} | Dueño={self.owner_pid} | "
            f"Cola={queue} | VariableGlobal={self.shared_value}"
        )
