class MemoryManager:
    TOTAL_MB = 100

    def __init__(self):
        self.allocations: dict[int, int] = {}

    @property
    def used_mb(self) -> int:
        return sum(self.allocations.values())

    @property
    def free_mb(self) -> int:
        return self.TOTAL_MB - self.used_mb

    def allocate(self, pid: int, amount_mb: int):
        if amount_mb <= 0:
            raise ValueError("La memoria debe ser mayor que 0 MB.")
        if pid in self.allocations:
            raise ValueError(f"El PID {pid} ya tiene memoria asignada.")
        if amount_mb > self.free_mb:
            raise MemoryError(
                f"Out of Memory: se solicitaron {amount_mb} MB y solo hay {self.free_mb} MB disponibles."
            )
        self.allocations[pid] = amount_mb

    def release(self, pid: int) -> int:
        return self.allocations.pop(pid, 0)

    def status(self) -> str:
        return (
            f"RAM TOTAL: {self.TOTAL_MB} MB | "
            f"USADA: {self.used_mb} MB | "
            f"DISPONIBLE: {self.free_mb} MB"
        )
