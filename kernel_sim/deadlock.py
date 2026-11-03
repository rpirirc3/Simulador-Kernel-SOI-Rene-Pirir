from kernel_sim.models import ProcessState


class DeadlockManager:
    def __init__(self):
        self.resources = {"R1": None, "R2": None}
        self.waiting_for: dict[int, str] = {}

    def reset(self):
        self.resources = {"R1": None, "R2": None}
        self.waiting_for.clear()

    def assign(self, pid: int, resource: str):
        if resource not in self.resources:
            raise ValueError("Recurso inválido.")
        if self.resources[resource] is not None:
            raise RuntimeError(f"{resource} ya está ocupado por PID {self.resources[resource]}.")
        self.resources[resource] = pid

    def request(self, pid: int, resource: str) -> str:
        if resource not in self.resources:
            raise ValueError("Recurso inválido.")
        owner = self.resources[resource]
        if owner is None:
            self.resources[resource] = pid
            self.waiting_for.pop(pid, None)
            return f"PID {pid} obtiene {resource}."
        if owner == pid:
            return f"PID {pid} ya posee {resource}."
        self.waiting_for[pid] = resource
        return f"PID {pid} espera {resource}, retenido por PID {owner}."

    def detect(self) -> tuple[bool, str]:
        # Con dos recursos exclusivos, basta detectar espera circular entre dos PID.
        for pid_a, res_a in list(self.waiting_for.items()):
            owner_b = self.resources.get(res_a)
            if owner_b is None or owner_b == pid_a:
                continue
            res_b = self.waiting_for.get(owner_b)
            if res_b is None:
                continue
            owner_a = self.resources.get(res_b)
            if owner_a == pid_a:
                return True, (
                    f"DEADLOCK DETECTADO: PID {pid_a} espera {res_a} "
                    f"(retenido por PID {owner_b}) y PID {owner_b} espera "
                    f"{res_b} (retenido por PID {pid_a})."
                )
        return False, "No se detectó deadlock."

    def force_demo(self, pcb_a, pcb_b) -> list[str]:
        self.reset()
        pcb_a.set_state(ProcessState.RUNNING)
        pcb_b.set_state(ProcessState.RUNNING)

        self.assign(pcb_a.pid, "R1")
        self.assign(pcb_b.pid, "R2")
        log = [
            f"PID {pcb_a.pid} retiene R1.",
            f"PID {pcb_b.pid} retiene R2.",
            self.request(pcb_a.pid, "R2"),
            self.request(pcb_b.pid, "R1"),
        ]
        pcb_a.set_state(ProcessState.BLOCKED)
        pcb_b.set_state(ProcessState.BLOCKED)
        detected, message = self.detect()
        log.append(message)
        return log

    def abort_and_release(self, pid: int, process_manager) -> list[str]:
        released = []
        for resource, owner in list(self.resources.items()):
            if owner == pid:
                self.resources[resource] = None
                released.append(resource)

        self.waiting_for.pop(pid, None)
        process_manager.abort_process(pid)

        # Cualquier proceso que esperaba un recurso ahora libre puede obtenerlo.
        updates = []
        for waiting_pid, resource in list(self.waiting_for.items()):
            if self.resources[resource] is None:
                self.resources[resource] = waiting_pid
                self.waiting_for.pop(waiting_pid, None)
                try:
                    process_manager.get(waiting_pid).set_state(ProcessState.READY)
                except KeyError:
                    pass
                updates.append(f"PID {waiting_pid} obtiene {resource} tras la liberación.")

        detected, message = self.detect()
        return [
            f"PID {pid} ABORTADO.",
            f"Recursos liberados: {released if released else 'ninguno'}.",
            *updates,
            message,
        ]

    def status(self) -> str:
        return f"Recursos={self.resources} | Esperas={self.waiting_for}"
