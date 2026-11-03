# Simulador de Funciones del Kernel Sistema Operativo

Proyecto Final del curso **Sistemas Operativos I**.

## Información académica

- Universidad Mariano Gálvez de Guatemala
- Curso: Sistemas Operativos I
- Catedrático: Ing. Julio Roberto Gómez Orozco
- Estudiante: Rene Abraham Pirir Cuc
- Carné: 7690-23-22174
- Sección: B

## Descripción

Simulador académico desarrollado en Python mediante una interfaz de línea de comandos (CLI) para representar funciones básicas de un sistema operativo.

El proyecto incluye:

- Gestión de procesos mediante PCB y TCB.
- Gestión de memoria RAM simulada de 100 MB.
- Planificación Round Robin con quantum q=3.
- Semáforo binario y exclusión mutua.
- Simulación, detección y resolución de Deadlock.

## Requisitos

- Python 3.10 o superior.

No requiere librerías externas.

## Ejecución

Desde la carpeta principal del proyecto:

```powershell
python main.py
```

Para ejecutar las pruebas básicas:

```powershell
python demo_pruebas.py
```

## Estructura principal

- `main.py`: inicio del simulador.
- `kernel_sim/`: módulos del sistema.
- `demo_pruebas.py`: pruebas automáticas.

## Autor

Rene Abraham Pirir Cuc  
Carné: 7690-23-22174