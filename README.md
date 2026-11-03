# Simulador de Funciones del Kernel / Sistema Operativo

Proyecto Final del curso **Sistemas Operativos I**, desarrollado como un simulador académico por línea de comandos para representar de forma lógica algunas funciones fundamentales del núcleo de un sistema operativo.

## Información académica

**Universidad:** Universidad Mariano Gálvez de Guatemala  
**Facultad:** Ingeniería en Sistemas de Información y Ciencias de la Computación  
**Curso:** Sistemas Operativos I  
**Catedrático:** Ing. Julio Roberto Gómez Orozco  
**Estudiante:** Rene Abraham Pirir Cuc  
**Carné:** 7690-23-22174  
**Sección:** B  

---

## Descripción

El proyecto implementa un simulador de funciones del Kernel mediante una interfaz de línea de comandos (CLI).

El objetivo es representar de manera práctica conceptos estudiados en Sistemas Operativos I, entre ellos:

- Gestión de procesos.
- PCB y TCB.
- Gestión de memoria.
- Planificación Round Robin.
- Exclusión mutua.
- Semáforos binarios.
- Sección crítica.
- Interbloqueo o Deadlock.
- Detección y resolución de Deadlock.

El simulador trabaja con estructuras de datos y no interactúa directamente con el hardware del equipo.

---

## Tecnologías utilizadas

- **Python:** 3.13.17
- **Visual Studio Code**
- **Git:** 2.56.0.windows.4
- **Sistema operativo de desarrollo:** Windows
- **Interfaz:** CLI / consola

El proyecto utiliza únicamente módulos incluidos en la biblioteca estándar de Python, por lo que no requiere instalar dependencias externas.

---

## Estructura del proyecto

```text
KernelSimulator_SOI/
│
├── main.py
├── demo_pruebas.py
├── README.md
├── INSTRUCCIONES_VSCODE.txt
├── .gitignore
│
└── kernel_sim/
    ├── __init__.py
    ├── cli.py
    ├── models.py
    ├── process_manager.py
    ├── memory.py
    ├── scheduler.py
    ├── semaphore_sim.py
    └── deadlock.py
```

### Descripción de archivos principales

**main.py**  
Punto de entrada del programa. Inicia la interfaz CLI del simulador.

**models.py**  
Contiene las estructuras utilizadas para representar PCB, TCB y estados de los procesos.

**process_manager.py**  
Administra la creación, consulta, terminación y aborto de procesos.

**memory.py**  
Gestiona la memoria RAM simulada de 100 MB.

**scheduler.py**  
Implementa el algoritmo de planificación Round Robin con quantum fijo de 3 unidades.

**semaphore_sim.py**  
Simula exclusión mutua mediante un semáforo binario con operaciones `wait()` y `signal()`.

**deadlock.py**  
Permite simular, detectar y resolver una condición de Deadlock utilizando dos recursos exclusivos.

**cli.py**  
Contiene el menú principal y las opciones disponibles para interactuar con el simulador.

**demo_pruebas.py**  
Ejecuta pruebas básicas automáticas sobre los principales módulos del sistema.

---

## Funcionalidades implementadas

### 1. Gestión de procesos

Cada proceso se representa mediante un PCB que contiene:

- PID.
- Estado actual.
- Tamaño en memoria.
- Ráfaga total de CPU.
- Ráfaga restante.

También se utiliza un TCB asociado con:

- TID.
- PID asociado.
- Estado.

El sistema permite crear y consultar procesos desde la consola.

---

### 2. Gestión de memoria

El simulador cuenta con una memoria RAM de:

```text
100 MB
```

Al crear un proceso se valida si existe suficiente memoria disponible.

Si la solicitud supera la capacidad restante, el proceso es rechazado mediante un mensaje:

```text
Out of Memory
```

La memoria asignada se libera cuando un proceso termina o es abortado.

---

### 3. Planificación Round Robin

Se implementa el algoritmo Round Robin con:

```text
Quantum = 3
```

Cada proceso puede ejecutar como máximo tres unidades por turno.

Si no termina:

1. Se actualiza su ráfaga restante.
2. Se simula un cambio de contexto.
3. Regresa al final de la cola de listos.

Si la ráfaga restante llega a cero, el proceso cambia al estado `TERMINADO` y libera su memoria.

---

### 4. Concurrencia y exclusión mutua

Se utiliza un semáforo binario para controlar una sección crítica.

Operaciones disponibles:

```text
wait()
signal()
```

Comportamiento probado:

- Un proceso puede ingresar a la sección crítica.
- Si otro proceso intenta ingresar mientras está ocupada, queda bloqueado.
- El proceso bloqueado se almacena en una cola de espera.
- Al ejecutar `signal()`, la sección crítica se libera.
- El siguiente proceso de la cola puede ingresar.

También se incluye una Variable Global Compartida para representar el acceso controlado a un recurso común.

---

### 5. Deadlock

El simulador dispone de dos recursos exclusivos:

```text
R1
R2
```

