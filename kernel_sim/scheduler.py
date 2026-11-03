from collections import deque
from kernel_sim.models import ProcessState


class RoundRobinScheduler:
    QUANTUM = 3

    def run(self, process_manager) -> list[str]:
        ready = deque(
            p for p in process_manager.active_processes()
            if p.burst_remaining > 0
        )
        log: list[str] = []

        if not ready:
            return ["No hay procesos listos para ejecutar."]

        log.append(f"Round Robin iniciado con Quantum fijo q={self.QUANTUM}")

        while ready:
            pcb = ready.popleft()

            if pcb.state in (ProcessState.ABORTED, ProcessState.TERMINATED):
                continue

            pcb.set_state(ProcessState.RUNNING)
            before = pcb.burst_remaining
            executed = min(self.QUANTUM, pcb.burst_remaining)
            pcb.burst_remaining -= executed

            log.append(
                f"PID {pcb.pid}: ejecuta {executed} unidad(es) "
                f"({before} -> {pcb.burst_remaining})"
            )

            if pcb.burst_remaining == 0:
                pcb.set_state(ProcessState.TERMINATED)
                process_manager.memory.release(pcb.pid)
                log.append(
                    f"PID {pcb.pid}: TERMINADO. Memoria liberada."
                )
            else:
                pcb.set_state(ProcessState.READY)
                ready.append(pcb)
                log.append(
                    f"PID {pcb.pid}: cambio de contexto simulado; "
                    "regresa al final de la cola."
                )

        log.append("Round Robin finalizado.")
        return log
