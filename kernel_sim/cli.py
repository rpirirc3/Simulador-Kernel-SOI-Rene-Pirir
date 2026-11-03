from kernel_sim.memory import MemoryManager
from kernel_sim.process_manager import ProcessManager
from kernel_sim.scheduler import RoundRobinScheduler
from kernel_sim.semaphore_sim import BinarySemaphore
from kernel_sim.deadlock import DeadlockManager


class KernelSimulatorCLI:
    def __init__(self):
        self.memory = MemoryManager()
        self.pm = ProcessManager(self.memory)
        self.scheduler = RoundRobinScheduler()
        self.semaphore = BinarySemaphore()
        self.deadlock = DeadlockManager()

    @staticmethod
    def pause():
        input("\nPresione ENTER para continuar...")

    @staticmethod
    def read_int(prompt: str, minimum: int = 1) -> int:
        while True:
            try:
                value = int(input(prompt).strip())
                if value < minimum:
                    print(f"El valor debe ser >= {minimum}.")
                    continue
                return value
            except ValueError:
                print("Entrada inválida. Ingrese un número entero.")

    def menu(self):
        print("\n" + "=" * 68)
        print(" SIMULADOR DE FUNCIONES DEL KERNEL / SISTEMA OPERATIVO ")
        print("=" * 68)
        print("1. Crear proceso (PCB / TCB)")
        print("2. Ver procesos")
        print("3. Ver memoria RAM")
        print("4. Ejecutar Round Robin (q=3)")
        print("5. Semáforo binario / sección crítica")
        print("6. Simular Deadlock")
        print("7. Resolver Deadlock abortando un proceso")
        print("8. Ver estado Deadlock")
        print("9. Cargar escenario de demostración")
        print("0. Salir")

    def create_process(self):
        pid = self.read_int("PID: ")
        memory_mb = self.read_int("Memoria requerida (MB): ")
        burst = self.read_int("Ráfaga CPU total: ")
        try:
            pcb = self.pm.create_process(pid, memory_mb, burst)
            print(
                f"Proceso creado: PID={pcb.pid}, TID={pcb.tcb.tid}, "
                f"Memoria={pcb.memory_mb} MB, BT={pcb.burst_total}"
            )
        except (ValueError, MemoryError) as e:
            print(f"ERROR: {e}")

    def semaphore_menu(self):
        print("\n--- SEMÁFORO BINARIO ---")
        print("1. wait()")
        print("2. Modificar variable compartida")
        print("3. signal()")
        print("4. Estado")
        option = input("Opción: ").strip()

        if option in {"1", "2", "3"}:
            pid = self.read_int("PID: ")
            try:
                pcb = self.pm.get(pid)
            except KeyError as e:
                print(e)
                return

            if option == "1":
                print(self.semaphore.wait(pcb))
            elif option == "2":
                amount = self.read_int("Incremento: ", minimum=1)
                print(self.semaphore.increment_shared(pcb, amount))
            elif option == "3":
                print(self.semaphore.signal(pcb))
        elif option == "4":
            print(self.semaphore.status())
        else:
            print("Opción inválida.")

    def simulate_deadlock(self):
        active = [p for p in self.pm.active_processes()]
        if len(active) < 2:
            print("Se requieren al menos 2 procesos activos para simular deadlock.")
            return
        print("Procesos activos:", [p.pid for p in active])
        pid_a = self.read_int("PID A: ")
        pid_b = self.read_int("PID B: ")
        if pid_a == pid_b:
            print("Debe seleccionar dos PID diferentes.")
            return
        try:
            a = self.pm.get(pid_a)
            b = self.pm.get(pid_b)
            for line in self.deadlock.force_demo(a, b):
                print(line)
        except (KeyError, ValueError, RuntimeError) as e:
            print(f"ERROR: {e}")

    def resolve_deadlock(self):
        pid = self.read_int("PID a abortar: ")
        try:
            for line in self.deadlock.abort_and_release(pid, self.pm):
                print(line)
        except KeyError as e:
            print(f"ERROR: {e}")

    def load_demo(self):
        if self.pm.processes:
            print("El escenario demo solo se carga cuando no existen procesos.")
            return
        demo = [(1, 30, 8), (2, 40, 4), (3, 20, 2)]
        for pid, mem, burst in demo:
            self.pm.create_process(pid, mem, burst)
        print("Escenario cargado:")
        print("P1: 30 MB, BT=8")
        print("P2: 40 MB, BT=4")
        print("P3: 20 MB, BT=2")
        print("RAM usada = 90 MB. Puede intentar crear P4 con 20 MB para probar Out of Memory.")

    def run(self):
        while True:
            self.menu()
            option = input("Seleccione una opción: ").strip()

            if option == "1":
                self.create_process()
                self.pause()
            elif option == "2":
                print("\n" + self.pm.table())
                self.pause()
            elif option == "3":
                print("\n" + self.memory.status())
                self.pause()
            elif option == "4":
                print()
                for line in self.scheduler.run(self.pm):
                    print(line)
                self.pause()
            elif option == "5":
                self.semaphore_menu()
                self.pause()
            elif option == "6":
                self.simulate_deadlock()
                self.pause()
            elif option == "7":
                self.resolve_deadlock()
                self.pause()
            elif option == "8":
                print(self.deadlock.status())
                detected, message = self.deadlock.detect()
                print(message)
                self.pause()
            elif option == "9":
                self.load_demo()
                self.pause()
            elif option == "0":
                print("Simulador finalizado.")
                break
            else:
                print("Opción inválida.")
                self.pause()
