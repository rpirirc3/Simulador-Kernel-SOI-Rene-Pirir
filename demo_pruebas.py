"""
Pruebas automatizadas sencillas para validar los requisitos principales.
Ejecutar:
    python demo_pruebas.py
"""

from kernel_sim.memory import MemoryManager
from kernel_sim.process_manager import ProcessManager
from kernel_sim.scheduler import RoundRobinScheduler
from kernel_sim.semaphore_sim import BinarySemaphore
from kernel_sim.deadlock import DeadlockManager


def prueba_memoria():
    memory = MemoryManager()
    pm = ProcessManager(memory)
    pm.create_process(1, 30, 8)
    pm.create_process(2, 40, 4)
    pm.create_process(3, 20, 2)
    assert memory.used_mb == 90
    try:
        pm.create_process(4, 20, 1)
        raise AssertionError("Debió producir Out of Memory")
    except MemoryError:
        pass
    print("[OK] Gestión de memoria / Out of Memory")


def prueba_round_robin():
    memory = MemoryManager()
    pm = ProcessManager(memory)
    pm.create_process(1, 10, 8)
    pm.create_process(2, 10, 4)
    pm.create_process(3, 10, 2)
    log = RoundRobinScheduler().run(pm)
    assert all(p.burst_remaining == 0 for p in pm.processes.values())
    assert all(p.state.value == "TERMINADO" for p in pm.processes.values())
    assert any("q=3" in line for line in log)
    print("[OK] Round Robin q=3")


def prueba_semaforo():
    memory = MemoryManager()
    pm = ProcessManager(memory)
    p1 = pm.create_process(1, 10, 5)
    p2 = pm.create_process(2, 10, 5)
    s = BinarySemaphore()
    assert "entra" in s.wait(p1)
    assert "BLOQUEADO" in s.wait(p2)
    assert "sale de la cola" in s.signal(p1)
    assert s.owner_pid == 2
    print("[OK] Semáforo binario wait()/signal()")


def prueba_deadlock():
    memory = MemoryManager()
    pm = ProcessManager(memory)
    p1 = pm.create_process(1, 10, 5)
    p2 = pm.create_process(2, 10, 5)
    d = DeadlockManager()
    d.force_demo(p1, p2)
    detected, _ = d.detect()
    assert detected
    d.abort_and_release(2, pm)
    detected, _ = d.detect()
    assert not detected
    print("[OK] Detección y resolución de Deadlock")


if __name__ == "__main__":
    prueba_memoria()
    prueba_round_robin()
    prueba_semaforo()
    prueba_deadlock()
    print("\nTODAS LAS PRUEBAS BÁSICAS PASARON CORRECTAMENTE.")