Se puede generar intencionalmente una condición de espera circular:

```text
Proceso A retiene R1 y solicita R2.
Proceso B retiene R2 y solicita R1.
```

El sistema detecta la condición y muestra:

```text
DEADLOCK DETECTADO
```

Para resolverla, el usuario puede abortar uno de los procesos.

Al abortarlo:

- se liberan sus recursos;
- otro proceso puede continuar;
- se rompe la espera circular;
- el sistema confirma que ya no existe Deadlock.

---

## Menú principal

El simulador presenta las siguientes opciones:

```text
1. Crear proceso (PCB / TCB)
2. Ver procesos
3. Ver memoria RAM
4. Ejecutar Round Robin (q=3)
5. Semáforo binario / sección crítica
6. Simular Deadlock
7. Resolver Deadlock abortando un proceso
8. Ver estado Deadlock
9. Cargar escenario de demostración
0. Salir
```

---

## Cómo ejecutar el proyecto

Abrir una terminal dentro de la carpeta principal del proyecto.

Ejecutar:

```powershell
python main.py
```

El programa mostrará el menú principal del simulador.

---

## Pruebas automáticas

Para ejecutar las pruebas básicas:

```powershell
python demo_pruebas.py
```

Las pruebas verifican:

- Gestión de memoria y `Out of Memory`.
- Round Robin con `q=3`.
- Semáforo binario.
- Operaciones `wait()` y `signal()`.
- Detección de Deadlock.
- Resolución de Deadlock.

---

## Escenario de demostración

La opción:

```text
9. Cargar escenario de demostración
```

crea los siguientes procesos:

```text
P1: 30 MB, BT=8
P2: 40 MB, BT=4
P3: 20 MB, BT=2
```

La memoria utilizada inicialmente es:

```text
90 MB
```

Al intentar crear un proceso adicional de 20 MB, el sistema detecta que solo quedan 10 MB disponibles y genera un error `Out of Memory`.

---

## Pruebas realizadas

Durante la validación manual del proyecto se comprobaron los siguientes casos:

### Gestión de procesos

- Creación de procesos.
- Visualización de PCB y TCB.
- Rechazo de PID duplicado.
- Rechazo de valores inválidos.

### Gestión de memoria

- RAM total de 100 MB.
- Asignación correcta de memoria.
- Rechazo por falta de RAM.
- Liberación de memoria al finalizar procesos.
- Liberación de memoria al abortar procesos.

### Round Robin

Se validó inicialmente con:

```text
P1 = 8
P2 = 4
P3 = 2
Quantum = 3
```

También se realizó una prueba adicional con valores diferentes:

```text
PID 10: 25 MB, BT=11
PID 20: 35 MB, BT=7
PID 30: 15 MB, BT=5
```

La memoria utilizada fue:

```text
75 MB
```

Los tres procesos finalizaron correctamente mediante Round Robin y, al terminar, la memoria quedó nuevamente en:

```text
RAM TOTAL: 100 MB
USADA: 0 MB
DISPONIBLE: 100 MB
```

### Semáforo

Se verificó el siguiente flujo:

```text
PID 1 ejecuta wait() y entra a la sección crítica.

PID 2 ejecuta wait() mientras la sección está ocupada
y queda BLOQUEADO.

PID 1 ejecuta signal().

PID 2 sale de la cola y entra a la sección crítica.
```

### Deadlock

Se generó la siguiente condición:

```text
PID 1 retiene R1.
PID 2 retiene R2.
PID 1 espera R2.
PID 2 espera R1.
```

El sistema detectó correctamente:

```text
DEADLOCK DETECTADO
```

Posteriormente se abortó el PID 2, se liberó R2 y el sistema confirmó:

```text
No se detectó deadlock.
```

---

## Validaciones de la interfaz

También se comprobó que:

- El menú puede utilizarse repetidamente sin reiniciar el programa.
- Una opción incorrecta como `99` muestra `Opción inválida`.
- El programa continúa funcionando después de una entrada incorrecta.
- La opción `0` finaliza correctamente el simulador.

---

## Objetivo académico

Este proyecto permite aplicar de manera práctica conceptos fundamentales de Sistemas Operativos I mediante la simulación de estructuras y mecanismos utilizados por un Kernel.

La implementación busca facilitar la comprensión de la administración de procesos, planificación de CPU, memoria, concurrencia y condiciones de interbloqueo.

---

## Estado del proyecto

Las funciones principales del simulador fueron implementadas y probadas mediante pruebas automáticas y manuales.

Se verificaron satisfactoriamente:

- Gestión de procesos.
- PCB y TCB.
- Gestión de memoria.
- Round Robin.
- Semáforo binario.
- Exclusión mutua.
- Deadlock.
- Resolución de Deadlock.
- Validaciones de la interfaz CLI.
- Pruebas con diferentes parámetros.

---

## Autor

**Rene Abraham Pirir Cuc**  
Carné: **7690-23-22174**  
Universidad Mariano Gálvez de Guatemala  
Sistemas Operativos I